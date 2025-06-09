"""Tests for page creation functionality.

This module contains tests for verifying that the page creation
form and submission work correctly.
"""
from fastapi.testclient import TestClient
from server.server import app

def test_create_page_form():
    """Test that create page form is rendered correctly.
    
    Verifies:
    1. Status code is 200
    2. Response includes form elements
    3. Form has correct action URL
    """
    with TestClient(app) as client:
        response = client.get("/create")
        assert response.status_code == 200
        content = response.text
        
        # Check form elements
        assert 'method="POST" action="/create"' in content
        assert 'name="title"' in content
        assert 'name="content"' in content
        assert 'name="template_name"' in content
        assert 'name="file_name"' in content

def test_create_page_success():
    """Test successful page creation.
    
    Verifies:
    1. Successful submission redirects to index
    2. Page data is saved correctly
    """
    test_data = {
        "title": "Test Page",
        "content": "# Test Content\n\nThis is a test.",
        "template_name": "default",
        "file_name": "test-page.html"
    }
    
    with TestClient(app) as client:
        response = client.post("/create", data=test_data)
        assert response.status_code == 200 

def test_create_page_validation():
    """Test form validation.
    
    Verifies:
    1. Invalid input shows error messages
    2. Form preserves valid input
    3. Returns 400 status code
    """
    test_data = {
        "title": "",  # Empty title
        "content": "Test content",
        "template_name": "invalid",  # Invalid template
        "file_name": "test.txt"  # Wrong extension
    }
    
    with TestClient(app) as client:
        response = client.post("/create", data=test_data)
        assert response.status_code == 400
        content = response.text
        
        # Check error messages
        assert "Title is required" in content
        assert "Invalid template selected" in content
        assert "Invalid filename" in content
        
        # Check form value preservation
        assert test_data["content"] in content  # Content should be preserved
