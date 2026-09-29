from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Any

from chat.models import Chat, Message, Project
from chat.storage import (
    ChatNotFoundError,
    FileStorage,
    ProjectNotFoundError,
)


class RequestHandler(BaseHTTPRequestHandler):
    storage: FileStorage

    def do_GET(self) -> None:
        if self.path == "/projects":
            projects = self.storage.list_projects()

            response = [
                {
                    "id": project.id,
                    "name": project.name,
                }
                for project in projects
            ]

            response_body = json.dumps(
                response,
                ensure_ascii=False,
            ).encode("utf-8")

            self.send_response(200)
            self.send_header(
                "Content-Type",
                "application/json",
            )
            self.send_header(
                "Content-Length",
                str(len(response_body)),
            )
            self.end_headers()
            self.wfile.write(response_body)
            return

        prefix = "/projects/"
        suffix = "/chats"

        if self.path.startswith(prefix) and self.path.endswith(suffix):
            project_id = self.path[
                len(prefix):-len(suffix)
            ]

            try:
                chats = self.storage.list_chats(project_id)
            except ProjectNotFoundError:
                self.send_error(404)
                return

            response = [
                {
                    "id": chat.id,
                    "provider": chat.provider,
                    "title": chat.title,
                    "project_id": chat.project_id,
                }
                for chat in chats
            ]

            response_body = json.dumps(
                response,
                ensure_ascii=False,
            ).encode("utf-8")

            self.send_response(200)
            self.send_header(
                "Content-Type",
                "application/json",
            )
            self.send_header(
                "Content-Length",
                str(len(response_body)),
            )
            self.end_headers()
            self.wfile.write(response_body)
            return

        prefix = "/projects/"
        suffix = "/chats/"

        if self.path.startswith(prefix) and suffix in self.path:
            path = self.path[len(prefix):]
            project_id, chat_path = path.split(suffix, 1)

            parts = chat_path.split("/", 1)

            if len(parts) != 2:
                self.send_error(404)
                return

            provider, chat_id = parts

            try:
                chat = self.storage.load_chat(
                    project_id,
                    provider,
                    chat_id,
                )
            except ChatNotFoundError:
                self.send_error(404)
                return

            response = {
                "id": chat.id,
                "provider": chat.provider,
                "title": chat.title,
                "project_id": chat.project_id,
                "metadata": chat.metadata,
            }

            response_body = json.dumps(
                response,
                ensure_ascii=False,
            ).encode("utf-8")

            self.send_response(200)
            self.send_header(
                "Content-Type",
                "application/json",
            )
            self.send_header(
                "Content-Length",
                str(len(response_body)),
            )
            self.end_headers()
            self.wfile.write(response_body)
            return

        if self.path.startswith("/projects/"):
            project_id = self.path[len("/projects/"):]

            try:
                project = self.storage.load_project(project_id)
            except ProjectNotFoundError:
                self.send_error(404)
                return

            response = {
                "id": project.id,
                "name": project.name,
                "description": project.description,
                "root_path": project.root_path,
            }

            response_body = json.dumps(
                response,
                ensure_ascii=False,
            ).encode("utf-8")

            self.send_response(200)
            self.send_header(
                "Content-Type",
                "application/json",
            )
            self.send_header(
                "Content-Length",
                str(len(response_body)),
            )
            self.end_headers()
            self.wfile.write(response_body)
            return

        self.send_error(404)

    def do_POST(self) -> None:
        if self.path == "/projects":
            try:
                content_length = int(
                    self.headers.get("Content-Length", "0")
                )
                body = self.rfile.read(content_length)
                data: dict[str, Any] = json.loads(
                    body.decode("utf-8")
                )

                project = Project(
                    id=data["id"],
                    name=data["name"],
                    description=data.get("description", ""),
                    root_path=data.get("root_path", ""),
                )

                self.storage.save_project(project)

                response = {
                    "id": project.id,
                    "name": project.name,
                }

                response_body = json.dumps(
                    response,
                    ensure_ascii=False,
                ).encode("utf-8")

                self.send_response(201)
                self.send_header(
                    "Content-Type",
                    "application/json",
                )
                self.send_header(
                    "Content-Length",
                    str(len(response_body)),
                )
                self.end_headers()
                self.wfile.write(response_body)

            except (json.JSONDecodeError, KeyError, TypeError):
                self.send_error(400)

            return

        if self.path.startswith("/projects/") and self.path.endswith("/chats"):
            project_id = self.path[
                len("/projects/"):-len("/chats")
            ]

            try:
                content_length = int(
                    self.headers.get("Content-Length", "0")
                )
                body = self.rfile.read(content_length)
                data: dict[str, Any] = json.loads(
                    body.decode("utf-8")
                )

                chat = Chat(
                    id=data["id"],
                    provider=data["provider"],
                    title=data["title"],
                    project_id=project_id,
                    metadata=data.get("metadata", {}),
                )

                self.storage.save_chat(chat)

                response = {
                    "id": chat.id,
                    "provider": chat.provider,
                    "title": chat.title,
                }

                response_body = json.dumps(
                    response,
                    ensure_ascii=False,
                ).encode("utf-8")

                self.send_response(201)
                self.send_header(
                    "Content-Type",
                    "application/json",
                )
                self.send_header(
                    "Content-Length",
                    str(len(response_body)),
                )
                self.end_headers()
                self.wfile.write(response_body)
                return

            except ProjectNotFoundError:
                self.send_error(404)
                return
            except (
                json.JSONDecodeError,
                KeyError,
                TypeError,
            ):
                self.send_error(400)
                return

        prefix = "/projects/"
        marker = "/chats/"

        if self.path.startswith(prefix) and marker in self.path:
            path = self.path[len(prefix):]
            project_id, chat_path = path.split(marker, 1)

            parts = chat_path.split("/", 2)

            if len(parts) != 3 or parts[2] != "messages":
                self.send_error(404)
                return

            provider, chat_id, _ = parts

            try:
                content_length = int(
                    self.headers.get("Content-Length", "0")
                )
                body = self.rfile.read(content_length)
                data: dict[str, Any] = json.loads(
                    body.decode("utf-8")
                )

                message = Message(
                    number=0,
                    role=data["role"],
                    content=data["content"],
                    metadata=data.get("metadata", {}),
                )

                self.storage.save_message(
                    project_id,
                    provider,
                    chat_id,
                    message,
                )

                response = {
                    "number": message.number,
                    "role": message.role,
                    "file_name": message.file_name,
                }

                response_body = json.dumps(
                    response,
                    ensure_ascii=False,
                ).encode("utf-8")

                self.send_response(201)
                self.send_header(
                    "Content-Type",
                    "application/json",
                )
                self.send_header(
                    "Content-Length",
                    str(len(response_body)),
                )
                self.end_headers()
                self.wfile.write(response_body)
                return

            except ChatNotFoundError:
                self.send_error(404)
                return
            except (
                json.JSONDecodeError,
                KeyError,
                TypeError,
            ):
                self.send_error(400)
                return

        self.send_error(404)
        return

    def log_message(
        self,
        format: str,
        *args: Any,
    ) -> None:
        return


def create_server(
    storage: FileStorage,
    *,
    host: str = "127.0.0.1",
    port: int = 0,
) -> HTTPServer:
    handler_class = type(
        "StorageRequestHandler",
        (RequestHandler,),
        {"storage": storage},
    )

    return HTTPServer(
        (host, port),
        handler_class,
    )