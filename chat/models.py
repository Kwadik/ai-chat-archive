from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


def current_utc_iso() -> str:
    """Returns current UTC timestamp in ISO 8601 format."""
    return datetime.now(timezone.utc).isoformat()


@dataclass
class Message:
    number: int
    role: str  # "user" | "assistant" | "system"
    content: str
    file_name: str = ""
    created_at: str = field(default_factory=current_utc_iso)
    updated_at: str = field(default_factory=current_utc_iso)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if not self.file_name:
            self.file_name = f"{self.number:03d}-{self.role}.md"

    def to_dict(self) -> Dict[str, Any]:
        """Metadata representation for chat.json (excluding heavy content)."""
        return {
            "number": self.number,
            "role": self.role,
            "file_name": self.file_name,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any], content: str = "") -> "Message":
        return cls(
            number=data["number"],
            role=data["role"],
            content=content,
            file_name=data.get("file_name", f"{data['number']:03d}-{data['role']}.md"),
            created_at=data.get("created_at", current_utc_iso()),
            updated_at=data.get("updated_at", current_utc_iso()),
            metadata=data.get("metadata", {}),
        )


@dataclass
class Chat:
    id: str
    provider: str  # e.g., "chatgpt", "claude"
    title: str
    project_id: str
    created_at: str = field(default_factory=current_utc_iso)
    updated_at: str = field(default_factory=current_utc_iso)
    messages: List[Message] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Serializes chat metadata and message index for chat.json."""
        return {
            "id": self.id,
            "provider": self.provider,
            "title": self.title,
            "project_id": self.project_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "metadata": self.metadata,
            "messages": [msg.to_dict() for msg in self.messages],
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any], messages: Optional[List[Message]] = None) -> "Chat":
        return cls(
            id=data["id"],
            provider=data["provider"],
            title=data["title"],
            project_id=data["project_id"],
            created_at=data.get("created_at", current_utc_iso()),
            updated_at=data.get("updated_at", current_utc_iso()),
            messages=messages if messages is not None else [],
            metadata=data.get("metadata", {}),
        )


@dataclass
class Project:
    id: str
    name: str
    description: str = ""
    created_at: str = field(default_factory=current_utc_iso)
    updated_at: str = field(default_factory=current_utc_iso)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Project":
        return cls(
            id=data["id"],
            name=data["name"],
            description=data.get("description", ""),
            created_at=data.get("created_at", current_utc_iso()),
            updated_at=data.get("updated_at", current_utc_iso()),
        )