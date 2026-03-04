defmodule JambiPhoenix.Pages.Page do
  @moduledoc """
  The Page schema representing a website page.
  """

  use Ecto.Schema
  import Ecto.Changeset

  @primary_key {:page_id, :id, autogenerate: true}

  schema "pages" do
    field(:title, :string)
    field(:content, :map)
    field(:file_name, :string)
    field(:template_name, :string)

    timestamps(type: :naive_datetime)
  end

  @doc false
  def changeset(page, attrs) do
    page
    |> cast(attrs, [:title, :content, :file_name, :template_name])
    |> validate_required([:title, :content, :file_name, :template_name])
    |> validate_length(:title, min: 1, max: 255)
    |> validate_length(:file_name, min: 1, max: 255)
    |> validate_length(:template_name, min: 1, max: 255)
  end

  def change_page(page, attrs) do
    __MODULE__.changeset(page, attrs)
  end
end
