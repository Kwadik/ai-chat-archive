import pytest
import json
import threading
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from chat.models import Chat, Message, Project
from chat.storage import (
    FileStorage,
    ProjectNotFoundError,
)
from server.http_server import create_server


def test_create_project_via_http(tmp_path):
    storage = FileStorage(tmp_path / "projects")

    server = create_server(
        storage,
        host="127.0.0.1",
        port=0,
    )

    thread = threading.Thread(
        target=server.serve_forever,
        daemon=True,
    )
    thread.start()

    try:
        server_port = server.server_address[1]

        request = Request(
            f"http://127.0.0.1:{server_port}/projects",
            data=json.dumps(
                {
                    "id": "project-1",
                    "name": "Test Project",
                }
            ).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
            },
            method="POST",
        )

        with urlopen(request) as response:
            assert response.status == 201

        project = storage.load_project("project-1")

        assert project.id == "project-1"
        assert project.name == "Test Project"

    finally:
        server.shutdown()
        server.server_close()
        thread.join()

def test_create_project_via_http_rejects_invalid_data(tmp_path):
    storage = FileStorage(tmp_path / "projects")

    server = create_server(
        storage,
        host="127.0.0.1",
        port=0,
    )

    thread = threading.Thread(
        target=server.serve_forever,
        daemon=True,
    )
    thread.start()

    try:
        server_port = server.server_address[1]

        request = Request(
            f"http://127.0.0.1:{server_port}/projects",
            data=b'{"name": "Test Project"}',
            headers={
                "Content-Type": "application/json",
            },
            method="POST",
        )

        try:
            urlopen(request)
            assert False, "Expected HTTP 400"
        except Exception as exc:
            assert getattr(exc, "code", None) == 400

    finally:
        server.shutdown()
        server.server_close()
        thread.join()

def test_list_projects_via_http(tmp_path):
    storage = FileStorage(tmp_path / "projects")

    storage.save_project(
        Project(
            id="project-1",
            name="First Project",
        )
    )
    storage.save_project(
        Project(
            id="project-2",
            name="Second Project",
        )
    )

    server = create_server(
        storage,
        host="127.0.0.1",
        port=0,
    )

    thread = threading.Thread(
        target=server.serve_forever,
        daemon=True,
    )
    thread.start()

    try:
        server_port = server.server_address[1]

        with urlopen(
            f"http://127.0.0.1:{server_port}/projects"
        ) as response:
            assert response.status == 200

            data = json.loads(
                response.read().decode("utf-8")
            )

        assert data == [
            {
                "id": "project-1",
                "name": "First Project",
            },
            {
                "id": "project-2",
                "name": "Second Project",
            },
        ]

    finally:
        server.shutdown()
        server.server_close()
        thread.join()

def test_get_project_via_http(tmp_path):
    storage = FileStorage(tmp_path / "projects")

    storage.save_project(
        Project(
            id="project-1",
            name="Test Project",
            description="Project description",
            root_path="E:/Projects/test",
        )
    )

    server = create_server(
        storage,
        host="127.0.0.1",
        port=0,
    )

    thread = threading.Thread(
        target=server.serve_forever,
        daemon=True,
    )
    thread.start()

    try:
        server_port = server.server_address[1]

        with urlopen(
            f"http://127.0.0.1:{server_port}/projects/project-1"
        ) as response:
            assert response.status == 200

            data = json.loads(
                response.read().decode("utf-8")
            )

        assert data["id"] == "project-1"
        assert data["name"] == "Test Project"
        assert data["description"] == "Project description"
        assert data["root_path"] == "E:/Projects/test"

    finally:
        server.shutdown()
        server.server_close()
        thread.join()

def test_get_unknown_path_returns_404(tmp_path):
    storage = FileStorage(tmp_path / "projects")

    server = create_server(
        storage,
        host="127.0.0.1",
        port=0,
    )

    thread = threading.Thread(
        target=server.serve_forever,
        daemon=True,
    )
    thread.start()

    try:
        server_port = server.server_address[1]

        try:
            urlopen(
                f"http://127.0.0.1:{server_port}/unknown"
            )
            assert False, "Expected HTTP 404"
        except Exception as exc:
            assert getattr(exc, "code", None) == 404

    finally:
        server.shutdown()
        server.server_close()
        thread.join()

