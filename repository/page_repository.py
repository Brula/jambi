import sqlite3
from typing import List

import config.config as config
from repository.model.model import Page

def get_pages() -> List[Page]:
    connection_string = config.current_config.database_connection_string
    con = sqlite3.connect(connection_string)
    cursor = con.cursor()
    result = cursor.execute("SELECT title, content, file_name, template_name from pages").fetchall()

    pages = []
    for page in result:
        pages.append(Page(title=page[0], content=page[1], file_name=page[2], template_name=page[3]))

    return pages