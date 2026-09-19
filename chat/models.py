from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass
class Project:
    id: str
    name: str
    root_path: Path


@dataclass
class Chat:
    id: str
    provider: str
    title: str
    project_id: str


@dataclass
class Message:
    number: int
    role: str
    content: str
    created_at: datetime | None = None
    file: str | None = None
