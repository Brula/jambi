from flask import Flask, send_from_directory, request

from repository.page_repository import create_page

app = Flask(__name__)

@app.route("/")
def index():
    return send_from_directory(path="index.html", directory="ui")

@app.get("/new")
def new_page_get():
    return send_from_directory(path="create.html", directory="ui")

@app.get("/edit")
def edit_page():
    # TODO: This should prefill the existing page content in the form.
    # To keep it simple, this should probably be a button on the index page
    return send_from_directory(path="create.html", directory="ui")

@app.post("/new")
def new_page_post(request):
    title = request.form.get('title')
    content = request.form.get('content')
    template_name = request.form.get('template_name')
    file_name = request.form.get('file_name')

    create_page(title=title, content=content, template_name=template_name, file_name=file_name)

    # TODO: - On startup create db if not exists
    # TODO: - Redirect to index if succeeded, show error when not
    # TODO: - Create form to make the request