def test_create_chat_via_http(tmp_path):
    storage = FileStorage(tmp_path / "projects")

    storage.save_project(
        Project(
            id="project-1",
            name="Test Project",
        )
    )

    server = create_server(
        storage,
        host="127.0.0.1",
        port=0,
    )

    thread = threading.Thread(
        target=server.serve_forever,
        daemon=True,
    )
    thread.start()

    try:
        server_port = server.server_address[1]

        request = Request(
            f"http://127.0.0.1:{server_port}/projects/project-1/chats",
            data=json.dumps(
                {
                    "id": "chat-1",
                    "provider": "chatgpt",
                    "title": "Test Chat",
                }
            ).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
            },
            method="POST",
        )

        with urlopen(request) as response:
            assert response.status == 201

            data = json.loads(
                response.read().decode("utf-8")
            )

        assert data["id"] == "chat-1"
        assert data["provider"] == "chatgpt"
        assert data["title"] == "Test Chat"

        chat = storage.load_chat(
            "project-1",
            "chatgpt",
            "chat-1",
        )

        assert chat.id == "chat-1"
        assert chat.provider == "chatgpt"
        assert chat.title == "Test Chat"
        assert chat.project_id == "project-1"

    finally:
        server.shutdown()
        server.server_close()
        thread.join()

def test_get_chat_via_http(tmp_path):
    storage = FileStorage(tmp_path / "projects")

    storage.save_project(
        Project(
            id="project-1",
            name="Test Project",
        )
    )

    chat = Chat(
        id="chat-1",
        provider="chatgpt",
        title="Test Chat",
        project_id="project-1",
        metadata={
            "source": "manual",
        },
    )
    storage.save_chat(chat)

    server = create_server(
        storage,
        host="127.0.0.1",
        port=0,
    )

    thread = threading.Thread(
        target=server.serve_forever,
        daemon=True,
    )
    thread.start()

    try:
        server_port = server.server_address[1]

        with urlopen(
            "http://127.0.0.1:"
            f"{server_port}/projects/project-1/"
            "chats/chatgpt/chat-1"
        ) as response:
            assert response.status == 200

            data = json.loads(
                response.read().decode("utf-8")
            )

        assert data["id"] == "chat-1"
        assert data["provider"] == "chatgpt"
        assert data["title"] == "Test Chat"
        assert data["project_id"] == "project-1"
        assert data["metadata"] == {
            "source": "manual",
        }

    finally:
        server.shutdown()
        server.server_close()
        thread.join()

def test_create_message_via_http(tmp_path):
    storage = FileStorage(tmp_path / "projects")

    storage.save_project(
        Project(
            id="project-1",
            name="Test Project",
        )
    )

    storage.save_chat(
        Chat(
            id="chat-1",
            provider="chatgpt",
            title="Test Chat",
            project_id="project-1",
        )
    )

    server = create_server(
        storage,
        host="127.0.0.1",
        port=0,
    )

    thread = threading.Thread(
        target=server.serve_forever,
        daemon=True,
    )
    thread.start()

    try:
        server_port = server.server_address[1]

        request = Request(
            "http://127.0.0.1:"
            f"{server_port}/projects/project-1/"
            "chats/chatgpt/chat-1/messages",
            data=json.dumps(
                {
                    "role": "user",
                    "content": "# Hello\n\nTest message.",
                }
            ).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
            },
            method="POST",
        )

        with urlopen(request) as response:
            assert response.status == 201

            data = json.loads(
                response.read().decode("utf-8")
            )

        assert data["number"] == 1
        assert data["role"] == "user"
        assert data["file_name"] == "001-user.md"

        chat = storage.load_chat(
            "project-1",
            "chatgpt",
            "chat-1",
        )

        assert len(chat.messages) == 1
        assert chat.messages[0].number == 1
        assert chat.messages[0].role == "user"
        assert chat.messages[0].content == (
            "# Hello\n\nTest message."
        )

    finally:
        server.shutdown()
        server.server_close()
        thread.join()

