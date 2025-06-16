.PHONY: setup build typecheck serve test

# Install dependencies and initialize development database
install:
	poetry run -- ./setup.py

# Build static pages from database content using templates
build:
	poetry run -- ./jambi.py

# Run type checking with strict settings
typecheck:
	poetry run -- mypy --strict ./jambi.py

# Start the development server with auto-reload
serve:
	poetry run -- uvicorn server.server:app --reload

# Run tests using pytest
test:
	poetry run pytest

# Show available commands
help:
	@echo "Available commands:"
	@echo "  make install      - Install dependencies and initialize database"
	@echo "  make build      - Build static pages from database"
	@echo "  make typecheck  - Run type checking"
	@echo "  make serve      - Start development server"
	@echo "  make test       - Run tests"
