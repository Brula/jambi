import sqlite3
from typing import List
from datetime import datetime
from datetime import datetime

from config.config import load_config
from repository.model.model import Page

def get_pages(table_name: str, database_connection_string: str) -> List[Page]:
    con = sqlite3.connect(database_connection_string)
    cursor = con.cursor()
    result = cursor.execute("SELECT title, content, file_name, template_name from " + table_name).fetchall()

    pages = []
    for page in result:
        pages.append(Page(title=page[0], content=page[1], file_name=page[2], template_name=page[3]))

    return pages

def create_page(title: str, content: str, template_name: str, file_name: str):
    config = load_config("dev")
    con = sqlite3.connect(config.database_connection_string)

    sql = '''INSERT INTO pages(title, content, template_name, file_name) VALUES(?,?,?,?) '''
    cursor = con.cursor()
    cursor.execute(sql, (title, content, template_name, file_name))
    con.commit()

    return cursor.lastrowid

def get_all_pages() -> List[Page]:
    """Get all pages from the database with their metadata.
    
    Returns:
        List[Page]: List of all pages in the database, or empty list if none exist
    """
    config = load_config("dev")
    con = sqlite3.connect(config.database_connection_string)
    cursor = con.cursor()
    try:
        result = cursor.execute("""
            SELECT page_id, title, content, template_name, file_name, 
                   created_at, updated_at 
            FROM pages 
            ORDER BY updated_at DESC
        """).fetchall()

        pages = []
        for page in result:
            pages.append(Page(
                page_id=page[0],
                title=page[1],
                content=page[2],
                template_name=page[3],
                file_name=page[4],
                created_at=datetime.fromisoformat(page[5]) if page[5] else None,
                updated_at=datetime.fromisoformat(page[6]) if page[6] else None
            ))

        return pages
    except sqlite3.OperationalError:
        # Table doesn't exist or other DB error
        return []
    finally:
        con.close()

def get_page_by_id(page_id: int) -> Page | None:
    """Get a single page by its page_id from the database.
    Args:
        page_id: The id of the page to fetch
    Returns:
        Page instance if found, else None
    """
    config = load_config("dev")
    con = sqlite3.connect(config.database_connection_string)
    cursor = con.cursor()
    try:
        result = cursor.execute(
            """
            SELECT page_id, title, content, template_name, file_name, created_at, updated_at
            FROM pages WHERE page_id = ?
            """, (page_id,)
        ).fetchone()
        if not result:
            return None
        return Page(
            page_id=result[0],
            title=result[1],
            content=result[2],
            template_name=result[3],
            file_name=result[4],
            created_at=datetime.fromisoformat(result[5]) if result[5] else None,
            updated_at=datetime.fromisoformat(result[6]) if result[6] else None
        )
    finally:
        con.close()

def delete_page_by_id(page_id: int) -> None:
    """Delete a page from the database by its page_id."""
    from config.config import load_config
    config = load_config("dev")
    con = sqlite3.connect(config.database_connection_string)
    cursor = con.cursor()
    cursor.execute("DELETE FROM pages WHERE page_id = ?", (page_id,))
    con.commit()
    con.close()

def update_page_by_id(page_id: int, title: str, content: str, template_name: str, file_name: str) -> None:
    """Update a page in the database by its page_id."""
    config = load_config("dev")
    con = sqlite3.connect(config.database_connection_string)
    cursor = con.cursor()
    cursor.execute(
        """
        UPDATE pages
        SET title = ?, content = ?, template_name = ?, file_name = ?, updated_at = CURRENT_TIMESTAMP
        WHERE page_id = ?
        """,
        (title, content, template_name, file_name, page_id)
    )
    con.commit()
    con.close()