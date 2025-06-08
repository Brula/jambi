from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Page:
    title: str
    content: str
    file_name: str
    template_name: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
