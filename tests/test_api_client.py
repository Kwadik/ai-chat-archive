import threading

from chat.storage import FileStorage
from chat.models import Message, Chat, Project, SearchResult
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

def test_update_message(tmp_path):
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
            number=0,
            role="user",
            content="Original message",
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

        message = client.update_message(
            "project-1",
            "chatgpt",
            "chat-1",
            1,
            role="user",
            content="Edited message",
        )

        assert message.number == 1
        assert message.role == "user"
        assert message.content == "Edited message"
        assert message.file_name == "001-user.md"

        chat = storage.load_chat(
            "project-1",
            "chatgpt",
            "chat-1",
        )

        assert len(chat.messages) == 1
        assert chat.messages[0].content == "Edited message"

    finally:
        server.shutdown()
        server.server_close()
        thread.join()

def test_update_message_preserves_metadata(tmp_path):
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
            number=0,
            role="user",
            content="Original message",
            metadata={
                "source": "browser-extension",
                "external_id": "msg-123",
            },
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

        message = client.update_message(
            "project-1",
            "chatgpt",
            "chat-1",
            1,
            role="user",
            content="Edited message",
        )

        assert message.number == 1
        assert message.role == "user"
        assert message.content == "Edited message"
        assert message.file_name == "001-user.md"
        assert message.metadata == {
            "source": "browser-extension",
            "external_id": "msg-123",
        }

    finally:
        server.shutdown()
        server.server_close()
        thread.join()

def test_update_message_replaces_metadata(tmp_path):
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
            number=0,
            role="user",
            content="Original message",
            metadata={
                "source": "old",
            },
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

        message = client.update_message(
            "project-1",
            "chatgpt",
            "chat-1",
            1,
            role="user",
            content="Edited message",
            metadata={
                "source": "new",
                "external_id": "msg-456",
            },
        )

        assert message.metadata == {
            "source": "new",
            "external_id": "msg-456",
        }

        chat = storage.load_chat(
            "project-1",
            "chatgpt",
            "chat-1",
        )

        assert chat.messages[0].metadata == {
            "source": "new",
            "external_id": "msg-456",
        }

    finally:
        server.shutdown()
        server.server_close()
        thread.join()

