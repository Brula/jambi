
defmodule JambiPhoenixWeb.PageControllerTest do
  use JambiPhoenixWeb.ConnCase
  alias JambiPhoenix.Pages

  setup do
    # Create a test page
    page_params = %{
      "title" => "Test Page",
      "file_name" => "test.html",
      "template_name" => "base",
      "content" => %{
        "heading" => "Welcome to Test Page",
        "title" => "Test Page",
        "content" => "<p>This is a test page content.</p>"
      }
    }
    
    {:ok, page} = Pages.create_page(page_params)
    
    # Store page struct for cleanup
    on_exit(fn -> Pages.delete_page(page) end)
    
    :ok
  end

  test "generate_all endpoint works", %{conn: conn} do
    conn = post(conn, "/api/generate/all")
    
    assert response(conn, 200)
    response_body = json_response(conn, 200)
    
    assert response_body["status"] == "success"
    assert response_body["message"] == "All pages generated successfully"
    assert Map.has_key?(response_body, "results")
  end
end