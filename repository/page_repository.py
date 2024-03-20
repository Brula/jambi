import sqlite3
from typing import List

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