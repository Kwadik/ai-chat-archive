import json
from datetime import datetime
from pathlib import Path

from .models import Chat, Message, Project


class FileStorage:
    """File-based storage. Markdown files remain the source of message content."""

    def __init__(self, root: Path):
        self.root = Path(root)

    def save_project(self, project: Project) -> None:
        project_dir = self.root / "projects" / project.id
        project_dir.mkdir(parents=True, exist_ok=True)

        metadata = {
            "id": project.id,
            "name": project.name,
            "root_path": str(project.root_path),
        }

        self._write_json(project_dir / "project.json", metadata)

    def save_chat(self, chat: Chat) -> None:
        chat_dir = self.chat_dir(chat.provider, chat.id)
        chat_dir.mkdir(parents=True, exist_ok=True)

        (chat_dir / "title.txt").write_text(
            chat.title,
            encoding="utf-8",
        )

        metadata = {
            "id": chat.id,
            "provider": chat.provider,
            "project_id": chat.project_id,
            "title": chat.title,
            "messages": [],
        }

        existing = chat_dir / "chat.json"
        if existing.exists():
            current = json.loads(existing.read_text(encoding="utf-8"))
            metadata["messages"] = current.get("messages", [])

        self._write_json(existing, metadata)

    def save_message(self, chat: Chat, message: Message) -> None:
        chat_dir = self.chat_dir(chat.provider, chat.id)
        chat_dir.mkdir(parents=True, exist_ok=True)

        filename = message.file or self.message_filename(message)
        message_path = chat_dir / filename

        message_path.write_text(message.content, encoding="utf-8")

        metadata_path = chat_dir / "chat.json"
        if metadata_path.exists():
            metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        else:
            metadata = {
                "id": chat.id,
                "provider": chat.provider,
                "project_id": chat.project_id,
                "title": chat.title,
                "messages": [],
            }

        metadata["messages"] = [
            item
            for item in metadata.get("messages", [])
            if item.get("number") != message.number
        ]

        item = {
            "number": message.number,
            "role": message.role,
            "file": filename,
        }

        if message.created_at is not None:
            item["created_at"] = message.created_at.isoformat()

        metadata["messages"].append(item)
        metadata["messages"].sort(key=lambda value: value["number"])

        self._write_json(metadata_path, metadata)

    def load_message(self, chat: Chat, number: int) -> Message:
        metadata = self.load_chat_metadata(chat)
        item = next(
            item
            for item in metadata["messages"]
            if item["number"] == number
        )

        content = (
            self.chat_dir(chat.provider, chat.id) / item["file"]
        ).read_text(encoding="utf-8")

        created_at = item.get("created_at")
        return Message(
            number=item["number"],
            role=item["role"],
            content=content,
            created_at=datetime.fromisoformat(created_at)
            if created_at
            else None,
            file=item["file"],
        )

    def load_chat_metadata(self, chat: Chat) -> dict:
        path = self.chat_dir(chat.provider, chat.id) / "chat.json"
        return json.loads(path.read_text(encoding="utf-8"))

    def chat_dir(self, provider: str, chat_id: str) -> Path:
        return self.root / provider / chat_id

    @staticmethod
    def message_filename(message: Message) -> str:
        return f"{message.number:03d}-{message.role}.md"

    @staticmethod
    def _write_json(path: Path, data: dict) -> None:
        path.write_text(
            json.dumps(data, ensure_ascii=False, indent=4),
            encoding="utf-8",
        )
