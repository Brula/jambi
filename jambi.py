#!/usr/bin/env python3
import os
import shutil

from config.config import load_config
from rendering_engine.template_rendering import render_template
from repository.page_repository import get_pages

def build(env: str) -> None:
    current_config = load_config(env)
    pages = get_pages(current_config.pages_table_name, current_config.database_connection_string)
    output_folder = current_config.output_folder
    css_folder = output_folder + "/static"

    if os.path.exists(output_folder):
        shutil.rmtree(output_folder, ignore_errors=True)

    os.mkdir(output_folder)

    for page in pages:
        render_template(page.template_name + '.html', output_folder, current_config.template_folder, page)

    shutil.copytree(
        current_config.template_folder + '/assets',
        css_folder,
        symlinks=False,
        ignore=None,
        copy_function=shutil.copy2,
        ignore_dangling_symlinks=False,
        dirs_exist_ok=False
    )

if __name__ == "__main__":
    build("dev")