def test_create_second_message_via_http(tmp_path):
    storage = FileStorage(tmp_path / "projects")

    storage.save_project(
        Project(
            id="project-1",
            name="Test Project",
        )
    )

    storage.save_chat(
        Chat(
            id="chat-1",
            provider="chatgpt",
            title="Test Chat",
            project_id="project-1",
        )
    )

    server = create_server(
        storage,
        host="127.0.0.1",
        port=0,
    )

    thread = threading.Thread(
        target=server.serve_forever,
        daemon=True,
    )
    thread.start()

    try:
        server_port = server.server_address[1]
        base_url = (
            "http://127.0.0.1:"
            f"{server_port}/projects/project-1/"
            "chats/chatgpt/chat-1/messages"
        )

        for role, content in [
            ("user", "First message"),
            ("assistant", "Second message"),
        ]:
            request = Request(
                base_url,
                data=json.dumps(
                    {
                        "role": role,
                        "content": content,
                    }
                ).encode("utf-8"),
                headers={
                    "Content-Type": "application/json",
                },
                method="POST",
            )

            with urlopen(request) as response:
                assert response.status == 201

        chat = storage.load_chat(
            "project-1",
            "chatgpt",
            "chat-1",
        )

        assert len(chat.messages) == 2

        assert chat.messages[0].number == 1
        assert chat.messages[0].file_name == "001-user.md"

        assert chat.messages[1].number == 2
        assert chat.messages[1].role == "assistant"
        assert chat.messages[1].file_name == "002-assistant.md"
        assert chat.messages[1].content == "Second message"

    finally:
        server.shutdown()
        server.server_close()
        thread.join()

def test_create_message_for_missing_chat_returns_404(tmp_path):
    storage = FileStorage(tmp_path / "projects")

    storage.save_project(
        Project(
            id="project-1",
            name="Test Project",
        )
    )

    server = create_server(
        storage,
        host="127.0.0.1",
        port=0,
    )

    thread = threading.Thread(
        target=server.serve_forever,
        daemon=True,
    )
    thread.start()

    try:
        server_port = server.server_address[1]

        request = Request(
            "http://127.0.0.1:"
            f"{server_port}/projects/project-1/"
            "chats/chatgpt/missing-chat/messages",
            data=json.dumps(
                {
                    "role": "user",
                    "content": "Test message",
                }
            ).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
            },
            method="POST",
        )

        try:
            urlopen(request)
            assert False, "Expected HTTP 404"
        except Exception as exc:
            assert getattr(exc, "code", None) == 404

    finally:
        server.shutdown()
        server.server_close()
        thread.join()

def test_create_chat_for_missing_project_returns_404(tmp_path):
    storage = FileStorage(tmp_path / "projects")

    server = create_server(
        storage,
        host="127.0.0.1",
        port=0,
    )

    thread = threading.Thread(
        target=server.serve_forever,
        daemon=True,
    )
    thread.start()

    try:
        server_port = server.server_address[1]

        request = Request(
            "http://127.0.0.1:"
            f"{server_port}/projects/missing-project/"
            "chats",
            data=json.dumps(
                {
                    "id": "chat-1",
                    "provider": "chatgpt",
                    "title": "Test Chat",
                }
            ).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
            },
            method="POST",
        )

        try:
            urlopen(request)
            assert False, "Expected HTTP 404"
        except Exception as exc:
            assert getattr(exc, "code", None) == 404

    finally:
        server.shutdown()
        server.server_close()
        thread.join()

def test_get_missing_project_returns_404(tmp_path):
    storage = FileStorage(tmp_path / "projects")

    server = create_server(
        storage,
        host="127.0.0.1",
        port=0,
    )

    thread = threading.Thread(
        target=server.serve_forever,
        daemon=True,
    )
    thread.start()

    try:
        server_port = server.server_address[1]

        try:
            urlopen(
                "http://127.0.0.1:"
                f"{server_port}/projects/missing-project"
            )
            assert False, "Expected HTTP 404"
        except Exception as exc:
            assert getattr(exc, "code", None) == 404

    finally:
        server.shutdown()
        server.server_close()
        thread.join()

