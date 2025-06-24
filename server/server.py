"""FastAPI server module for Jambi CMS.

This module provides the main web application and handles page
viewing, creation, and editing functionality.
"""
from fastapi import FastAPI, Request, Form, status
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import Response, RedirectResponse
from pathlib import Path
from typing import List
import re

from repository.page_repository import (
    create_page,
    get_all_pages,
    get_page_by_id,
    delete_page_by_id,
    update_page_by_id
)
from repository.model.model import Page

app = FastAPI(
    title="Jambi",
    description="A headless CMS for generating static websites"
)

# Mount static files
# Reason: Assets need to be served from /assets URL for frontend
app.mount("/assets", StaticFiles(directory=Path(__file__).parent / "ui" / "assets"), name="assets")

# Setup templates
# Reason: Templates are stored in the ui directory within the server package
templates = Jinja2Templates(directory=Path(__file__).parent / "ui")

@app.get("/", response_model=None)
async def root(request: Request) -> Response:
    """Serve the index page with list of all pages.
    
    Args:
        request: The FastAPI request object
        
    Returns:
        TemplateResponse: Rendered index page with list of pages
    """
    pages: List[Page] = get_all_pages()
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "page_title": "Jambi CMS",
            "pages": pages
        }
    )

@app.get("/create")
async def create_page_get(request: Request):
    """Show the create page form.
    
    Args:
        request: The FastAPI request object
        
    Returns:
        TemplateResponse: Rendered create page form
    """
    return templates.TemplateResponse(
        request=request,
        name="create.html",
        context={}
    )

def validate_filename(filename: str) -> bool:
    """Validate that a filename contains only allowed characters and ends in .html.
    
    Args:
        filename: The filename to validate
        
    Returns:
        bool: True if filename is valid, False otherwise
    """
    pattern = r'^[a-zA-Z0-9\-]+\.html$'
    return bool(re.match(pattern, filename))

@app.post("/create")
async def create_page_post(
    request: Request,
    title: str = Form(...),
    content: str = Form(...),
    template_name: str = Form(...),
    file_name: str = Form(...)
):
    """Handle creation of a new page.
    
    Args:
        request: The FastAPI request object
        title: The page title
        content: The page content (markdown)
        template_name: The template to use
        file_name: The output filename
        
    Returns:
        RedirectResponse: Redirect to index on success
        TemplateResponse: Render form with error on failure
    """
    # Add .html if no extension is present and doesn't already end with .html
    if not file_name.lower().endswith('.html') and '.' not in file_name:
        file_name = file_name + '.html'

    # Validate input
    errors = []
    if not title.strip():
        errors.append("Title is required")
    if not content.strip():
        errors.append("Content is required") 
    if template_name not in ['default', 'infinite8']:
        errors.append("Invalid template selected")
    if not validate_filename(file_name):
        errors.append("Invalid filename. Use only letters, numbers, and hyphens, ending in .html")

    if errors:
        return templates.TemplateResponse(
            request=request,
            name="create.html",
            context={
                "error": " ".join(errors),
                "form": {
                    "title": title,
                    "content": content,
                    "template_name": template_name,
                    "file_name": file_name
                }
            },
            status_code=400
        )

    try:
        # Create the page
        create_page(
            title=title,
            content=content,
            template_name=template_name,
            file_name=file_name
        )
        return RedirectResponse(url="/", status_code=303)
    except Exception as e:
        return templates.TemplateResponse(
            request=request,
            name="create.html",
            context={
                "error": "Failed to create page: " + str(e),
                "form": {
                    "title": title,
                    "content": content,
                    "template_name": template_name,
                    "file_name": file_name
                }
            },
            status_code=500
        )

@app.get("/edit/{page_id}")
async def edit_page_get(request: Request, page_id: int):
    """Show the create page form with existing content prefilled for editing."""
    page = get_page_by_id(page_id)
    if not page:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Page not found")
    form_data = {
        "title": page.title,
        "content": page.content,
        "template_name": page.template_name,
        "file_name": page.file_name.replace('.html', '') if page.file_name.endswith('.html') else page.file_name
    }
    return templates.TemplateResponse(
        request=request,
        name="create.html",
        context={"form": form_data, "edit_mode": True, "page_id": page_id}
    )

@app.post("/edit/{page_id}")
async def edit_page_post(
    request: Request,
    page_id: int,
    title: str = Form(...),
    content: str = Form(...),
    template_name: str = Form(...),
    file_name: str = Form(...)
):
    """Handle editing of an existing page."""
    # Add .html if no extension is present and doesn't already end with .html
    if not file_name.lower().endswith('.html') and '.' not in file_name:
        file_name = file_name + '.html'
    # Validate input
    errors = []
    if not title.strip():
        errors.append("Title is required")
    if not content.strip():
        errors.append("Content is required")
    if template_name not in ['default', 'infinite8']:
        errors.append("Invalid template selected")
    if not validate_filename(file_name):
        errors.append("Invalid filename. Use only letters, numbers, and hyphens, ending in .html")
    if errors:
        return templates.TemplateResponse(
            request=request,
            name="create.html",
            context={
                "error": " ".join(errors),
                "form": {
                    "title": title,
                    "content": content,
                    "template_name": template_name,
                    "file_name": file_name.replace('.html', '') if file_name.endswith('.html') else file_name
                },
                "edit_mode": True,
                "page_id": page_id
            },
            status_code=400
        )
    try:
        update_page_by_id(
            page_id=page_id,
            title=title,
            content=content,
            template_name=template_name,
            file_name=file_name
        )
        return RedirectResponse(url="/", status_code=303)
    except Exception as e:
        return templates.TemplateResponse(
            request=request,
            name="create.html",
            context={
                "error": "Failed to update page: " + str(e),
                "form": {
                    "title": title,
                    "content": content,
                    "template_name": template_name,
                    "file_name": file_name.replace('.html', '') if file_name.endswith('.html') else file_name
                },
                "edit_mode": True,
                "page_id": page_id
            },
            status_code=500
        )

@app.post("/delete/{page_id}")
async def delete_page(page_id: int):
    """Delete a page by its id and redirect to index."""
    delete_page_by_id(page_id)
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)