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

"""Serve the index page with list of all pages.

Args:
    request: The FastAPI request object
    
Returns:
    TemplateResponse: Rendered index page with list of pages
"""
@app.get("/", response_model=None)
async def root(request: Request) -> Response:
    pages: List[Page] = get_all_pages()
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "page_title": "Jambi CMS",
            "pages": pages
        }
    )

"""Show the create/edit page form.

If page_id is provided, prefills the form with existing page data.

Args:
    request: The FastAPI request object
    page_id: Optional page ID to edit existing page
    
Returns:
    Response: Rendered template response with the form
"""
@app.get("/create")
async def create_page_get(request: Request, page_id: int | None = None) -> Response:
    if page_id is not None:
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
        return render_page_form(
            request,
            form=form_data,
            edit_mode=True,
            page_id=page_id
        )
    return render_page_form(request, form={})

"""Validate that a filename contains only allowed characters and ends in .html.

Args:
    filename: The filename to validate
    
Returns:
    bool: True if filename is valid, False otherwise
"""
def validate_filename(filename: str) -> bool:
    pattern = r'^[a-zA-Z0-9\-]+\.html$'
    return bool(re.match(pattern, filename))

"""Validate form data for page creation/editing.

Args:
    title: The page title to validate
    content: The page content to validate
    template_name: The template name to validate
    file_name: The filename to validate
    
Returns:
    List[str]: List of validation error messages, empty if valid
"""
def validate_page_form(title: str, content: str, template_name: str, file_name: str) -> List[str]:
    errors = []
    if not title.strip():
        errors.append("Title is required")
    if not content.strip():
        errors.append("Content is required")
    if template_name not in ['default', 'infinite8']:
        errors.append("Invalid template selected")
    if not validate_filename(file_name):
        errors.append("Invalid filename. Use only letters, numbers, and hyphens, ending in .html")
    return errors

"""Render the page creation/editing form with optional error message.

Args:
    request: The FastAPI request object
    form: Dictionary containing form data to prefill
    error: Optional error message to display
    edit_mode: Whether the form is for editing (True) or creating (False)
    page_id: The ID of the page being edited (if edit_mode is True)
    status_code: HTTP status code to return with the response
    
Returns:
    Response: Rendered template response with the form
"""
def render_page_form(request: Request, form: dict, error: str | None = None, edit_mode: bool = False, page_id: int | None = None, status_code: int = 400) -> Response:
    context = {"form": form, "edit_mode": edit_mode}
    if error:
        context["error"] = error
    if page_id is not None:
        context["page_id"] = page_id
    return templates.TemplateResponse(
        request=request,
        name="create.html",
        context=context,
        status_code=status_code
    )

"""Handle both creation and editing of pages.

Args:
    request: The FastAPI request object
    title: The page title
    content: The page content (markdown)
    template_name: The template to use
    file_name: The output filename
    page_id: The page ID if editing, None if creating
    
Returns:
    RedirectResponse: Redirect to index on success
    TemplateResponse: Render form with error on failure
"""
async def handle_page_form(
    request: Request,
    title: str,
    content: str,
    template_name: str,
    file_name: str,
    page_id: int | None = None
) -> Response:
    is_edit_mode = page_id is not None

    # Add .html if no extension is present
    if not file_name.lower().endswith('.html') and '.' not in file_name:
        file_name = file_name + '.html'

    # Validate form
    errors = validate_page_form(title, content, template_name, file_name)
    if errors:
        return render_page_form(
            request,
            form={
                "title": title,
                "content": content,
                "template_name": template_name,
                "file_name": file_name.replace('.html', '') if file_name.endswith('.html') else file_name
            },
            error=" ".join(errors),
            edit_mode=is_edit_mode,
            page_id=page_id,
            status_code=400
        )

    try:
        if is_edit_mode:
            update_page_by_id(
                page_id=page_id,
                title=title,
                content=content,
                template_name=template_name,
                file_name=file_name
            )
        else:
            create_page(
                title=title,
                content=content,
                template_name=template_name,
                file_name=file_name
            )
        return RedirectResponse(url="/", status_code=303)
    except Exception as e:
        action_type = "update" if is_edit_mode else "create"
        return render_page_form(
            request,
            form={
                "title": title,
                "content": content,
                "template_name": template_name,
                "file_name": file_name.replace('.html', '') if file_name.endswith('.html') else file_name
            },
            error=f"Failed to {action_type} page: {str(e)}",
            edit_mode=is_edit_mode,
            page_id=page_id,
            status_code=500
        )

"""Handle creation or editing of a page via POST request.

If page_id is provided, updates the existing page.
If page_id is not provided, creates a new page.

Args:
    request: The FastAPI request object
    title: The page title from form data
    content: The page content from form data (markdown)
    template_name: The template name from form data
    file_name: The output filename from form data
    page_id: Optional page ID for editing existing pages
    
Returns:
    Response: Redirect to index on success, or rendered form with errors on failure
"""
@app.post("/create")
async def create_page_post(
    request: Request,
    title: str = Form(...),
    content: str = Form(...),
    template_name: str = Form(...),
    file_name: str = Form(...),
    page_id: int | None = Form(None)
) -> Response:
    return await handle_page_form(request, title, content, template_name, file_name, page_id)

"""Delete a page by its ID and redirect to the index page.

Args:
    page_id: The ID of the page to delete
    
Returns:
    RedirectResponse: Redirect to the index page after deletion
"""
@app.post("/delete/{page_id}")
async def delete_page(page_id: int) -> RedirectResponse:
    delete_page_by_id(page_id)
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)