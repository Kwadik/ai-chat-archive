import threading

from chat.storage import FileStorage
from chat.models import Message, Chat, Project
from client.api import ApiClient
from server.http_server import create_server


def test_create_project(tmp_path):
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

        client = ApiClient(
            f"http://127.0.0.1:{server_port}"
        )

        result = client.create_project(
            id="project-1",
            name="Test Project",
        )

        assert result == {
            "id": "project-1",
            "name": "Test Project",
        }

        project = storage.load_project("project-1")

        assert project.name == "Test Project"

    finally:
        server.shutdown()
        server.server_close()
        thread.join()

def test_get_projects(tmp_path):
    storage = FileStorage(tmp_path / "projects")

    storage.save_project(
        Project(
            id="project-1",
            name="Project One",
        )
    )
    storage.save_project(
        Project(
            id="project-2",
            name="Project Two",
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

        client = ApiClient(
            f"http://127.0.0.1:{server_port}"
        )

        result = client.get_projects()

        assert result == [
            {
                "id": "project-1",
                "name": "Project One",
            },
            {
                "id": "project-2",
                "name": "Project Two",
            },
        ]

    finally:
        server.shutdown()
        server.server_close()
        thread.join()

def test_get_project(tmp_path):
    storage = FileStorage(tmp_path / "projects")

    storage.save_project(
        Project(
            id="project-1",
            name="Test Project",
            description="Project description",
            root_path="E:/Projects/test-project",
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

        client = ApiClient(
            f"http://127.0.0.1:{server_port}"
        )

        result = client.get_project("project-1")

        assert result == {
            "id": "project-1",
            "name": "Test Project",
            "description": "Project description",
            "root_path": "E:/Projects/test-project",
        }

    finally:
        server.shutdown()
        server.server_close()
        thread.join()

def test_create_chat(tmp_path):
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

        client = ApiClient(
            f"http://127.0.0.1:{server_port}"
        )

        result = client.create_chat(
            project_id="project-1",
            id="chat-1",
            provider="chatgpt",
            title="Test Chat",
            metadata={
                "url": "https://chatgpt.com/c/chat-1",
            },
        )

        assert result == {
            "id": "chat-1",
            "provider": "chatgpt",
            "title": "Test Chat",
        }

        chat = storage.load_chat(
            "project-1",
            "chatgpt",
            "chat-1",
        )

        assert chat.metadata == {
            "url": "https://chatgpt.com/c/chat-1",
        }

    finally:
        server.shutdown()
        server.server_close()
        thread.join()

def test_get_chats(tmp_path):
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

        client = ApiClient(
            f"http://127.0.0.1:{server_port}"
        )

        result = client.get_chats("project-1")

        assert result == [
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

def test_get_chat(tmp_path):
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
            metadata={
                "url": "https://chatgpt.com/c/chat-1",
            },
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

        client = ApiClient(
            f"http://127.0.0.1:{server_port}"
        )

        result = client.get_chat(
            project_id="project-1",
            provider="chatgpt",
            chat_id="chat-1",
        )

        assert result == {
            "id": "chat-1",
            "provider": "chatgpt",
            "title": "Test Chat",
            "project_id": "project-1",
            "metadata": {
                "url": "https://chatgpt.com/c/chat-1",
            },
            "messages": [
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
            ],
        }

    finally:
        server.shutdown()
        server.server_close()
        thread.join()

def test_create_message(tmp_path):
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

        client = ApiClient(
            f"http://127.0.0.1:{server_port}"
        )

        result = client.create_message(
            project_id="project-1",
            provider="chatgpt",
            chat_id="chat-1",
            role="assistant",
            content="Привет!\n\n# Ответ",
            metadata={
                "source": "manual-copy",
            },
        )

        assert result == {
            "number": 1,
            "role": "assistant",
            "file_name": "001-assistant.md",
        }

        chat = storage.load_chat(
            "project-1",
            "chatgpt",
            "chat-1",
        )

        assert len(chat.messages) == 1
        assert chat.messages[0].number == 1
        assert chat.messages[0].role == "assistant"
        assert chat.messages[0].content == (
            "Привет!\n\n# Ответ"
        )
        assert chat.messages[0].metadata == {
            "source": "manual-copy",
        }

    finally:
        server.shutdown()
        server.server_close()
        thread.join()