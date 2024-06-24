#!/usr/bin/env python3
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

    subprocess.run(["echo", "Initializing development database"])
    subprocess.run(["mkdir", "dev_database"])
    subprocess.run(["touch", "dev_database/jambi.db"])
    subprocess.run(["echo", "Created database file jambi.db"])

    subprocess.run(["echo", "Creating database tables"])
    subprocess.run(["sqlite3", "dev_database/jambi.db", ".read setup/init.sql"])
    subprocess.run(["echo", "Successfully created database tables"])

    subprocess.run(["echo", "Configuration completed successfully!"])

if __name__ == "__main__":
    setup()