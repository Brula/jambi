defmodule JambiPhoenixWeb.PageController do
  use JambiPhoenixWeb, :controller
  alias JambiPhoenix.PageGenerator
  alias JambiPhoenix.Pages

  def home(conn, _params) do
    render(conn, :home)
  end

  # Browser actions
  def index(conn, _params) do
    {:ok, pages} = Pages.list_pages()
    render(conn, :index, pages: pages)
  end

  def new(conn, _params) do
    changeset = JambiPhoenix.Pages.Page.changeset(%JambiPhoenix.Pages.Page{}, %{})
    render(conn, :new, changeset: changeset)
  end

  def create(conn, %{"page" => page_params}) do
    case Pages.create_page(page_params) do
      {:ok, page} ->
        conn
        |> put_flash(:info, "Page created successfully")
        |> redirect(to: "/pages/#{page.page_id}")

      {:error, %Ecto.Changeset{} = changeset} ->
        render(conn, :new, changeset: changeset)

      {:error, reason} ->
        conn
        |> put_flash(:error, "Failed to create page: #{reason}")
        |> redirect(to: "/pages/new")
    end
  end

  def show(conn, %{"id" => id}) do
    case Pages.get_page(id) do
      {:ok, page} ->
        render(conn, :show, page: page)

      {:error, :not_found} ->
        conn
        |> put_flash(:error, "Page not found")
        |> redirect(to: "/pages")

      {:error, reason} ->
        conn
        |> put_flash(:error, "Failed to load page: #{reason}")
        |> redirect(to: "/pages")
    end
  end

  def edit(conn, %{"id" => id}) do
    case Pages.get_page(id) do
      {:ok, page} ->
        changeset = JambiPhoenix.Pages.Page.changeset(page, %{})
        render(conn, :edit, page: page, changeset: changeset)

      {:error, :not_found} ->
        conn
        |> put_flash(:error, "Page not found")
        |> redirect(to: "/pages")

      {:error, reason} ->
        conn
        |> put_flash(:error, "Failed to load page: #{reason}")
        |> redirect(to: "/pages")
    end
  end

  def update(conn, %{"id" => id, "page" => page_params}) do
    case Pages.update_page(id, page_params) do
      {:ok, page} ->
        conn
        |> put_flash(:info, "Page updated successfully")
        |> redirect(to: "/pages/#{page.page_id}")

      {:error, %Ecto.Changeset{} = changeset} ->
        render(conn, :edit, changeset: changeset)

      {:error, reason} ->
        conn
        |> put_flash(:error, "Failed to update page: #{reason}")
        |> redirect(to: "/pages/#{id}/edit")
    end
  end

  def delete(conn, %{"id" => id}) do
    case Pages.delete_page(id) do
      {:ok, _page} ->
        conn
        |> put_flash(:info, "Page deleted successfully")
        |> redirect(to: "/pages")

      {:error, reason} ->
        conn
        |> put_flash(:error, "Failed to delete page: #{reason}")
        |> redirect(to: "/pages")
    end
  end

  # API actions
  def api_index(conn, _params) do
    {:ok, pages} = Pages.list_pages()
    conn
    |> put_status(:ok)
    |> json(%{data: pages})
  end

  def generate_single(conn, %{
        "template_name" => template_name,
        "content" => content,
        "output_path" => output_path
      }) do
    # Parse content from JSON string to map
    content_map = Jason.decode!(content)

    result = PageGenerator.generate_page(template_name, content_map, output_path)

    case result do
      {:ok, path} ->
        conn
        |> put_status(:created)
        |> json(%{status: "success", message: "Page generated successfully", path: path})

      {:error, reason} ->
        conn
        |> put_status(:unprocessable_entity)
        |> json(%{status: "error", message: "Failed to generate page", reason: reason})
    end
  end

  def generate_all(conn, _params) do
    {:ok, results} = Pages.generate_all_pages()
    conn
    |> put_status(:ok)
    |> json(%{
      status: "success",
      message: "All pages generated successfully",
      results: results
    })
  end

  # Template management endpoints
  def list_templates(conn, _params) do
    # Get template folder from configuration
    template_dir = Application.get_env(:jambi_phoenix, :template_folder, "lib/jambi_phoenix_web/templates/static_page_view")

    case File.ls(template_dir) do
      {:ok, files} ->
        # Filter only .heex files and extract template names
        templates =
          files
          |> Enum.map(fn file ->
            case String.split(file, ".") do
              [name, "heex"] ->
                %{
                  name: name,
                  path: "#{template_dir}/#{file}"
                }
              _ ->
                nil
            end
          end)
          |> Enum.reject(&(&1 == nil))

        conn
        |> put_status(:ok)
        |> json(%{data: templates})

      {:error, reason} ->
        conn
        |> put_status(:internal_server_error)
        |> json(%{error: "Failed to list templates", reason: reason})
    end
  end

  def create_template(conn, %{"name" => name, "content" => content}) do
    template_dir = Application.get_env(:jambi_phoenix, :template_folder, "lib/jambi_phoenix_web/templates/static_page_view")
    template_path = Path.join(template_dir, "#{name}.heex")

    # Ensure templates directory exists
    File.mkdir_p!(template_dir)

    case File.write(template_path, content) do
      {:ok, _file} ->
        conn
        |> put_status(:created)
        |> json(%{
          status: "success",
          message: "Template created successfully",
          path: template_path
        })

      {:error, reason} ->
        conn
        |> put_status(:internal_server_error)
        |> json(%{status: "error", message: "Failed to create template", reason: reason})
    end
  end

  def get_template(conn, %{"name" => name}) do
    template_dir = Application.get_env(:jambi_phoenix, :template_folder, "lib/jambi_phoenix_web/templates/static_page_view")
    template_path = Path.join(template_dir, "#{name}.heex")

    case File.read(template_path) do
      {:ok, content} ->
        conn
        |> put_status(:ok)
        |> json(%{data: %{name: name, content: content}})

      {:error, reason} ->
        conn
        |> put_status(:not_found)
        |> json(%{error: "Template not found", reason: reason})
    end
  end

  def update_template(conn, %{"name" => name, "content" => content}) do
    template_dir = Application.get_env(:jambi_phoenix, :template_folder, "lib/jambi_phoenix_web/templates/static_page_view")
    template_path = Path.join(template_dir, "#{name}.heex")

    case File.read(template_path) do
      {:error, :enoent} ->
        conn
        |> put_status(:not_found)
        |> json(%{error: "Template not found"})

      {:ok, _existing_content} ->
        case File.write(template_path, content) do
          {:ok, _file} ->
            conn
            |> put_status(:ok)
            |> json(%{status: "success", message: "Template updated successfully"})

          {:error, reason} ->
            conn
            |> put_status(:internal_server_error)
            |> json(%{status: "error", message: "Failed to update template", reason: reason})
        end

      {:error, reason} ->
        conn
        |> put_status(:internal_server_error)
        |> json(%{error: "Failed to read template", reason: reason})
    end
  end

  def delete_template(conn, %{"name" => name}) do
    template_dir = Application.get_env(:jambi_phoenix, :template_folder, "lib/jambi_phoenix_web/templates/static_page_view")
    template_path = Path.join(template_dir, "#{name}.heex")

    case File.exists?(template_path) do
      true ->
        case File.rm(template_path) do
          :ok ->
            conn
            |> put_status(:ok)
            |> json(%{status: "success", message: "Template deleted successfully"})

          {:error, reason} ->
            conn
            |> put_status(:internal_server_error)
            |> json(%{status: "error", message: "Failed to delete template", reason: reason})
        end

      false ->
        conn
        |> put_status(:not_found)
        |> json(%{error: "Template not found"})
    end
  end
end
