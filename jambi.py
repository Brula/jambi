#!/usr/bin/env python3
from config.config import load_config
from rendering_engine.template_rendering import render_template
from repository.page_repository import get_pages

def build(env: str) -> None:
    load_config(env)
    pages = get_pages()
    for page in pages:
        render_template('infinite8.html', page)


if __name__ == "__main__":
    build("dev")
