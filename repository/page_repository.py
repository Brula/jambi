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