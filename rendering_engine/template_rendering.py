from jinja2 import Environment, FileSystemLoader
from markdown import markdown

from repository.model.model import Page

def render_template(template_name: str, output_folder: str, page: Page) -> None:
    env = Environment(
        loader=FileSystemLoader(searchpath="./templates"),
        autoescape=False
    )

    content_as_html = markdown(page.content)
    template = env.get_template(template_name)
    output = template.render(page_title=page.title, content=content_as_html)
    return _output_to_file(file_name=page.file_name, output=output, output_folder=output_folder)

def _output_to_file(file_name: str, output: str, output_folder: str) -> None:
    output_file = open(output_folder + "/" + file_name + ".html", "w")
    output_file.write(output)
    return output_file.close()