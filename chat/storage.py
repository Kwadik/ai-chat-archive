from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from .models import Chat, Message, Project, ensure_utc


class ProjectNotFoundError(FileNotFoundError):
    """Raised when a requested project does not exist."""


class ChatNotFoundError(FileNotFoundError):
    """Raised when a requested chat does not exist."""


class FileStorage:
    """
    Filesystem storage.

    Layout:

        projects/
        └── <project_id>/
            ├── project.json
            └── chats/
                └── <provider>/
                    └── <chat_id>/
                        ├── chat.json
                        ├── 001-user.md
                        ├── 002-assistant.md
                        └── ...
    """

    def __init__(self, projects_dir: str | Path) -> None:
        self.projects_dir = Path(projects_dir)

    # ------------------------------------------------------------------
    # Generic JSON helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _datetime_to_json(value: datetime) -> str:
        return ensure_utc(value).isoformat()

    @staticmethod
    def _datetime_from_json(value: str) -> datetime:
        parsed = datetime.fromisoformat(value)
        return ensure_utc(parsed)

    @staticmethod
    def _write_json(path: Path, data: dict[str, Any]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)

        path.write_text(
            json.dumps(
                data,
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

    @staticmethod
    def _read_json(path: Path) -> dict[str, Any]:
        return json.loads(path.read_text(encoding="utf-8"))

    # ------------------------------------------------------------------
    # Project paths
    # ------------------------------------------------------------------

    def get_project_dir(self, project_id: str) -> Path:
        return self.projects_dir / project_id

    def get_project_file(self, project_id: str) -> Path:
        return self.get_project_dir(project_id) / "project.json"

    def get_chats_dir(self, project_id: str) -> Path:
        return self.get_project_dir(project_id) / "chats"

    # ------------------------------------------------------------------
    # Project operations
    # ------------------------------------------------------------------

    def save_project(self, project: Project) -> None:
        project_dir = self.get_project_dir(project.id)
        project_dir.mkdir(parents=True, exist_ok=True)

        data = {
            "id": project.id,
            "name": project.name,
            "description": project.description,
            "root_path": project.root_path,
            "created_at": self._datetime_to_json(project.created_at),
            "updated_at": self._datetime_to_json(project.updated_at),
        }

        self._write_json(
            self.get_project_file(project.id),
            data,
        )

    def load_project(self, project_id: str) -> Project:
        path = self.get_project_file(project_id)

        if not path.exists():
            raise ProjectNotFoundError(
                f"Project not found: {project_id}"
            )

        data = self._read_json(path)

        return Project(
            id=data["id"],
            name=data["name"],
            description=data.get("description", ""),
            root_path=data.get("root_path", ""),
            created_at=self._datetime_from_json(data["created_at"]),
            updated_at=self._datetime_from_json(data["updated_at"]),
        )

    def list_projects(self) -> list[Project]:
        if not self.projects_dir.exists():
            return []

        projects: list[Project] = []

        for project_dir in sorted(self.projects_dir.iterdir()):
            if not project_dir.is_dir():
                continue

            project_file = project_dir / "project.json"

            if not project_file.exists():
                continue

            projects.append(
                self.load_project(project_dir.name)
            )

        return projects

    # ------------------------------------------------------------------
    # Chat paths
    # ------------------------------------------------------------------

    def get_chat_dir(
        self,
        project_id: str,
        provider: str,
        chat_id: str,
    ) -> Path:
        return (
            self.get_chats_dir(project_id)
            / provider
            / chat_id
        )

    def get_chat_file(
        self,
        project_id: str,
        provider: str,
        chat_id: str,
    ) -> Path:
        return self.get_chat_dir(
            project_id,
            provider,
            chat_id,
        ) / "chat.json"

    # ------------------------------------------------------------------
    # Chat operations
    # ------------------------------------------------------------------

    def save_chat(self, chat: Chat) -> None:
        """
        Save chat metadata and message Markdown files.

        The project must already exist.

        Existing message files are updated in place.
        Their original created_at is preserved when the same
        message number already exists.

        Existing orphan Markdown files are intentionally not deleted.
        """

        # Important:
        # Do not silently create a project here.
        self.load_project(chat.project_id)

        chat_dir = self.get_chat_dir(
            chat.project_id,
            chat.provider,
            chat.id,
        )
        chat_dir.mkdir(parents=True, exist_ok=True)

        existing_chat: Chat | None = None

        chat_file = chat_dir / "chat.json"

        if chat_file.exists():
            existing_chat = self.load_chat(
                chat.project_id,
                chat.provider,
                chat.id,
            )

        existing_messages: dict[int, Message] = {}

        if existing_chat is not None:
            existing_messages = {
                message.number: message
                for message in existing_chat.messages
            }

        # Save messages.
        for message in chat.messages:
            existing_message = existing_messages.get(
                message.number
            )

            if existing_message is not None:
                # Preserve creation time.
                message.created_at = existing_message.created_at

            message.updated_at = message.updated_at

            message_path = chat_dir / message.file_name

            message_path.write_text(
                message.content,
                encoding="utf-8",
            )

        # Save chat metadata/index.
        chat_data = {
            "id": chat.id,
            "provider": chat.provider,
            "title": chat.title,
            "project_id": chat.project_id,
            "created_at": self._datetime_to_json(chat.created_at),
            "updated_at": self._datetime_to_json(chat.updated_at),
            "metadata": chat.metadata,
            "messages": [
                {
                    "number": message.number,
                    "role": message.role,
                    "file_name": message.file_name,
                    "created_at": self._datetime_to_json(
                        message.created_at
                    ),
                    "updated_at": self._datetime_to_json(
                        message.updated_at
                    ),
                    "metadata": message.metadata,
                }
                for message in chat.messages
            ],
        }

        self._write_json(chat_file, chat_data)

    def load_chat(
        self,
        project_id: str,
        provider: str,
        chat_id: str,
    ) -> Chat:
        chat_file = self.get_chat_file(
            project_id,
            provider,
            chat_id,
        )

        if not chat_file.exists():
            raise ChatNotFoundError(
                f"Chat not found: "
                f"{project_id}/{provider}/{chat_id}"
            )

        data = self._read_json(chat_file)

        messages: list[Message] = []

        for message_data in data.get("messages", []):
            message_path = (
                chat_file.parent
                / message_data["file_name"]
            )

            content = ""

            if message_path.exists():
                content = message_path.read_text(
                    encoding="utf-8"
                )

            messages.append(
                Message(
                    number=message_data["number"],
                    role=message_data["role"],
                    content=content,
                    file_name=message_data["file_name"],
                    created_at=self._datetime_from_json(
                        message_data["created_at"]
                    ),
                    updated_at=self._datetime_from_json(
                        message_data["updated_at"]
                    ),
                    metadata=message_data.get(
                        "metadata",
                        {},
                    ),
                )
            )

        return Chat(
            id=data["id"],
            provider=data["provider"],
            title=data["title"],
            project_id=data["project_id"],
            created_at=self._datetime_from_json(
                data["created_at"]
            ),
            updated_at=self._datetime_from_json(
                data["updated_at"]
            ),
            messages=messages,
            metadata=data.get("metadata", {}),
        )

    # ------------------------------------------------------------------
    # Metadata filtering
    # ------------------------------------------------------------------

    def search_metadata(
        self,
        *,
        project_id: str | None = None,
        provider: str | None = None,
        chat_id: str | None = None,
        role: str | None = None,
        created_after: datetime | None = None,
        created_before: datetime | None = None,
    ) -> list[Chat]:
        """
        Search using JSON metadata only.

        Markdown content is not read during filtering.
        """

        results: list[Chat] = []

        if not self.projects_dir.exists():
            return results

        for project_dir in self.projects_dir.iterdir():
            if not project_dir.is_dir():
                continue

            current_project_id = project_dir.name

            if (
                project_id is not None
                and current_project_id != project_id
            ):
                continue

            chats_dir = project_dir / "chats"

            if not chats_dir.exists():
                continue

            for provider_dir in chats_dir.iterdir():
                if not provider_dir.is_dir():
                    continue

                current_provider = provider_dir.name

                if (
                    provider is not None
                    and current_provider != provider
                ):
                    continue

                for chat_dir in provider_dir.iterdir():
                    if not chat_dir.is_dir():
                        continue

                    current_chat_id = chat_dir.name

                    if (
                        chat_id is not None
                        and current_chat_id != chat_id
                    ):
                        continue

                    chat_file = chat_dir / "chat.json"

                    if not chat_file.exists():
                        continue

                    data = self._read_json(chat_file)

                    chat_created_at = (
                        self._datetime_from_json(
                            data["created_at"]
                        )
                    )

                    if (
                        created_after is not None
                        and chat_created_at < ensure_utc(
                            created_after
                        )
                    ):
                        continue

                    if (
                        created_before is not None
                        and chat_created_at > ensure_utc(
                            created_before
                        )
                    ):
                        continue

                    if role is not None:
                        message_roles = {
                            message.get("role")
                            for message in data.get(
                                "messages",
                                [],
                            )
                        }

                        if role not in message_roles:
                            continue

                    results.append(
                        self.load_chat(
                            current_project_id,
                            current_provider,
                            current_chat_id,
                        )
                    )

        return results