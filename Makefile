.PHONY: setup build serve test format lint precommit

# Install dependencies and setup assets
setup:
	mix setup

# Build static pages from database content using templates
build:
	mix run --no-halt

# Start the development server with auto-reload
serve:
	mix phx.server

# Run tests
test:
	mix test

# Format code
format:
	mix format

# Run linter (credential check)
lint:
	mix creds

# Run precommit checks (compile, format, test)
precommit:
	mix precommit

# Show available commands
help:
	@echo "Available commands:"
	@echo "  make setup        - Install dependencies and setup assets"
	@echo "  make build        - Build static pages from database"
	@echo "  make serve        - Start development server"
	@echo "  make test         - Run tests"
	@echo "  make format       - Format code"
	@echo "  make lint         - Run linter"
	@echo "  make precommit    - Run precommit checks"