def test_get_missing_chat_returns_404(tmp_path):
    storage = FileStorage(tmp_path / "projects")

    storage.save_project(
        Project(
            id="project-1",
            name="Test Project",
        )
    )

    server = create_server(
        storage,
        host="127.0.0.1",
        port=0,
    )

    thread = threading.Thread(
        target=server.serve_forever,
        daemon=True,
    )
    thread.start()

    try:
        server_port = server.server_address[1]

        try:
            urlopen(
                "http://127.0.0.1:"
                f"{server_port}/projects/project-1/"
                "chats/chatgpt/missing-chat"
            )
            assert False, "Expected HTTP 404"
        except Exception as exc:
            assert getattr(exc, "code", None) == 404

    finally:
        server.shutdown()
        server.server_close()
        thread.join()

def test_create_message_without_role_returns_400(tmp_path):
    storage = FileStorage(tmp_path / "projects")

    storage.save_project(
        Project(
            id="project-1",
            name="Test Project",
        )
    )

    storage.save_chat(
        Chat(
            id="chat-1",
            provider="chatgpt",
            title="Test Chat",
            project_id="project-1",
        )
    )

    server = create_server(
        storage,
        host="127.0.0.1",
        port=0,
    )

    thread = threading.Thread(
        target=server.serve_forever,
        daemon=True,
    )
    thread.start()

    try:
        server_port = server.server_address[1]

        request = Request(
            "http://127.0.0.1:"
            f"{server_port}/projects/project-1/"
            "chats/chatgpt/chat-1/messages",
            data=json.dumps(
                {
                    "content": "Hello",
                }
            ).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
            },
            method="POST",
        )

        try:
            urlopen(request)
            assert False, "Expected HTTP 400"
        except Exception as exc:
            assert getattr(exc, "code", None) == 400

    finally:
        server.shutdown()
        server.server_close()
        thread.join()

def test_create_message_preserves_unicode_markdown_via_http(tmp_path):
    storage = FileStorage(tmp_path / "projects")

    storage.save_project(
        Project(
            id="project-1",
            name="Test Project",
        )
    )

    storage.save_chat(
        Chat(
            id="chat-1",
            provider="chatgpt",
            title="Test Chat",
            project_id="project-1",
        )
    )

    server = create_server(
        storage,
        host="127.0.0.1",
        port=0,
    )

    thread = threading.Thread(
        target=server.serve_forever,
        daemon=True,
    )
    thread.start()

    try:
        server_port = server.server_address[1]

        content = (
            "# Привет 👋\n\n"
            "Это **Markdown** с русским текстом.\n\n"
            "```python\n"
            "print('hello')\n"
            "```\n"
        )

        request = Request(
            "http://127.0.0.1:"
            f"{server_port}/projects/project-1/"
            "chats/chatgpt/chat-1/messages",
            data=json.dumps(
                {
                    "role": "assistant",
                    "content": content,
                },
                ensure_ascii=False,
            ).encode("utf-8"),
            headers={
                "Content-Type": "application/json; charset=utf-8",
            },
            method="POST",
        )

        with urlopen(request) as response:
            assert response.status == 201

        chat = storage.load_chat(
            "project-1",
            "chatgpt",
            "chat-1",
        )

        assert chat.messages[0].content == content

    finally:
        server.shutdown()
        server.server_close()
        thread.join()

