# Jambi

Jambi is a headless CMS built with Elixir and Phoenix that makes it easy to create super fast static websites. Users can create their own templates using HEEx (HTML + Elixir) templates and add placeholders with curly brackets (`{ }`) to have Jambi fill in the content as configured in the database schema.

## Features

- **Page Management**: Create, edit, delete, and view pages through a web interface
- **Template System**: Use HEEx templates to define page layouts with dynamic content placeholders
- **Static Page Generation**: Generate static HTML pages from templates and content stored in the database
- **RESTful API**: Full API support for programmatic page and template management
- **SQLite Database**: Lightweight database for storing pages and content

## Getting Started

### Prerequisites

- Elixir 1.15 or later
- Erlang/OTP 24 or later
- Node.js (for asset compilation)

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd jambi
   ```

2. Install dependencies:
   ```bash
   mix setup
   ```

3. Set up the database:
   ```bash
   mix ecto.setup
   ```

### Running the Application

Start the Phoenix server:

```bash
mix phx.server
```

Or start it inside IEx for interactive development:

```bash
iex -S mix phx.server
```

Now you can visit [`localhost:4000`](http://localhost:4000) from your browser.

## Project Structure

- `lib/jambi_phoenix/` - Core application logic
  - `pages.ex` - Page context and business logic
  - `page_generator.ex` - Static page generation from templates
- `lib/jambi_phoenix_web/` - Web layer
  - `controllers/` - HTTP request handlers
  - `templates/static_page_view/` - HEEx templates for static page generation
- `config/` - Application configuration (Elixir-based)
- `priv/repo/migrations/` - Database migrations
- `test/` - Test suite

## Configuration

Configuration is managed through Elixir config files:

- `config/config.exs` - Base configuration
- `config/dev.exs` - Development-specific settings
- `config/test.exs` - Test environment settings
- `config/runtime.exs` - Runtime configuration (production)

Key configuration options:
- `output_folder` - Directory where generated static pages are saved
- `template_folder` - Directory containing HEEx templates for page generation
- Database connection settings

## Usage

### Creating Pages

Pages can be created through the web UI at `/pages/new` or via the API:

```bash
POST /api/pages
Content-Type: application/json

{
  "page": {
    "title": "My Page",
    "file_name": "my-page.html",
    "template_name": "base",
    "content": {
      "heading": "Welcome",
      "body": "<p>Content here</p>"
    }
  }
}
```

### Generating Static Pages

Generate a single page:
```bash
POST /api/generate/single
```

Generate all pages:
```bash
POST /api/generate/all
```

### Template Management

Templates are stored as HEEx files in `lib/jambi_phoenix_web/templates/static_page_view/`. Templates use Phoenix's HEEx syntax and can access content through assigns:

```heex
<div>
  <h1>{@title}</h1>
  <div>{@content}</div>
</div>
```

## API Endpoints

### Pages
- `GET /pages` - List all pages
- `GET /pages/:id` - Show a page
- `POST /pages` - Create a page
- `PATCH /pages/:id` - Update a page
- `DELETE /pages/:id` - Delete a page

### Generation
- `POST /api/generate/single` - Generate a single page
- `POST /api/generate/all` - Generate all pages

### Templates
- `GET /api/templates` - List all templates
- `GET /api/templates/:name` - Get a template
- `POST /api/templates` - Create a template
- `PATCH /api/templates/:name` - Update a template
- `DELETE /api/templates/:name` - Delete a template

## Testing

Run the test suite:

```bash
mix test
```

Run tests for a specific file:

```bash
mix test test/path/to/test.exs
```

Run pre-commit checks (format, compile, test):

```bash
mix precommit
```

## Development

### Code Style

- Follow Elixir formatting conventions (`mix format`)
- Use `mix precommit` before committing to ensure code quality
- See `AGENTS.md` for Phoenix-specific guidelines

### Architecture

The application follows Phoenix conventions:
- **Contexts**: Business logic organized in contexts (e.g., `JambiPhoenix.Pages`)
- **Controllers**: Handle HTTP requests and responses
- **Templates**: HEEx templates for rendering HTML
- **Database**: Ecto with SQLite for data persistence

## Production Deployment

For production deployment, see the [Phoenix deployment guides](https://hexdocs.pm/phoenix/deployment.html).

Key production considerations:
- Set `SECRET_KEY_BASE` environment variable
- Configure `PHX_HOST` and `PORT` environment variables
- Set `OUTPUT_FOLDER` and `TEMPLATE_FOLDER` if using custom paths
- Ensure database migrations are run

## Learn More

- [Phoenix Framework](https://www.phoenixframework.org/)
- [Phoenix Guides](https://hexdocs.pm/phoenix/overview.html)
- [Phoenix Documentation](https://hexdocs.pm/phoenix)
- [Elixir Forum - Phoenix](https://elixirforum.com/c/phoenix-forum)
