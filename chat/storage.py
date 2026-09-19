import json
from pathlib import Path
from typing import List, Optional, Tuple

from chat.models import Chat, Message, Project, current_utc_iso


class FileStorage:
    """
    File-based storage implementation following Option A:
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

    def __init__(self, projects_dir: Path | str):
        self.projects_dir = Path(projects_dir)
        self.projects_dir.mkdir(parents=True, exist_ok=True)

    # --- Project Management ---

    def get_project_dir(self, project_id: str) -> Path:
        return self.projects_dir / project_id

    def save_project(self, project: Project) -> Project:
        proj_dir = self.get_project_dir(project.id)
        proj_dir.mkdir(parents=True, exist_ok=True)

        proj_file = proj_dir / "project.json"
        if proj_file.exists():
            # Update updated_at if modified
            project.updated_at = current_utc_iso()

        with open(proj_file, "w", encoding="utf-8") as f:
            json.dump(project.to_dict(), f, ensure_ascii=False, indent=2)

        return project

    def load_project(self, project_id: str) -> Optional[Project]:
        proj_file = self.get_project_dir(project_id) / "project.json"
        if not proj_file.exists():
            return None

        with open(proj_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            return Project.from_dict(data)

    def list_projects(self) -> List[Project]:
        projects = []
        for p in self.projects_dir.iterdir():
            if p.is_dir():
                project = self.load_project(p.name)
                if project:
                    projects.append(project)
        return projects

    # --- Chat Storage & Synchronization ---

    def get_chat_dir(self, project_id: str, provider: str, chat_id: str) -> Path:
        return self.get_project_dir(project_id) / "chats" / provider.lower() / chat_id

    def save_chat(self, chat: Chat) -> Chat:
        """
        Saves or updates a chat without creating duplicates.
        Preserves original `created_at` timestamps for existing messages.
        Updates `updated_at` timestamps when content changes.
        """
        # Ensure parent project exists
        if not self.load_project(chat.project_id):
            self.save_project(Project(id=chat.project_id, name=chat.project_id))

        chat_dir = self.get_chat_dir(chat.project_id, chat.provider, chat.id)
        chat_dir.mkdir(parents=True, exist_ok=True)

        existing_chat = self.load_chat(chat.project_id, chat.provider, chat.id)
        existing_messages_by_num = (
            {m.number: m for m in existing_chat.messages} if existing_chat else {}
        )

        now = current_utc_iso()
        processed_messages: List[Message] = []

        for msg in chat.messages:
            existing_msg = existing_messages_by_num.get(msg.number)

            if existing_msg:
                # Keep initial created_at
                msg.created_at = existing_msg.created_at

                # Check if content or metadata changed
                if existing_msg.content != msg.content or existing_msg.metadata != msg.metadata:
                    msg.updated_at = now
                else:
                    msg.updated_at = existing_msg.updated_at
            else:
                # New message
                if not msg.created_at:
                    msg.created_at = now
                msg.updated_at = now

            # Ensure file_name is properly formatted
            if not msg.file_name:
                msg.file_name = f"{msg.number:03d}-{msg.role}.md"

            # Write Markdown file
            md_path = chat_dir / msg.file_name
            with open(md_path, "w", encoding="utf-8") as f:
                f.write(msg.content)

            processed_messages.append(msg)

        # Update chat meta
        if existing_chat:
            chat.created_at = existing_chat.created_at
            chat.updated_at = now
        else:
            if not chat.created_at:
                chat.created_at = now
            chat.updated_at = now

        chat.messages = processed_messages

        # Save metadata index chat.json
        chat_json_path = chat_dir / "chat.json"
        with open(chat_json_path, "w", encoding="utf-8") as f:
            json.dump(chat.to_dict(), f, ensure_ascii=False, indent=2)

        return chat

    def load_chat(self, project_id: str, provider: str, chat_id: str) -> Optional[Chat]:
        chat_dir = self.get_chat_dir(project_id, provider, chat_id)
        chat_json_path = chat_dir / "chat.json"

        if not chat_json_path.exists():
            return None

        with open(chat_json_path, "r", encoding="utf-8") as f:
            chat_data = json.load(f)

        messages = []
        for msg_meta in chat_data.get("messages", []):
            file_name = msg_meta.get("file_name", f"{msg_meta['number']:03d}-{msg_meta['role']}.md")
            md_path = chat_dir / file_name
            content = ""
            if md_path.exists():
                with open(md_path, "r", encoding="utf-8") as f:
                    content = f.read()

            msg = Message.from_dict(msg_meta, content=content)
            messages.append(msg)

        return Chat.from_dict(chat_data, messages=messages)

    # --- Cross-Project Search Helper ---

    def search_metadata(
        self,
        query: Optional[str] = None,
        project_id: Optional[str] = None,
        provider: Optional[str] = None,
    ) -> List[Tuple[str, Chat]]:
        """
        Scans metadata across all projects without reading markdown files.
        Demonstrates that Option A still allows instant global searching.
        """
        results = []
        target_projects = [project_id] if project_id else [p.name for p in self.projects_dir.iterdir() if p.is_dir()]

        for p_id in target_projects:
            chats_base = self.get_project_dir(p_id) / "chats"
            if not chats_base.exists():
                continue

            for prov_dir in chats_base.iterdir():
                if not prov_dir.is_dir():
                    continue
                if provider and prov_dir.name != provider.lower():
                    continue

                for c_dir in prov_dir.iterdir():
                    chat_json = c_dir / "chat.json"
                    if chat_json.exists():
                        with open(chat_json, "r", encoding="utf-8") as f:
                            data = json.load(f)
                            chat = Chat.from_dict(data)

                            if query:
                                if query.lower() in chat.title.lower():
                                    results.append((p_id, chat))
                            else:
                                results.append((p_id, chat))

        return results