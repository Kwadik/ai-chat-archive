from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


def utc_now() -> datetime:
    """Return current timezone-aware UTC datetime."""
    return datetime.now(timezone.utc)


def ensure_utc(value: datetime) -> datetime:
    """Normalize a datetime to timezone-aware UTC."""
    if value.tzinfo is None:
        raise ValueError("Datetime must be timezone-aware")

    return value.astimezone(timezone.utc)


@dataclass
class Message:
    """
    One logical message.

    The message content is stored as a separate Markdown file.
    """

    number: int
    role: str
    content: str
    file_name: str = ""

    created_at: datetime = field(default_factory=utc_now)
    updated_at: datetime = field(default_factory=utc_now)

    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.created_at = ensure_utc(self.created_at)
        self.updated_at = ensure_utc(self.updated_at)

        if not self.file_name:
            self.file_name = f"{self.number:03d}-{self.role}.md"


@dataclass
class Chat:
    """
    A complete chat consisting of metadata and messages.
    """

    id: str
    provider: str
    title: str
    project_id: str

    created_at: datetime = field(default_factory=utc_now)
    updated_at: datetime = field(default_factory=utc_now)

    messages: list[Message] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.created_at = ensure_utc(self.created_at)
        self.updated_at = ensure_utc(self.updated_at)


@dataclass
class Project:
    """
    A project containing chats and project-level files.
    """

    id: str
    name: str

    description: str = ""
    root_path: str = ""

    created_at: datetime = field(default_factory=utc_now)
    updated_at: datetime = field(default_factory=utc_now)

    def __post_init__(self) -> None:
        self.created_at = ensure_utc(self.created_at)
        self.updated_at = ensure_utc(self.updated_at)