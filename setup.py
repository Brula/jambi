import shutil
import subprocess
import venv


def setup() -> None:
    subprocess.run(["echo", "Setting up Jambi in the current directory"])

    subprocess.run(["echo", "Creating virtual environment .venv in current directory"])
    venv.create(".venv")
    subprocess.run(["sh", ".venv/bin/activate"])
    subprocess.run(["echo", "Created virtual environment .venv in current directory and activated for current shell"])

    subprocess.run(["echo", "Installing dependencies in current virtual environment using poetry"])
    subprocess.run(["poetry", "install"])
    subprocess.run(["echo", "Done installing dependencies through poetry"])

    subprocess.run(["echo", "Installing alembic to setup development database"])
    subprocess.run(["pip", "install", "alembic"])

    subprocess.run(["echo", "Initializing development database"])
    subprocess.run(["mkdir", "dev_database"])
    subprocess.run(["touch", "dev_database/jambi.db"])
    subprocess.run(["echo", "Created database file jambi.db"])

    subprocess.run(["alembic", "init", "alembic"])

    subprocess.run(["echo", "Configuring alembic for local development"])
    subprocess.run(["rm", "alembic.ini"])
    shutil.copy("setup/alembic.ini", ".")
    shutil.copy("setup/663f52c96e7d_init_db_and_pages_table.py", "alembic/versions/")
    subprocess.run(["echo", "Configured alembic, running migration script to create tables"])

    subprocess.run(["alembic", "upgrade", "head"])
    subprocess.run(["echo", "Configuration completed successfully!"])


if __name__ == "__main__":
    setup()