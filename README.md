# Jambi

A basic static site generator fully built in Python.

## Local development

To use jambi in a local environment it needs a proper setup. Before we continue, make sure poetry is installed on your local machine.
If you don't have poetry installed yet, make sure to check out [poetry's official documentation](https://python-poetry.org/docs/) for instructions on how to install poetry locally.

### Configuring the setup
After installing poetry, you're ready to install jambi. To make sure it has everything it needs, run `make setup`.
This will install jambi and its dependencies in a new virtual environment on your local machine.
This will also make sure the development database is correctly initialised.

### Build your webpages
To build your pages, run `make build`. 
This will fetch your pages from the database and build them using the templates that are defined in the `templates` directory.
After building your webpages they can be found in the `output` directory.

### Testing
For testing we use pytest. The test directory structure mirrors the directory structure of the main application. We strive to test all codepaths in the python code by unit tests. To run all the tests in the test directory, run `make test`.

### Running locally

- `make typecheck` for typechecking
- `make serve` for starting the webserver

To see all available commands, run `make help`.
