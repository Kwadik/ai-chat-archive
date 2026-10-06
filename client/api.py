from __future__ import annotations

import json
from urllib.request import Request, urlopen
from urllib.parse import urlencode
from chat.models import Chat, Message, Project, SearchResult


class ApiClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    def get_projects(self) -> list[dict]:
        request = Request(
            f"{self.base_url}/projects",
            method="GET",
        )

        with urlopen(request) as response:
            return json.loads(
                response.read().decode("utf-8")
            )

    def get_project(self, project_id: str) -> dict:
        request = Request(
            f"{self.base_url}/projects/{project_id}",
            method="GET",
        )

        with urlopen(request) as response:
            return json.loads(
                response.read().decode("utf-8")
            )

    def create_project(
        self,
        *,
        id: str,
        name: str,
    ) -> dict:
        payload = {
            "id": id,
            "name": name,
        }

        request = Request(
            f"{self.base_url}/projects",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
            },
            method="POST",
        )

        with urlopen(request) as response:
            return json.loads(
                response.read().decode("utf-8")
            )

    def get_chats(self, project_id: str) -> list[dict]:
        request = Request(
            f"{self.base_url}/projects/{project_id}/chats",
            method="GET",
        )

        with urlopen(request) as response:
            return json.loads(
                response.read().decode("utf-8")
            )

    def get_chat(
        self,
        *,
        project_id: str,
        provider: str,
        chat_id: str,
    ) -> dict:
        request = Request(
            f"{self.base_url}/projects/"
            f"{project_id}/chats/"
            f"{provider}/{chat_id}",
            method="GET",
        )

        with urlopen(request) as response:
            return json.loads(
                response.read().decode("utf-8")
            )

    def create_chat(
        self,
        *,
        project_id: str,
        id: str,
        provider: str,
        title: str,
        metadata: dict | None = None,
    ) -> dict:
        payload = {
            "id": id,
            "provider": provider,
            "title": title,
        }

        if metadata is not None:
            payload["metadata"] = metadata

        request = Request(
            f"{self.base_url}/projects/{project_id}/chats",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
            },
            method="POST",
        )

        with urlopen(request) as response:
            return json.loads(
                response.read().decode("utf-8")
            )

    def create_message(
        self,
        *,
        project_id: str,
        provider: str,
        chat_id: str,
        role: str,
        content: str,
        metadata: dict | None = None,
    ) -> dict:
        payload = {
            "role": role,
            "content": content,
        }

        if metadata is not None:
            payload["metadata"] = metadata

        request = Request(
            f"{self.base_url}/projects/"
            f"{project_id}/chats/"
            f"{provider}/{chat_id}/messages",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
            },
            method="POST",
        )

        with urlopen(request) as response:
            return json.loads(
                response.read().decode("utf-8")
            )

    def update_message(
        self,
        project_id: str,
        provider: str,
        chat_id: str,
        number: int,
        *,
        role: str,
        content: str,
        metadata: dict | None = None,
    ) -> Message:
        path = (
            f"/projects/{project_id}/"
            f"chats/{provider}/{chat_id}/messages/{number}"
        )

        data = {
            "role": role,
            "content": content,
        }

        if metadata is not None:
            data["metadata"] = metadata

        request = Request(
            self.base_url + path,
            data=json.dumps(data).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
            },
            method="PUT",
        )

        with urlopen(request) as response:
            response_data = json.loads(
                response.read().decode("utf-8")
            )

        return Message(
            number=response_data["number"],
            role=response_data["role"],
            content=content,
            file_name=response_data["file_name"],
            metadata=response_data["metadata"],
        )

    def search(
        self,
        query: str,
        *,
        project_id: str | None = None,
        chat_id: str | None = None,
        role: str | None = None,
    ) -> list[SearchResult]:
        params = {
            "q": query,
        }

        if project_id is not None:
            params["project_id"] = project_id

        if chat_id is not None:
            params["chat_id"] = chat_id

        if role is not None:
            params["role"] = role

        query_string = urlencode(params)

        request = Request(
            f"{self.base_url}/search?{query_string}",
            method="GET",
        )

        with urlopen(request) as response:
            data = json.loads(
                response.read().decode("utf-8")
            )

            return [
                SearchResult(
                    project=Project(
                        id=item["project"]["id"],
                        name=item["project"]["name"],
                    ),
                    chat=Chat(
                        id=item["chat"]["id"],
                        provider=item["chat"]["provider"],
                        title=item["chat"]["title"],
                        project_id=item["chat"]["project_id"],
                    ),
                    message=Message(
                        number=item["message"]["number"],
                        role=item["message"]["role"],
                        content=item["message"]["content"],
                        file_name=item["message"]["file_name"],
                    ),
                    provider=item["provider"],
                )
                for item in data
            ]