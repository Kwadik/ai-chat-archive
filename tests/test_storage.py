from chat.models import Chat, Message, Project
from chat.storage import (
    FileStorage,
    ProjectNotFoundError,
)


def test_project_save_and_load(tmp_path):
    storage = FileStorage(tmp_path / "projects")

    project = Project(
        id="project-1",
        name="Test Project",
        description="Test description",
        root_path="E:/Projects/test",
    )

    storage.save_project(project)

    loaded = storage.load_project("project-1")

    assert loaded.id == "project-1"
    assert loaded.name == "Test Project"
    assert loaded.description == "Test description"
    assert loaded.root_path == "E:/Projects/test"


def test_missing_project_raises(tmp_path):
    storage = FileStorage(tmp_path / "projects")

    try:
        storage.load_project("missing")
        assert False, "Expected ProjectNotFoundError"
    except ProjectNotFoundError:
        pass


def test_chat_save_and_load(tmp_path):
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
        messages=[
            Message(
                number=1,
                role="user",
                content="# Hello\n\nThis is Markdown.",
            ),
            Message(
                number=2,
                role="assistant",
                content="```python\nprint('hello')\n```",
            ),
        ],
    )

    storage.save_chat(chat)

    loaded = storage.load_chat(
        "project-1",
        "chatgpt",
        "chat-1",
    )

    assert loaded.id == "chat-1"
    assert loaded.provider == "chatgpt"
    assert loaded.title == "Test Chat"

    assert len(loaded.messages) == 2

    assert loaded.messages[0].content == (
        "# Hello\n\nThis is Markdown."
    )

    assert loaded.messages[1].content == (
        "```python\nprint('hello')\n```"
    )


def test_chat_files_are_created_in_expected_structure(tmp_path):
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
        messages=[
            Message(
                number=1,
                role="user",
                content="Hello",
            )
        ],
    )

    storage.save_chat(chat)

    chat_dir = (
        tmp_path
        / "projects"
        / "project-1"
        / "chats"
        / "chatgpt"
        / "chat-1"
    )

    assert (chat_dir / "chat.json").exists()
    assert (chat_dir / "001-user.md").exists()


def test_save_chat_does_not_create_missing_project(tmp_path):
    storage = FileStorage(tmp_path / "projects")

    chat = Chat(
        id="chat-1",
        provider="chatgpt",
        title="Test Chat",
        project_id="missing-project",
    )

    try:
        storage.save_chat(chat)
        assert False, "Expected ProjectNotFoundError"
    except ProjectNotFoundError:
        pass