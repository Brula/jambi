import sqlite3
from typing import List

from repository.model.model import Page

def get_pages() -> List[Page]:
    con = sqlite3.connect("database/data.db")
    cursor = con.cursor()
    result = cursor.execute("SELECT title, content, file_name from pages").fetchall()

    pages = []
    for page in result:
        pages.append(Page(title=page[0], content=page[1], file_name=page[2]))

    return pages