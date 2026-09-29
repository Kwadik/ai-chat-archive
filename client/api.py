from __future__ import annotations

import json
from urllib.request import Request, urlopen


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