def test_full_chat_workflow(tmp_path):
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
        client = ApiClient(
            f"http://127.0.0.1:{server.server_address[1]}"
        )

        project = client.create_project(
            id="project-1",
            name="Test Project",
        )

        assert project == {
            "id": "project-1",
            "name": "Test Project",
        }

        chat = client.create_chat(
            project_id="project-1",
            id="chat-1",
            provider="chatgpt",
            title="Test Chat",
            metadata={
                "url": "https://chatgpt.com/c/chat-1",
            },
        )

        assert chat == {
            "id": "chat-1",
            "provider": "chatgpt",
            "title": "Test Chat",
        }

        user_message = client.create_message(
            project_id="project-1",
            provider="chatgpt",
            chat_id="chat-1",
            role="user",
            content="# Hello",
        )

        assert user_message == {
            "number": 1,
            "role": "user",
            "file_name": "001-user.md",
        }

        assistant_message = client.create_message(
            project_id="project-1",
            provider="chatgpt",
            chat_id="chat-1",
            role="assistant",
            content="Привет!",
        )

        assert assistant_message == {
            "number": 2,
            "role": "assistant",
            "file_name": "002-assistant.md",
        }

        assert client.get_projects() == [
            {
                "id": "project-1",
                "name": "Test Project",
            }
        ]

        assert client.get_chats("project-1") == [
            {
                "id": "chat-1",
                "provider": "chatgpt",
                "title": "Test Chat",
                "project_id": "project-1",
            }
        ]

        assert client.get_chat(
            project_id="project-1",
            provider="chatgpt",
            chat_id="chat-1",
        ) == {
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
                    "content": "# Hello",
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

def test_search(tmp_path):
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
            content="How do I use Python?",
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

        result = client.search("python")

        assert len(result) == 1

        search_result = result[0]

        assert search_result.project.id == "project-1"
        assert search_result.project.name == "Test Project"

        assert search_result.chat.id == "chat-1"
        assert search_result.chat.provider == "chatgpt"
        assert search_result.chat.title == "Test Chat"
        assert search_result.chat.project_id == "project-1"

        assert search_result.message.number == 1
        assert search_result.message.role == "user"
        assert search_result.message.content == "How do I use Python?"
        assert search_result.message.file_name == "001-user.md"

        assert search_result.provider == "chatgpt"

    finally:
        server.shutdown()
        server.server_close()
        thread.join()

def test_search_handles_spaces(tmp_path):
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
            content="How does machine learning work?",
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

        result = client.search("machine learning")

        assert len(result) == 1

        search_result = result[0]

        assert search_result.project.id == "project-1"
        assert search_result.project.name == "Test Project"

        assert search_result.chat.id == "chat-1"
        assert search_result.chat.provider == "chatgpt"
        assert search_result.chat.title == "Test Chat"
        assert search_result.chat.project_id == "project-1"

        assert search_result.message.number == 1
        assert search_result.message.role == "user"
        assert search_result.message.content == (
            "How does machine learning work?"
        )
        assert search_result.message.file_name == "001-user.md"

        assert search_result.provider == "chatgpt"

    finally:
        server.shutdown()
        server.server_close()
        thread.join()

def test_search_with_project_id(tmp_path):
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

    storage.save_chat(
        Chat(
            id="chat-1",
            provider="chatgpt",
            title="Chat One",
            project_id="project-1",
        )
    )
    storage.save_chat(
        Chat(
            id="chat-2",
            provider="chatgpt",
            title="Chat Two",
            project_id="project-2",
        )
    )

    storage.save_message(
        "project-1",
        "chatgpt",
        "chat-1",
        Message(
            number=1,
            role="user",
            content="Python in project one",
        ),
    )

    storage.save_message(
        "project-2",
        "chatgpt",
        "chat-2",
        Message(
            number=1,
            role="user",
            content="Python in project two",
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

        result = client.search(
            "python",
            project_id="project-1",
        )

        assert len(result) == 1

        search_result = result[0]

        assert search_result.project.id == "project-1"
        assert search_result.project.name == "Project One"

        assert search_result.chat.id == "chat-1"
        assert search_result.chat.provider == "chatgpt"
        assert search_result.chat.title == "Chat One"
        assert search_result.chat.project_id == "project-1"

        assert search_result.message.number == 1
        assert search_result.message.role == "user"
        assert search_result.message.content == "Python in project one"
        assert search_result.message.file_name == "001-user.md"

        assert search_result.provider == "chatgpt"

    finally:
        server.shutdown()
        server.server_close()
        thread.join()

def test_search_with_chat_id(tmp_path):
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

    storage.save_chat(
        Chat(
            id="chat-1",
            provider="chatgpt",
            title="Chat One",
            project_id="project-1",
        )
    )
    storage.save_chat(
        Chat(
            id="chat-2",
            provider="chatgpt",
            title="Chat Two",
            project_id="project-2",
        )
    )

    storage.save_message(
        "project-1",
        "chatgpt",
        "chat-1",
        Message(
            number=1,
            role="user",
            content="Python in chat one",
        ),
    )

    storage.save_message(
        "project-2",
        "chatgpt",
        "chat-2",
        Message(
            number=1,
            role="user",
            content="Python in chat two",
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

        result = client.search(
            "python",
            chat_id="chat-1",
        )

        assert len(result) == 1

        search_result = result[0]

        assert search_result.project.id == "project-1"
        assert search_result.project.name == "Project One"

        assert search_result.chat.id == "chat-1"
        assert search_result.chat.provider == "chatgpt"
        assert search_result.chat.title == "Chat One"
        assert search_result.chat.project_id == "project-1"

        assert search_result.message.number == 1
        assert search_result.message.role == "user"
        assert search_result.message.content == "Python in chat one"
        assert search_result.message.file_name == "001-user.md"

        assert search_result.provider == "chatgpt"

    finally:
        server.shutdown()
        server.server_close()
        thread.join()

def test_search_with_role(tmp_path):
    storage = FileStorage(tmp_path / "projects")

    storage.save_project(
        Project(
            id="project-1",
            name="Project One",
        )
    )

    storage.save_chat(
        Chat(
            id="chat-1",
            provider="chatgpt",
            title="Chat One",
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
            content="Python from user",
        ),
    )

    storage.save_message(
        "project-1",
        "chatgpt",
        "chat-1",
        Message(
            number=2,
            role="assistant",
            content="Python from assistant",
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

        result = client.search(
            "python",
            role="assistant",
        )

        assert len(result) == 1

        search_result = result[0]

        assert search_result.project.id == "project-1"
        assert search_result.project.name == "Project One"

        assert search_result.chat.id == "chat-1"
        assert search_result.chat.provider == "chatgpt"
        assert search_result.chat.title == "Chat One"
        assert search_result.chat.project_id == "project-1"

        assert search_result.message.number == 2
        assert search_result.message.role == "assistant"
        assert search_result.message.content == "Python from assistant"
        assert search_result.message.file_name == "002-assistant.md"

        assert search_result.provider == "chatgpt"

    finally:
        server.shutdown()
        server.server_close()
        thread.join()

def test_search_with_combined_filters(tmp_path):
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

    storage.save_chat(
        Chat(
            id="chat-1",
            provider="chatgpt",
            title="Chat One",
            project_id="project-1",
        )
    )
    storage.save_chat(
        Chat(
            id="chat-2",
            provider="chatgpt",
            title="Chat Two",
            project_id="project-1",
        )
    )
    storage.save_chat(
        Chat(
            id="chat-3",
            provider="chatgpt",
            title="Chat Three",
            project_id="project-2",
        )
    )

    storage.save_message(
        "project-1",
        "chatgpt",
        "chat-1",
        Message(
            number=1,
            role="assistant",
            content="Python in target chat",
        ),
    )

    storage.save_message(
        "project-1",
        "chatgpt",
        "chat-2",
        Message(
            number=1,
            role="assistant",
            content="Python in another chat",
        ),
    )

    storage.save_message(
        "project-1",
        "chatgpt",
        "chat-1",
        Message(
            number=2,
            role="user",
            content="Python from user",
        ),
    )

    storage.save_message(
        "project-2",
        "chatgpt",
        "chat-3",
        Message(
            number=1,
            role="assistant",
            content="Python in another project",
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

        result = client.search(
            "python",
            project_id="project-1",
            chat_id="chat-1",
            role="assistant",
        )

        assert len(result) == 1

        search_result = result[0]

        assert search_result.project.id == "project-1"
        assert search_result.project.name == "Project One"

        assert search_result.chat.id == "chat-1"
        assert search_result.chat.provider == "chatgpt"
        assert search_result.chat.title == "Chat One"
        assert search_result.chat.project_id == "project-1"

        assert search_result.message.number == 1
        assert search_result.message.role == "assistant"
        assert search_result.message.content == "Python in target chat"
        assert search_result.message.file_name == "001-assistant.md"

        assert search_result.provider == "chatgpt"

    finally:
        server.shutdown()
        server.server_close()
        thread.join()

def test_search_with_empty_query(tmp_path):
    storage = FileStorage(tmp_path / "projects")

    storage.save_project(
        Project(
            id="project-1",
            name="Project One",
        )
    )

    storage.save_chat(
        Chat(
            id="chat-1",
            provider="chatgpt",
            title="Chat One",
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
            content="Some message",
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

        result = client.search("")

        assert result == []

    finally:
        server.shutdown()
        server.server_close()
        thread.join()

def test_search_with_empty_query_and_project_id(tmp_path):
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

    storage.save_chat(
        Chat(
            id="chat-1",
            provider="chatgpt",
            title="Chat One",
            project_id="project-1",
        )
    )
    storage.save_chat(
        Chat(
            id="chat-2",
            provider="chatgpt",
            title="Chat Two",
            project_id="project-2",
        )
    )

    storage.save_message(
        "project-1",
        "chatgpt",
        "chat-1",
        Message(
            number=1,
            role="user",
            content="Message one",
        ),
    )

    storage.save_message(
        "project-2",
        "chatgpt",
        "chat-2",
        Message(
            number=1,
            role="user",
            content="Message two",
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

        result = client.search(
            "",
            project_id="project-1",
        )

        assert len(result) == 1

        search_result = result[0]

        assert search_result.project.id == "project-1"
        assert search_result.project.name == "Project One"

        assert search_result.chat.id == "chat-1"
        assert search_result.chat.provider == "chatgpt"
        assert search_result.chat.title == "Chat One"
        assert search_result.chat.project_id == "project-1"

        assert search_result.message.number == 1
        assert search_result.message.role == "user"
        assert search_result.message.content == "Message one"
        assert search_result.message.file_name == "001-user.md"

        assert search_result.provider == "chatgpt"

    finally:
        server.shutdown()
        server.server_close()
        thread.join()

def test_search_with_empty_query_and_chat_id(tmp_path):
    storage = FileStorage(tmp_path / "projects")

    storage.save_project(
        Project(
            id="project-1",
            name="Project One",
        )
    )

    storage.save_chat(
        Chat(
            id="chat-1",
            provider="chatgpt",
            title="Chat One",
            project_id="project-1",
        )
    )
    storage.save_chat(
        Chat(
            id="chat-2",
            provider="chatgpt",
            title="Chat Two",
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
            content="Message one",
        ),
    )

    storage.save_message(
        "project-1",
        "chatgpt",
        "chat-2",
        Message(
            number=1,
            role="user",
            content="Message two",
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

        result = client.search(
            "",
            chat_id="chat-1",
        )

        assert len(result) == 1

        search_result = result[0]

        assert search_result.project.id == "project-1"
        assert search_result.project.name == "Project One"

        assert search_result.chat.id == "chat-1"
        assert search_result.chat.provider == "chatgpt"
        assert search_result.chat.title == "Chat One"
        assert search_result.chat.project_id == "project-1"

        assert search_result.message.number == 1
        assert search_result.message.role == "user"
        assert search_result.message.content == "Message one"
        assert search_result.message.file_name == "001-user.md"

        assert search_result.provider == "chatgpt"

    finally:
        server.shutdown()
        server.server_close()
        thread.join()

def test_search_with_empty_query_and_role(tmp_path):
    storage = FileStorage(tmp_path / "projects")

    storage.save_project(
        Project(
            id="project-1",
            name="Project One",
        )
    )

    storage.save_chat(
        Chat(
            id="chat-1",
            provider="chatgpt",
            title="Chat One",
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
            content="User message",
        ),
    )

    storage.save_message(
        "project-1",
        "chatgpt",
        "chat-1",
        Message(
            number=2,
            role="assistant",
            content="Assistant message",
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

        result = client.search(
            "",
            role="assistant",
        )

        assert len(result) == 1

        search_result = result[0]

        assert search_result.project.id == "project-1"
        assert search_result.project.name == "Project One"

        assert search_result.chat.id == "chat-1"
        assert search_result.chat.provider == "chatgpt"
        assert search_result.chat.title == "Chat One"
        assert search_result.chat.project_id == "project-1"

        assert search_result.message.number == 2
        assert search_result.message.role == "assistant"
        assert search_result.message.content == "Assistant message"
        assert search_result.message.file_name == "002-assistant.md"

        assert search_result.provider == "chatgpt"

    finally:
        server.shutdown()
        server.server_close()
        thread.join()

def test_search_handles_special_characters(tmp_path):
    storage = FileStorage(tmp_path / "projects")

    storage.save_project(
        Project(
            id="project-1",
            name="Project One",
        )
    )

    storage.save_chat(
        Chat(
            id="chat-1",
            provider="chatgpt",
            title="Chat One",
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
            content="I am learning C++",
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

        result = client.search("C++")

        assert len(result) == 1

        search_result = result[0]

        assert search_result.project.id == "project-1"
        assert search_result.project.name == "Project One"

        assert search_result.chat.id == "chat-1"
        assert search_result.chat.provider == "chatgpt"
        assert search_result.chat.title == "Chat One"
        assert search_result.chat.project_id == "project-1"

        assert search_result.message.number == 1
        assert search_result.message.role == "user"
        assert search_result.message.content == "I am learning C++"
        assert search_result.message.file_name == "001-user.md"

        assert search_result.provider == "chatgpt"

    finally:
        server.shutdown()
        server.server_close()
        thread.join()

def test_search_with_unknown_project_id(tmp_path):
    storage = FileStorage(tmp_path / "projects")

    storage.save_project(
        Project(
            id="project-1",
            name="Project One",
        )
    )

    storage.save_chat(
        Chat(
            id="chat-1",
            provider="chatgpt",
            title="Chat One",
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
            content="Python message",
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

        result = client.search(
            "python",
            project_id="unknown-project",
        )

        assert result == []

    finally:
        server.shutdown()
        server.server_close()
        thread.join()

def test_search_with_unknown_chat_id(tmp_path):
    storage = FileStorage(tmp_path / "projects")

    storage.save_project(
        Project(
            id="project-1",
            name="Project One",
        )
    )

    storage.save_chat(
        Chat(
            id="chat-1",
            provider="chatgpt",
            title="Chat One",
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
            content="Python message",
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

        result = client.search(
            "python",
            chat_id="unknown-chat",
        )

        assert result == []

    finally:
        server.shutdown()
        server.server_close()
        thread.join()

def test_search_with_unknown_role(tmp_path):
    storage = FileStorage(tmp_path / "projects")

    storage.save_project(
        Project(
            id="project-1",
            name="Project One",
        )
    )

    storage.save_chat(
        Chat(
            id="chat-1",
            provider="chatgpt",
            title="Chat One",
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
            content="Python message",
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

        result = client.search(
            "python",
            role="unknown-role",
        )

        assert result == []

    finally:
        server.shutdown()
        server.server_close()
        thread.join()

def test_search_preserves_message_order(tmp_path):
    storage = FileStorage(tmp_path / "projects")

    storage.save_project(
        Project(
            id="project-1",
            name="Project One",
        )
    )

    storage.save_chat(
        Chat(
            id="chat-1",
            provider="chatgpt",
            title="Chat One",
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
            content="Python first",
        ),
    )

    storage.save_message(
        "project-1",
        "chatgpt",
        "chat-1",
        Message(
            number=2,
            role="assistant",
            content="Python second",
        ),
    )

    storage.save_message(
        "project-1",
        "chatgpt",
        "chat-1",
        Message(
            number=3,
            role="user",
            content="Python third",
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

        result = client.search("python")

        assert len(result) == 3

        assert result[0].project.id == "project-1"
        assert result[0].project.name == "Project One"
        assert result[0].chat.id == "chat-1"
        assert result[0].chat.provider == "chatgpt"
        assert result[0].chat.title == "Chat One"
        assert result[0].chat.project_id == "project-1"
        assert result[0].message.number == 1
        assert result[0].message.role == "user"
        assert result[0].message.content == "Python first"
        assert result[0].message.file_name == "001-user.md"
        assert result[0].provider == "chatgpt"

        assert result[1].project.id == "project-1"
        assert result[1].project.name == "Project One"
        assert result[1].chat.id == "chat-1"
        assert result[1].chat.provider == "chatgpt"
        assert result[1].chat.title == "Chat One"
        assert result[1].chat.project_id == "project-1"
        assert result[1].message.number == 2
        assert result[1].message.role == "assistant"
        assert result[1].message.content == "Python second"
        assert result[1].message.file_name == "002-assistant.md"
        assert result[1].provider == "chatgpt"

        assert result[2].project.id == "project-1"
        assert result[2].project.name == "Project One"
        assert result[2].chat.id == "chat-1"
        assert result[2].chat.provider == "chatgpt"
        assert result[2].chat.title == "Chat One"
        assert result[2].chat.project_id == "project-1"
        assert result[2].message.number == 3
        assert result[2].message.role == "user"
        assert result[2].message.content == "Python third"
        assert result[2].message.file_name == "003-user.md"
        assert result[2].provider == "chatgpt"

    finally:
        server.shutdown()
        server.server_close()
        thread.join()

def test_search_returns_message_once_when_query_occurs_multiple_times(
    tmp_path,
):
    storage = FileStorage(tmp_path / "projects")

    storage.save_project(
        Project(
            id="project-1",
            name="Project One",
        )
    )

    storage.save_chat(
        Chat(
            id="chat-1",
            provider="chatgpt",
            title="Chat One",
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
            content="Python is useful. I use Python every day.",
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

        result = client.search("python")

        assert len(result) == 1

        search_result = result[0]

        assert search_result.project.id == "project-1"
        assert search_result.project.name == "Project One"

        assert search_result.chat.id == "chat-1"
        assert search_result.chat.provider == "chatgpt"
        assert search_result.chat.title == "Chat One"
        assert search_result.chat.project_id == "project-1"

        assert search_result.message.number == 1
        assert search_result.message.role == "user"
        assert search_result.message.content == (
            "Python is useful. I use Python every day."
        )
        assert search_result.message.file_name == "001-user.md"

        assert search_result.provider == "chatgpt"

    finally:
        server.shutdown()
        server.server_close()
        thread.join()

def test_search_is_case_insensitive(tmp_path):
    storage = FileStorage(tmp_path / "projects")

    storage.save_project(
        Project(
            id="project-1",
            name="Project One",
        )
    )

    storage.save_chat(
        Chat(
            id="chat-1",
            provider="chatgpt",
            title="Chat One",
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
            content="Python is useful",
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

        result = client.search("PYTHON")

        assert len(result) == 1

        search_result = result[0]

        assert search_result.project.id == "project-1"
        assert search_result.project.name == "Project One"

        assert search_result.chat.id == "chat-1"
        assert search_result.chat.provider == "chatgpt"
        assert search_result.chat.title == "Chat One"
        assert search_result.chat.project_id == "project-1"

        assert search_result.message.number == 1
        assert search_result.message.role == "user"
        assert search_result.message.content == "Python is useful"
        assert search_result.message.file_name == "001-user.md"

        assert search_result.provider == "chatgpt"

    finally:
        server.shutdown()
        server.server_close()
        thread.join()

def test_search_handles_unicode_query(tmp_path):
    storage = FileStorage(tmp_path / "projects")

    storage.save_project(
        Project(
            id="project-1",
            name="Project One",
        )
    )

    storage.save_chat(
        Chat(
            id="chat-1",
            provider="chatgpt",
            title="Chat One",
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
            content="Изучаю Python каждый день",
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

        result = client.search("изучаю")

        assert len(result) == 1

        search_result = result[0]

        assert search_result.project.id == "project-1"
        assert search_result.project.name == "Project One"

        assert search_result.chat.id == "chat-1"
        assert search_result.chat.provider == "chatgpt"
        assert search_result.chat.title == "Chat One"
        assert search_result.chat.project_id == "project-1"

        assert search_result.message.number == 1
        assert search_result.message.role == "user"
        assert search_result.message.content == "Изучаю Python каждый день"
        assert search_result.message.file_name == "001-user.md"

        assert search_result.provider == "chatgpt"

    finally:
        server.shutdown()
        server.server_close()
        thread.join()

def test_search_handles_unicode_query_with_spaces(tmp_path):
    storage = FileStorage(tmp_path / "projects")

    storage.save_project(
        Project(
            id="project-1",
            name="Project One",
        )
    )

    storage.save_chat(
        Chat(
            id="chat-1",
            provider="chatgpt",
            title="Chat One",
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
            content="Изучаю машинное обучение",
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

        result = client.search("машинное обучение")

        assert len(result) == 1

        search_result = result[0]

        assert search_result.project.id == "project-1"
        assert search_result.project.name == "Project One"

        assert search_result.chat.id == "chat-1"
        assert search_result.chat.provider == "chatgpt"
        assert search_result.chat.title == "Chat One"
        assert search_result.chat.project_id == "project-1"

        assert search_result.message.number == 1
        assert search_result.message.role == "user"
        assert search_result.message.content == "Изучаю машинное обучение"
        assert search_result.message.file_name == "001-user.md"

        assert search_result.provider == "chatgpt"

    finally:
        server.shutdown()
        server.server_close()
        thread.join()

def test_search_with_all_filters_and_spaces(tmp_path):
    storage = FileStorage(tmp_path / "projects")

    storage.save_project(
        Project(
            id="project-1",
            name="Project One",
        )
    )

    storage.save_chat(
        Chat(
            id="chat-1",
            provider="chatgpt",
            title="Chat One",
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
            content="Изучаю машинное обучение",
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

        result = client.search(
            "машинное обучение",
            project_id="project-1",
            chat_id="chat-1",
            role="user",
        )

        assert len(result) == 1

        search_result = result[0]

        assert search_result.project.id == "project-1"
        assert search_result.project.name == "Project One"

        assert search_result.chat.id == "chat-1"
        assert search_result.chat.provider == "chatgpt"
        assert search_result.chat.title == "Chat One"
        assert search_result.chat.project_id == "project-1"

        assert search_result.message.number == 1
        assert search_result.message.role == "user"
        assert search_result.message.content == "Изучаю машинное обучение"
        assert search_result.message.file_name == "001-user.md"

        assert search_result.provider == "chatgpt"

    finally:
        server.shutdown()
        server.server_close()
        thread.join()

def test_search_with_empty_project_id(tmp_path):
    storage = FileStorage(tmp_path / "projects")

    storage.save_project(
        Project(
            id="project-1",
            name="Project One",
        )
    )

    storage.save_chat(
        Chat(
            id="chat-1",
            provider="chatgpt",
            title="Chat One",
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
            content="Python message",
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

        result = client.search(
            "python",
            project_id="",
        )

        assert result == []

    finally:
        server.shutdown()
        server.server_close()
        thread.join()

def test_search_with_empty_chat_id(tmp_path):
    storage = FileStorage(tmp_path / "projects")

    storage.save_project(
        Project(
            id="project-1",
            name="Project One",
        )
    )

    storage.save_chat(
        Chat(
            id="chat-1",
            provider="chatgpt",
            title="Chat One",
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
            content="Python message",
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

        result = client.search(
            "python",
            chat_id="",
        )

        assert result == []

    finally:
        server.shutdown()
        server.server_close()
        thread.join()

def test_search_with_empty_role(tmp_path):
    storage = FileStorage(tmp_path / "projects")

    storage.save_project(
        Project(
            id="project-1",
            name="Project One",
        )
    )

    storage.save_chat(
        Chat(
            id="chat-1",
            provider="chatgpt",
            title="Chat One",
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
            content="Python message",
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

        result = client.search(
            "python",
            role="",
        )

        assert result == []

    finally:
        server.shutdown()
        server.server_close()
        thread.join()

def test_search_with_empty_query_and_no_filters(tmp_path):
    storage = FileStorage(tmp_path / "projects")

    storage.save_project(
        Project(
            id="project-1",
            name="Project One",
        )
    )

    storage.save_chat(
        Chat(
            id="chat-1",
            provider="chatgpt",
            title="Chat One",
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
            content="Python message",
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

        result = client.search("")

        assert result == []

    finally:
        server.shutdown()
        server.server_close()
        thread.join()

def test_search_with_empty_project_and_chat_ids(tmp_path):
    storage = FileStorage(tmp_path / "projects")

    storage.save_project(
        Project(
            id="project-1",
            name="Project One",
        )
    )

    storage.save_chat(
        Chat(
            id="chat-1",
            provider="chatgpt",
            title="Chat One",
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
            content="Python message",
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

        result = client.search(
            "python",
            project_id="",
            chat_id="",
        )

        assert result == []

    finally:
        server.shutdown()
        server.server_close()
        thread.join()

def test_search_with_all_empty_filters(tmp_path):
    storage = FileStorage(tmp_path / "projects")

    storage.save_project(
        Project(
            id="project-1",
            name="Project One",
        )
    )

    storage.save_chat(
        Chat(
            id="chat-1",
            provider="chatgpt",
            title="Chat One",
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
            content="Python message",
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

        result = client.search(
            "python",
            project_id="",
            chat_id="",
            role="",
        )

        assert result == []

    finally:
        server.shutdown()
        server.server_close()
        thread.join()

def test_search_with_role_containing_spaces(tmp_path):
    storage = FileStorage(tmp_path / "projects")

    storage.save_project(
        Project(
            id="project-1",
            name="Project One",
        )
    )

    storage.save_chat(
        Chat(
            id="chat-1",
            provider="chatgpt",
            title="Chat One",
            project_id="project-1",
        )
    )

    storage.save_message(
        "project-1",
        "chatgpt",
        "chat-1",
        Message(
            number=1,
            role="assistant ",
            content="Python message",
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

        result = client.search(
            "python",
            role="assistant ",
        )

        assert len(result) == 1
        assert result[0].message.role == "assistant "

    finally:
        server.shutdown()
        server.server_close()
        thread.join()

def test_search_preserves_leading_and_trailing_spaces_in_query(tmp_path):
    storage = FileStorage(tmp_path / "projects")

    storage.save_project(
        Project(
            id="project-1",
            name="Project One",
        )
    )

    storage.save_chat(
        Chat(
            id="chat-1",
            provider="chatgpt",
            title="Chat One",
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
            content="  Python  ",
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

        result = client.search(
            "  Python  ",
        )

        assert len(result) == 1
        assert result[0].message.content == "  Python  "

    finally:
        server.shutdown()
        server.server_close()
        thread.join()

def test_search_with_unicode_role(tmp_path):
    storage = FileStorage(tmp_path / "projects")

    storage.save_project(
        Project(
            id="project-1",
            name="Project One",
        )
    )

    storage.save_chat(
        Chat(
            id="chat-1",
            provider="chatgpt",
            title="Chat One",
            project_id="project-1",
        )
    )

    storage.save_message(
        "project-1",
        "chatgpt",
        "chat-1",
        Message(
            number=1,
            role="ассистент",
            content="Python message",
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

        result = client.search(
            "python",
            role="ассистент",
        )

        assert len(result) == 1
        assert result[0].message.role == "ассистент"

    finally:
        server.shutdown()
        server.server_close()
        thread.join()

def test_search_with_unicode_project_id(tmp_path):
    storage = FileStorage(tmp_path / "projects")

    storage.save_project(
        Project(
            id="проект-1",
            name="Project One",
        )
    )

    storage.save_chat(
        Chat(
            id="chat-1",
            provider="chatgpt",
            title="Chat One",
            project_id="проект-1",
        )
    )

    storage.save_message(
        "проект-1",
        "chatgpt",
        "chat-1",
        Message(
            number=1,
            role="user",
            content="Python message",
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

        result = client.search(
            "python",
            project_id="проект-1",
        )

        assert len(result) == 1
        assert result[0].message.content == "Python message"

    finally:
        server.shutdown()
        server.server_close()
        thread.join()

def test_search_with_unicode_chat_id(tmp_path):
    storage = FileStorage(tmp_path / "projects")

    storage.save_project(
        Project(
            id="project-1",
            name="Project One",
        )
    )

    storage.save_chat(
        Chat(
            id="чат-1",
            provider="chatgpt",
            title="Chat One",
            project_id="project-1",
        )
    )

    storage.save_message(
        "project-1",
        "chatgpt",
        "чат-1",
        Message(
            number=1,
            role="user",
            content="Python message",
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

        result = client.search(
            "python",
            chat_id="чат-1",
        )

        assert len(result) == 1
        assert result[0].message.content == "Python message"

    finally:
        server.shutdown()
        server.server_close()
        thread.join()

def test_search_with_unicode_project_and_chat_ids(tmp_path):
    storage = FileStorage(tmp_path / "projects")

    storage.save_project(
        Project(
            id="проект-1",
            name="Project One",
        )
    )

    storage.save_chat(
        Chat(
            id="чат-1",
            provider="chatgpt",
            title="Chat One",
            project_id="проект-1",
        )
    )

    storage.save_message(
        "проект-1",
        "chatgpt",
        "чат-1",
        Message(
            number=1,
            role="user",
            content="Python message",
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

        result = client.search(
            "python",
            project_id="проект-1",
            chat_id="чат-1",
        )

        assert len(result) == 1
        assert result[0].message.content == "Python message"

    finally:
        server.shutdown()
        server.server_close()
        thread.join()

def test_search_with_all_unicode_filters(tmp_path):
    storage = FileStorage(tmp_path / "projects")

    storage.save_project(
        Project(
            id="проект-1",
            name="Project One",
        )
    )

    storage.save_chat(
        Chat(
            id="чат-1",
            provider="chatgpt",
            title="Chat One",
            project_id="проект-1",
        )
    )

    storage.save_message(
        "проект-1",
        "chatgpt",
        "чат-1",
        Message(
            number=1,
            role="ассистент",
            content="Python message",
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

        result = client.search(
            "python",
            project_id="проект-1",
            chat_id="чат-1",
            role="ассистент",
        )

        assert len(result) == 1
        assert result[0].message.role == "ассистент"
        assert result[0].message.content == "Python message"

    finally:
        server.shutdown()
        server.server_close()
        thread.join()

def test_search_result_contains_expected_fields(tmp_path):
    storage = FileStorage(tmp_path / "projects")

    storage.save_project(
        Project(
            id="project-1",
            name="Project One",
        )
    )

    storage.save_chat(
        Chat(
            id="chat-1",
            provider="chatgpt",
            title="Chat One",
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
            content="Python message",
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

        result = client.search("python")

        from dataclasses import fields

        assert len(result) == 1

        assert {field.name for field in fields(result[0])} == {
            "project",
            "chat",
            "message",
            "provider",
        }

    finally:
        server.shutdown()
        server.server_close()
        thread.join()

def test_search_result_preserves_message_order(tmp_path):
    storage = FileStorage(tmp_path / "projects")

    storage.save_project(
        Project(
            id="project-1",
            name="Project One",
        )
    )

    storage.save_chat(
        Chat(
            id="chat-1",
            provider="chatgpt",
            title="Chat One",
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
            content="Python first",
        ),
    )

    storage.save_message(
        "project-1",
        "chatgpt",
        "chat-1",
        Message(
            number=2,
            role="assistant",
            content="Python second",
        ),
    )

    storage.save_message(
        "project-1",
        "chatgpt",
        "chat-1",
        Message(
            number=3,
            role="user",
            content="Python third",
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

        result = client.search("python")

        assert [item.message.number for item in result] == [1, 2, 3]

    finally:
        server.shutdown()
        server.server_close()
        thread.join()

def test_search_returns_empty_list_when_no_messages_match(tmp_path):
    storage = FileStorage(tmp_path / "projects")

    storage.save_project(
        Project(
            id="project-1",
            name="Project One",
        )
    )

    storage.save_chat(
        Chat(
            id="chat-1",
            provider="chatgpt",
            title="Chat One",
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
            content="Python message",
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

        result = client.search("javascript")

        assert result == []
        assert isinstance(result, list)

    finally:
        server.shutdown()
        server.server_close()
        thread.join()

def test_search_returns_empty_list_for_unknown_project_id(tmp_path):
    storage = FileStorage(tmp_path / "projects")

    storage.save_project(
        Project(
            id="project-1",
            name="Project One",
        )
    )

    storage.save_chat(
        Chat(
            id="chat-1",
            provider="chatgpt",
            title="Chat One",
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
            content="Python message",
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

        result = client.search(
            "python",
            project_id="unknown-project",
        )

        assert result == []
        assert isinstance(result, list)

    finally:
        server.shutdown()
        server.server_close()
        thread.join()

def test_search_returns_empty_list_for_unknown_chat_id(tmp_path):
    storage = FileStorage(tmp_path / "projects")

    storage.save_project(
        Project(
            id="project-1",
            name="Project One",
        )
    )

    storage.save_chat(
        Chat(
            id="chat-1",
            provider="chatgpt",
            title="Chat One",
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
            content="Python message",
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

        result = client.search(
            "python",
            chat_id="unknown-chat",
        )

        assert result == []
        assert isinstance(result, list)

    finally:
        server.shutdown()
        server.server_close()
        thread.join()

def test_search_returns_empty_list_for_unknown_role(tmp_path):
    storage = FileStorage(tmp_path / "projects")

    storage.save_project(
        Project(
            id="project-1",
            name="Project One",
        )
    )

    storage.save_chat(
        Chat(
            id="chat-1",
            provider="chatgpt",
            title="Chat One",
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
            content="Python message",
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

        result = client.search(
            "python",
            role="system",
        )

        assert result == []
        assert isinstance(result, list)

    finally:
        server.shutdown()
        server.server_close()
        thread.join()

def test_search_returns_empty_list_when_filters_do_not_match(tmp_path):
    storage = FileStorage(tmp_path / "projects")

    storage.save_project(
        Project(
            id="project-1",
            name="Project One",
        )
    )

    storage.save_chat(
        Chat(
            id="chat-1",
            provider="chatgpt",
            title="Chat One",
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
            content="Python message",
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

        result = client.search(
            "python",
            project_id="project-1",
            chat_id="chat-1",
            role="assistant",
        )

        assert result == []

    finally:
        server.shutdown()
        server.server_close()
        thread.join()

def test_search_does_not_mix_project_and_chat_filters(tmp_path):
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

    storage.save_chat(
        Chat(
            id="chat-1",
            provider="chatgpt",
            title="Chat One",
            project_id="project-1",
        )
    )

    storage.save_chat(
        Chat(
            id="chat-1",
            provider="chatgpt",
            title="Chat One Other Project",
            project_id="project-2",
        )
    )

    storage.save_message(
        "project-1",
        "chatgpt",
        "chat-1",
        Message(
            number=1,
            role="user",
            content="Python project one",
        ),
    )

    storage.save_message(
        "project-2",
        "chatgpt",
        "chat-1",
        Message(
            number=1,
            role="user",
            content="Python project two",
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

        result = client.search(
            "python",
            project_id="project-1",
            chat_id="chat-1",
        )

        assert len(result) == 1
        assert result[0].message.content == "Python project one"

    finally:
        server.shutdown()
        server.server_close()
        thread.join()

def test_search_by_chat_id_across_projects(tmp_path):
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

    storage.save_chat(
        Chat(
            id="chat-1",
            provider="chatgpt",
            title="Chat One",
            project_id="project-1",
        )
    )

    storage.save_chat(
        Chat(
            id="chat-1",
            provider="chatgpt",
            title="Chat One Other Project",
            project_id="project-2",
        )
    )

    storage.save_message(
        "project-1",
        "chatgpt",
        "chat-1",
        Message(
            number=1,
            role="user",
            content="Python project one",
        ),
    )

    storage.save_message(
        "project-2",
        "chatgpt",
        "chat-1",
        Message(
            number=1,
            role="user",
            content="Python project two",
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

        result = client.search(
            "python",
            chat_id="chat-1",
        )

        assert len(result) == 2
        assert [
            item.message.content
            for item in result
        ] == [
            "Python project one",
            "Python project two",
        ]

    finally:
        server.shutdown()
        server.server_close()
        thread.join()

def test_search_by_role_across_projects_and_chats(tmp_path):
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

    storage.save_chat(
        Chat(
            id="chat-1",
            provider="chatgpt",
            title="Chat One",
            project_id="project-1",
        )
    )

    storage.save_chat(
        Chat(
            id="chat-2",
            provider="chatgpt",
            title="Chat Two",
            project_id="project-2",
        )
    )

    storage.save_message(
        "project-1",
        "chatgpt",
        "chat-1",
        Message(
            number=1,
            role="assistant",
            content="Python project one",
        ),
    )

    storage.save_message(
        "project-2",
        "chatgpt",
        "chat-2",
        Message(
            number=1,
            role="assistant",
            content="Python project two",
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

        result = client.search(
            "python",
            role="assistant",
        )

        assert len(result) == 2
        assert [
            item.message.content
            for item in result
        ] == [
            "Python project one",
            "Python project two",
        ]

    finally:
        server.shutdown()
        server.server_close()
        thread.join()

def test_search_by_chat_id_and_role_across_projects(tmp_path):
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

    storage.save_chat(
        Chat(
            id="chat-1",
            provider="chatgpt",
            title="Chat One",
            project_id="project-1",
        )
    )

    storage.save_chat(
        Chat(
            id="chat-1",
            provider="chatgpt",
            title="Chat One Other Project",
            project_id="project-2",
        )
    )

    storage.save_message(
        "project-1",
        "chatgpt",
        "chat-1",
        Message(
            number=1,
            role="assistant",
            content="Python project one",
        ),
    )

    storage.save_message(
        "project-1",
        "chatgpt",
        "chat-1",
        Message(
            number=2,
            role="user",
            content="Python user one",
        ),
    )

    storage.save_message(
        "project-2",
        "chatgpt",
        "chat-1",
        Message(
            number=1,
            role="assistant",
            content="Python project two",
        ),
    )

    result = []

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

        result = client.search(
            "python",
            chat_id="chat-1",
            role="assistant",
        )

        assert len(result) == 2
        assert [
            item.message.content
            for item in result
        ] == [
            "Python project one",
            "Python project two",
        ]

    finally:
        server.shutdown()
        server.server_close()
        thread.join()

def test_search_by_project_id_and_role_across_chats(tmp_path):
    storage = FileStorage(tmp_path / "projects")

    storage.save_project(
        Project(
            id="project-1",
            name="Project One",
        )
    )

    storage.save_chat(
        Chat(
            id="chat-1",
            provider="chatgpt",
            title="Chat One",
            project_id="project-1",
        )
    )

    storage.save_chat(
        Chat(
            id="chat-2",
            provider="chatgpt",
            title="Chat Two",
            project_id="project-1",
        )
    )

    storage.save_message(
        "project-1",
        "chatgpt",
        "chat-1",
        Message(
            number=1,
            role="assistant",
            content="Python chat one",
        ),
    )

    storage.save_message(
        "project-1",
        "chatgpt",
        "chat-2",
        Message(
            number=1,
            role="assistant",
            content="Python chat two",
        ),
    )

    storage.save_message(
        "project-1",
        "chatgpt",
        "chat-2",
        Message(
            number=2,
            role="user",
            content="Python user message",
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

        result = client.search(
            "python",
            project_id="project-1",
            role="assistant",
        )

        assert len(result) == 2
        assert [
            item.message.content
            for item in result
        ] == [
            "Python chat one",
            "Python chat two",
        ]

    finally:
        server.shutdown()
        server.server_close()
        thread.join()

def test_search_by_project_id_and_chat_id_without_role_filter(
    tmp_path,
):
    storage = FileStorage(tmp_path / "projects")

    storage.save_project(
        Project(
            id="project-1",
            name="Project One",
        )
    )

    storage.save_chat(
        Chat(
            id="chat-1",
            provider="chatgpt",
            title="Chat One",
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
            content="Python user message",
        ),
    )

    storage.save_message(
        "project-1",
        "chatgpt",
        "chat-1",
        Message(
            number=2,
            role="assistant",
            content="Python assistant message",
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

        result = client.search(
            "python",
            project_id="project-1",
            chat_id="chat-1",
        )

        assert len(result) == 2
        assert [
            item.message.role
            for item in result
        ] == [
            "user",
            "assistant",
        ]

    finally:
        server.shutdown()
        server.server_close()
        thread.join()

def test_search_result_preserves_project_and_message_order(
    tmp_path,
):
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

    storage.save_chat(
        Chat(
            id="chat-1",
            provider="chatgpt",
            title="Chat One",
            project_id="project-1",
        )
    )

    storage.save_chat(
        Chat(
            id="chat-2",
            provider="chatgpt",
            title="Chat Two",
            project_id="project-2",
        )
    )

    storage.save_message(
        "project-1",
        "chatgpt",
        "chat-1",
        Message(
            number=1,
            role="user",
            content="Python first project",
        ),
    )

    storage.save_message(
        "project-1",
        "chatgpt",
        "chat-1",
        Message(
            number=2,
            role="assistant",
            content="Python second project",
        ),
    )

    storage.save_message(
        "project-2",
        "chatgpt",
        "chat-2",
        Message(
            number=1,
            role="user",
            content="Python third project",
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

        result = client.search("python")

        assert [
            item.message.content
            for item in result
        ] == [
            "Python first project",
            "Python second project",
            "Python third project",
        ]

    finally:
        server.shutdown()
        server.server_close()
        thread.join()

def test_search_result_contains_correct_file_names_for_multiple_messages(
    tmp_path,
):
    storage = FileStorage(tmp_path / "projects")

    storage.save_project(
        Project(
            id="project-1",
            name="Project One",
        )
    )

    storage.save_chat(
        Chat(
            id="chat-1",
            provider="chatgpt",
            title="Chat One",
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
            content="Python first message",
        ),
    )

    storage.save_message(
        "project-1",
        "chatgpt",
        "chat-1",
        Message(
            number=2,
            role="assistant",
            content="Python second message",
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

        result = client.search("python")

        assert [
            item.message.file_name
            for item in result
        ] == [
            "001-user.md",
            "002-assistant.md",
        ]

    finally:
        server.shutdown()
        server.server_close()
        thread.join()

def test_search_returns_search_results(tmp_path):
    storage = FileStorage(tmp_path / "projects")

    storage.save_project(
        Project(
            id="project-1",
            name="Project One",
        )
    )

    storage.save_chat(
        Chat(
            id="chat-1",
            provider="chatgpt",
            title="Chat One",
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
            content="Python is useful.",
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

        result = client.search("python")

        assert len(result) == 1
        assert isinstance(result[0], SearchResult)

        assert result[0].project.id == "project-1"
        assert result[0].project.name == "Project One"

        assert result[0].chat.id == "chat-1"
        assert result[0].chat.provider == "chatgpt"
        assert result[0].chat.title == "Chat One"
        assert result[0].chat.project_id == "project-1"

        assert result[0].message.number == 1
        assert result[0].message.role == "user"
        assert result[0].message.content == "Python is useful."
        assert result[0].message.file_name == "001-user.md"

        assert result[0].provider == "chatgpt"

    finally:
        server.shutdown()
        server.server_close()
        thread.join()

def test_search_returns_multiple_search_results_in_order(tmp_path):
    storage = FileStorage(tmp_path / "projects")

    storage.save_project(
        Project(
            id="project-1",
            name="Project One",
        )
    )

    storage.save_chat(
        Chat(
            id="chat-1",
            provider="chatgpt",
            title="Chat One",
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
            content="Python first",
        ),
    )

    storage.save_message(
        "project-1",
        "chatgpt",
        "chat-1",
        Message(
            number=2,
            role="assistant",
            content="Python second",
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

        result = client.search("python")

        assert len(result) == 2

        first = result[0]

        assert isinstance(first, SearchResult)
        assert first.project.id == "project-1"
        assert first.chat.id == "chat-1"
        assert first.message.number == 1
        assert first.message.role == "user"
        assert first.message.content == "Python first"
        assert first.message.file_name == "001-user.md"
        assert first.provider == "chatgpt"

        second = result[1]

        assert isinstance(second, SearchResult)
        assert second.project.id == "project-1"
        assert second.chat.id == "chat-1"
        assert second.message.number == 2
        assert second.message.role == "assistant"
        assert second.message.content == "Python second"
        assert second.message.file_name == "002-assistant.md"
        assert second.provider == "chatgpt"

    finally:
        server.shutdown()
        server.server_close()
        thread.join()

def test_search_result_preserves_project_and_chat_context(
    tmp_path,
):
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

    storage.save_chat(
        Chat(
            id="chat-1",
            provider="chatgpt",
            title="Chat One",
            project_id="project-1",
        )
    )
    storage.save_chat(
        Chat(
            id="chat-2",
            provider="claude",
            title="Chat Two",
            project_id="project-2",
        )
    )

    storage.save_message(
        "project-1",
        "chatgpt",
        "chat-1",
        Message(
            number=1,
            role="user",
            content="Python in project one",
        ),
    )

    storage.save_message(
        "project-2",
        "claude",
        "chat-2",
        Message(
            number=1,
            role="user",
            content="Python in project two",
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

        result = client.search("python")

        assert len(result) == 2

        first = result[0]

        assert first.project.id == "project-1"
        assert first.project.name == "Project One"
        assert first.chat.id == "chat-1"
        assert first.chat.provider == "chatgpt"
        assert first.chat.title == "Chat One"
        assert first.chat.project_id == "project-1"
        assert first.message.content == "Python in project one"
        assert first.provider == "chatgpt"

        second = result[1]

        assert second.project.id == "project-2"
        assert second.project.name == "Project Two"
        assert second.chat.id == "chat-2"
        assert second.chat.provider == "claude"
        assert second.chat.title == "Chat Two"
        assert second.chat.project_id == "project-2"
        assert second.message.content == "Python in project two"
        assert second.provider == "claude"

    finally:
        server.shutdown()
        server.server_close()
        thread.join()