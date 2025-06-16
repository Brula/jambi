"""Tests for index page routing and rendering.

This module contains tests for verifying that the index page
is properly served and shows the correct content.
"""
from fastapi.testclient import TestClient
from server.server import app

def test_index_page_render():
    """Test that index page is rendered correctly.
    
    Verifies:
    1. Status code is 200
    2. Response includes expected page title
    3. Response includes necessary page elements
    """
    with TestClient(app) as client:
        response = client.get("/")
        assert response.status_code == 200
        content = response.text
        
        # Check page elements
        assert "<title>Jambi CMS</title>" in content
        assert 'class="pages-list"' in content
        assert '<link rel="stylesheet" type="text/css" href="assets/style.css">' in content

def test_index_page_empty_list():
    """Test index page with no pages in database.
    
    Verifies empty state is handled properly.
    """
    from repository.page_repository import get_all_pages
    if get_all_pages():
        import pytest
        pytest.skip("Database is not empty, skipping empty list test.")
    with TestClient(app) as client:
        response = client.get("/")
        assert response.status_code == 200
        assert "No pages created yet" in response.text

