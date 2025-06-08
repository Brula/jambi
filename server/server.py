from fastapi import FastAPI
from typing import Union

from repository.page_repository import create_page

app = FastAPI()

@app.get("/")
async def root():
    return {"Hello": "Index page"}

@app.get("/new")
async def new_page_get():
    return {"Hello": "New page"}

@app.get("/edit")
async def edit_page():
    return {"Hello": "Edit page"}

@app.post("/new")
async def new_page_post(request):
    title = request.form.get('title')
    content = request.form.get('content')
    template_name = request.form.get('template_name')
    file_name = request.form.get('file_name')

    create_page(title=title, content=content, template_name=template_name, file_name=file_name)