def test_list_chats_via_http(tmp_path):
    storage = FileStorage(tmp_path / "projects")

    storage.save_project(
        Project(
            id="project-1",
            name="Test Project",
        )
    )

    storage.save_chat(
        Chat(
            id="chat-1",
            provider="chatgpt",
            title="First Chat",
            project_id="project-1",
        )
    )

    storage.save_chat(
        Chat(
            id="chat-2",
            provider="chatgpt",
            title="Second Chat",
            project_id="project-1",
        )
    )

    server = create_server(
        storage,
        host="127.0.0.1",
        port=0,
    )

    thread = threading.Thread(
        target=server.serve_forever,
        daemon=True,
    )
    thread.start()

    try:
        server_port = server.server_address[1]

        with urlopen(
            "http://127.0.0.1:"
            f"{server_port}/projects/project-1/chats"
        ) as response:
            assert response.status == 200

            data = json.loads(
                response.read().decode("utf-8")
            )

        assert data == [
            {
                "id": "chat-1",
                "provider": "chatgpt",
                "title": "First Chat",
                "project_id": "project-1",
            },
            {
                "id": "chat-2",
                "provider": "chatgpt",
                "title": "Second Chat",
                "project_id": "project-1",
            },
        ]

    finally:
        server.shutdown()
        server.server_close()
        thread.join()

def test_list_chats_for_project_without_chats_returns_empty_list(
    tmp_path,
):
    storage = FileStorage(tmp_path / "projects")

    storage.save_project(
        Project(
            id="project-1",
            name="Test Project",
        )
    )

    server = create_server(
        storage,
        host="127.0.0.1",
        port=0,
    )

    thread = threading.Thread(
        target=server.serve_forever,
        daemon=True,
    )
    thread.start()

    try:
        server_port = server.server_address[1]

        with urlopen(
            "http://127.0.0.1:"
            f"{server_port}/projects/project-1/chats"
        ) as response:
            assert response.status == 200

            data = json.loads(
                response.read().decode("utf-8")
            )

        assert data == []

    finally:
        server.shutdown()
        server.server_close()
        thread.join()

def test_list_projects_when_empty_returns_empty_list(tmp_path):
    storage = FileStorage(tmp_path / "projects")

    server = create_server(
        storage,
        host="127.0.0.1",
        port=0,
    )

    thread = threading.Thread(
        target=server.serve_forever,
        daemon=True,
    )
    thread.start()

    try:
        server_port = server.server_address[1]

        with urlopen(
            f"http://127.0.0.1:{server_port}/projects"
        ) as response:
            assert response.status == 200

            data = json.loads(
                response.read().decode("utf-8")
            )

        assert data == []

    finally:
        server.shutdown()
        server.server_close()
        thread.join()

def test_list_chats_for_missing_project_returns_404(tmp_path):
    storage = FileStorage(tmp_path / "projects")

    server = create_server(
        storage,
        host="127.0.0.1",
        port=0,
    )

    thread = threading.Thread(
        target=server.serve_forever,
        daemon=True,
    )
    thread.start()

    try:
        server_port = server.server_address[1]

        with pytest.raises(HTTPError) as exc_info:
            urlopen(
                f"http://127.0.0.1:{server_port}"
                "/projects/missing-project/chats"
            )

        assert exc_info.value.code == 404

    finally:
        server.shutdown()
        server.server_close()
        thread.join()

def test_get_chat_returns_messages(tmp_path):
    storage = FileStorage(tmp_path / "projects")

    storage.save_project(
        Project(
            id="project-1",
            name="Test Project",
        )
    )

    storage.save_chat(
        Chat(
            id="chat-1",
            provider="chatgpt",
            title="Test Chat",
            project_id="project-1",
        )
    )

    storage.save_message(
        "project-1",
        "chatgpt",
        "chat-1",
        Message(
            number=1,
            role="user",
            content="# Hello\n\nWorld",
        ),
    )

    storage.save_message(
        "project-1",
        "chatgpt",
        "chat-1",
        Message(
            number=2,
            role="assistant",
            content="Привет!",
        ),
    )

    server = create_server(
        storage,
        host="127.0.0.1",
        port=0,
    )

    thread = threading.Thread(
        target=server.serve_forever,
        daemon=True,
    )
    thread.start()

    try:
        server_port = server.server_address[1]

        with urlopen(
            f"http://127.0.0.1:{server_port}"
            "/projects/project-1/chats/chatgpt/chat-1"
        ) as response:
            assert response.status == 200

            data = json.loads(
                response.read().decode("utf-8")
            )

        assert data["messages"] == [
            {
                "number": 1,
                "role": "user",
                "content": "# Hello\n\nWorld",
                "file_name": "001-user.md",
            },
            {
                "number": 2,
                "role": "assistant",
                "content": "Привет!",
                "file_name": "002-assistant.md",
            },
        ]

        assert "created_at" not in data["messages"][0]
        assert "updated_at" not in data["messages"][0]
        assert "metadata" not in data["messages"][0]

    finally:
        server.shutdown()
        server.server_close()
        thread.join()

