from dataclasses import dataclass

@dataclass
class Page:
    title: str
    content: str
    file_name: str
    template_name: str
