defmodule JambiPhoenix.Repo.Migrations.CreatePagesTable do
  use Ecto.Migration

  def change do
    create table(:pages) do
      add :title, :string, null: false
      add :content, :map, null: false
      add :file_name, :string, null: false
      add :template_name, :string, null: false

      timestamps(type: :naive_datetime)
    end

    create unique_index(:pages, [:file_name])
  end
end