def test_get_empty_chat_returns_empty_messages(tmp_path):
    storage = FileStorage(tmp_path / "projects")

    storage.save_project(
        Project(
            id="project-1",
            name="Test Project",
        )
    )

    storage.save_chat(
        Chat(
            id="chat-1",
            provider="chatgpt",
            title="Empty Chat",
            project_id="project-1",
        )
    )

    server = create_server(
        storage,
        host="127.0.0.1",
        port=0,
    )

    thread = threading.Thread(
        target=server.serve_forever,
        daemon=True,
    )
    thread.start()

    try:
        server_port = server.server_address[1]

        with urlopen(
            f"http://127.0.0.1:{server_port}"
            "/projects/project-1/chats/chatgpt/chat-1"
        ) as response:
            assert response.status == 200

            data = json.loads(
                response.read().decode("utf-8")
            )

        assert data["messages"] == []

    finally:
        server.shutdown()
        server.server_close()
        thread.join()

def test_create_chat_preserves_metadata(tmp_path):
    storage = FileStorage(tmp_path / "projects")

    storage.save_project(
        Project(
            id="project-1",
            name="Test Project",
        )
    )

    server = create_server(
        storage,
        host="127.0.0.1",
        port=0,
    )

    thread = threading.Thread(
        target=server.serve_forever,
        daemon=True,
    )
    thread.start()

    try:
        server_port = server.server_address[1]

        payload = {
            "id": "chat-1",
            "provider": "chatgpt",
            "title": "Test Chat",
            "metadata": {
                "url": "https://chatgpt.com/c/chat-1",
                "source": "manual",
            },
        }

        request = Request(
            f"http://127.0.0.1:{server_port}"
            "/projects/project-1/chats",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
            },
            method="POST",
        )

        with urlopen(request) as response:
            assert response.status == 201

        chat = storage.load_chat(
            "project-1",
            "chatgpt",
            "chat-1",
        )

        assert chat.metadata == {
            "url": "https://chatgpt.com/c/chat-1",
            "source": "manual",
        }

    finally:
        server.shutdown()
        server.server_close()
        thread.join()

def test_create_message_preserves_metadata(tmp_path):
    storage = FileStorage(tmp_path / "projects")

    storage.save_project(
        Project(
            id="project-1",
            name="Test Project",
        )
    )

    storage.save_chat(
        Chat(
            id="chat-1",
            provider="chatgpt",
            title="Test Chat",
            project_id="project-1",
        )
    )

    server = create_server(
        storage,
        host="127.0.0.1",
        port=0,
    )

    thread = threading.Thread(
        target=server.serve_forever,
        daemon=True,
    )
    thread.start()

    try:
        server_port = server.server_address[1]

        payload = {
            "role": "user",
            "content": "# Hello",
            "metadata": {
                "source": "manual-copy",
                "format": "markdown",
            },
        }

        request = Request(
            f"http://127.0.0.1:{server_port}"
            "/projects/project-1/chats/chatgpt/chat-1/messages",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
            },
            method="POST",
        )

        with urlopen(request) as response:
            assert response.status == 201

        chat = storage.load_chat(
            "project-1",
            "chatgpt",
            "chat-1",
        )

        assert chat.messages[0].metadata == {
            "source": "manual-copy",
            "format": "markdown",
        }

    finally:
        server.shutdown()
        server.server_close()
        thread.join()