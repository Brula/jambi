from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Page:
    title: str
    content: str
    file_name: str
    template_name: str
    page_id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
