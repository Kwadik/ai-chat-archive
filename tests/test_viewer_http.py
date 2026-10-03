import threading
from urllib.request import urlopen

from chat.models import Chat, Message, Project
from chat.storage import FileStorage
from viewer.http_server import create_server
from urllib.error import HTTPError
from http.client import HTTPConnection


def test_get_projects_page(tmp_path):
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
        url = (
            f"http://127.0.0.1:"
            f"{server.server_address[1]}/"
        )

        with urlopen(url) as response:
            html = response.read().decode("utf-8")

        assert response.status == 200
        assert "First Project" in html
        assert "Second Project" in html

    finally:
        server.shutdown()
        server.server_close()
        thread.join()

def test_unknown_viewer_route_returns_404(tmp_path):
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
        url = (
            f"http://127.0.0.1:"
            f"{server.server_address[1]}/unknown"
        )

        try:
            urlopen(url)
        except HTTPError as error:
            assert error.code == 404
        else:
            raise AssertionError("Expected HTTP 404")

    finally:
        server.shutdown()
        server.server_close()
        thread.join()

def test_get_project_page(tmp_path):
    storage = FileStorage(tmp_path / "projects")

    storage.save_project(
        Project(
            id="project-1",
            name="My Project",
            description="Project description",
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
        url = (
            f"http://127.0.0.1:"
            f"{server.server_address[1]}/projects/project-1"
        )

        with urlopen(url) as response:
            html = response.read().decode("utf-8")

        assert response.status == 200
        assert "My Project" in html
        assert "Project description" in html

    finally:
        server.shutdown()
        server.server_close()
        thread.join()

def test_missing_project_returns_404(tmp_path):
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
        url = (
            f"http://127.0.0.1:"
            f"{server.server_address[1]}/projects/missing"
        )

        try:
            urlopen(url)
        except HTTPError as error:
            assert error.code == 404
        else:
            raise AssertionError("Expected HTTP 404")

    finally:
        server.shutdown()
        server.server_close()
        thread.join()

def test_get_viewer_css(tmp_path):
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
        url = (
            f"http://127.0.0.1:"
            f"{server.server_address[1]}"
            "/static/css/viewer.css"
        )

        with urlopen(url) as response:
            css = response.read().decode("utf-8")

        assert response.status == 200
        assert response.headers["Content-Type"].startswith("text/css")
        assert "font-family" in css

    finally:
        server.shutdown()
        server.server_close()
        thread.join()

def test_get_viewer_js(tmp_path):
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
        url = (
            f"http://127.0.0.1:"
            f"{server.server_address[1]}"
            "/static/js/viewer.js"
        )

        with urlopen(url) as response:
            javascript = response.read().decode("utf-8")

        assert response.status == 200
        assert response.headers["Content-Type"].startswith(
            "application/javascript"
        )
        assert '"use strict";' in javascript

    finally:
        server.shutdown()
        server.server_close()
        thread.join()

def test_get_project_page_shows_chats(tmp_path):
    storage = FileStorage(tmp_path / "projects")

    storage.save_project(
        Project(
            id="project-1",
            name="My Project",
        )
    )

    storage.save_chat(
        Chat(
            id="chat-1",
            provider="chatgpt",
            title="My First Chat",
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
        url = (
            f"http://127.0.0.1:"
            f"{server.server_address[1]}"
            "/projects/project-1"
        )

        with urlopen(url) as response:
            html = response.read().decode("utf-8")

        assert response.status == 200
        assert "My Project" in html
        assert "My First Chat" in html

    finally:
        server.shutdown()
        server.server_close()
        thread.join()

def test_get_project_page_chat_title_is_link(tmp_path):
    storage = FileStorage(tmp_path)

    project = Project(
        id="project-1",
        name="My Project",
    )
    storage.save_project(project)

    chat = Chat(
        id="chat-1",
        provider="chatgpt",
        title="My First Chat",
        project_id="project-1",
    )
    storage.save_chat(chat)

    server = create_server(storage)
    thread = threading.Thread(target=server.serve_forever)
    thread.start()

    try:
        connection = HTTPConnection(
            server.server_address[0],
            server.server_address[1],
        )
        connection.request("GET", "/projects/project-1")
        response = connection.getresponse()

        body = response.read().decode("utf-8")

        assert response.status == 200
        assert (
            'href="/projects/project-1/chats/chatgpt/chat-1"'
            in body
        )
        assert "My First Chat" in body
    finally:
        server.shutdown()
        thread.join()
        server.server_close()

def test_get_chat_page(tmp_path):
    storage = FileStorage(tmp_path)

    project = Project(
        id="project-1",
        name="My Project",
    )
    storage.save_project(project)

    chat = Chat(
        id="chat-1",
        provider="chatgpt",
        title="My First Chat",
        project_id="project-1",
    )
    storage.save_chat(chat)

    message = Message(
        number=1,
        role="user",
        content="Hello from my chat",
    )
    storage.save_message(
        "project-1",
        "chatgpt",
        "chat-1",
        message,
    )

    server = create_server(storage)
    thread = threading.Thread(target=server.serve_forever)
    thread.start()

    try:
        connection = HTTPConnection(
            server.server_address[0],
            server.server_address[1],
        )
        connection.request(
            "GET",
            "/projects/project-1/chats/chatgpt/chat-1",
        )
        response = connection.getresponse()

        body = response.read().decode("utf-8")

        assert response.status == 200
        assert "My First Chat" in body
        assert "Hello from my chat" in body
    finally:
        server.shutdown()
        thread.join()
        server.server_close()

def test_missing_chat_returns_404(tmp_path):
    storage = FileStorage(tmp_path)

    project = Project(
        id="project-1",
        name="My Project",
    )
    storage.save_project(project)

    server = create_server(storage)
    thread = threading.Thread(target=server.serve_forever)
    thread.start()

    try:
        connection = HTTPConnection(
            server.server_address[0],
            server.server_address[1],
        )
        connection.request(
            "GET",
            "/projects/project-1/chats/chatgpt/missing-chat",
        )
        response = connection.getresponse()

        response.read()

        assert response.status == 404
    finally:
        server.shutdown()
        thread.join()
        server.server_close()

def test_get_chat_page_shows_messages_in_order(tmp_path):
    storage = FileStorage(tmp_path)

    project = Project(
        id="project-1",
        name="My Project",
    )
    storage.save_project(project)

    chat = Chat(
        id="chat-1",
        provider="chatgpt",
        title="My First Chat",
        project_id="project-1",
    )
    storage.save_chat(chat)

    storage.save_message(
        "project-1",
        "chatgpt",
        "chat-1",
        Message(
            number=1,
            role="user",
            content="First message",
        ),
    )

    storage.save_message(
        "project-1",
        "chatgpt",
        "chat-1",
        Message(
            number=2,
            role="assistant",
            content="Second message",
        ),
    )

    server = create_server(storage)
    thread = threading.Thread(target=server.serve_forever)
    thread.start()

    try:
        connection = HTTPConnection(
            server.server_address[0],
            server.server_address[1],
        )
        connection.request(
            "GET",
            "/projects/project-1/chats/chatgpt/chat-1",
        )
        response = connection.getresponse()

        body = response.read().decode("utf-8")

        assert response.status == 200
        assert "First message" in body
        assert "Second message" in body
        assert body.index("First message") < body.index("Second message")
    finally:
        server.shutdown()
        thread.join()
        server.server_close()