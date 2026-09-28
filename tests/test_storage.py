from datetime import datetime, timezone

from chat.models import Chat, Message, Project
from chat.storage import (
    ChatNotFoundError,
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


def test_updated_message_preserves_created_at_and_updates_updated_at(
    tmp_path,
    monkeypatch,
):
    storage = FileStorage(tmp_path / "projects")

    storage.save_project(
        Project(
            id="project-1",
            name="Test Project",
        )
    )

    first_time = datetime(
        2026,
        1,
        1,
        10,
        0,
        tzinfo=timezone.utc,
    )

    second_time = datetime(
        2026,
        1,
        1,
        10,
        5,
        tzinfo=timezone.utc,
    )

    monkeypatch.setattr(
        "chat.storage.utc_now",
        lambda: first_time,
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
                content="Original",
            )
        ],
    )

    storage.save_chat(chat)

    loaded = storage.load_chat(
        "project-1",
        "chatgpt",
        "chat-1",
    )

    original_created_at = loaded.messages[0].created_at
    original_updated_at = loaded.messages[0].updated_at

    monkeypatch.setattr(
        "chat.storage.utc_now",
        lambda: second_time,
    )

    updated_chat = Chat(
        id="chat-1",
        provider="chatgpt",
        title="Test Chat",
        project_id="project-1",
        messages=[
            Message(
                number=1,
                role="user",
                content="Changed",
            )
        ],
    )

    storage.save_chat(updated_chat)

    loaded = storage.load_chat(
        "project-1",
        "chatgpt",
        "chat-1",
    )

    message = loaded.messages[0]

    assert message.content == "Changed"
    assert message.created_at == original_created_at
    assert message.updated_at == second_time
    assert message.updated_at != original_updated_at


def test_unchanged_message_preserves_timestamps(
    tmp_path,
    monkeypatch,
):
    storage = FileStorage(tmp_path / "projects")

    storage.save_project(
        Project(
            id="project-1",
            name="Test Project",
        )
    )

    first_time = datetime(
        2026,
        1,
        1,
        10,
        0,
        tzinfo=timezone.utc,
    )

    second_time = datetime(
        2026,
        1,
        1,
        10,
        5,
        tzinfo=timezone.utc,
    )

    monkeypatch.setattr(
        "chat.storage.utc_now",
        lambda: first_time,
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
                content="Original",
            )
        ],
    )

    storage.save_chat(chat)

    loaded = storage.load_chat(
        "project-1",
        "chatgpt",
        "chat-1",
    )

    original_created_at = loaded.messages[0].created_at
    original_updated_at = loaded.messages[0].updated_at

    monkeypatch.setattr(
        "chat.storage.utc_now",
        lambda: second_time,
    )

    unchanged_chat = Chat(
        id="chat-1",
        provider="chatgpt",
        title="Test Chat",
        project_id="project-1",
        messages=[
            Message(
                number=1,
                role="user",
                content="Original",
            )
        ],
    )

    storage.save_chat(unchanged_chat)

    loaded = storage.load_chat(
        "project-1",
        "chatgpt",
        "chat-1",
    )

    message = loaded.messages[0]

    assert message.created_at == original_created_at
    assert message.updated_at == original_updated_at


def test_updated_message_does_not_create_duplicate_files(
    tmp_path,
):
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
                content="Original",
            )
        ],
    )

    storage.save_chat(chat)

    updated_chat = Chat(
        id="chat-1",
        provider="chatgpt",
        title="Test Chat",
        project_id="project-1",
        messages=[
            Message(
                number=1,
                role="user",
                content="Changed",
            )
        ],
    )

    storage.save_chat(updated_chat)

    chat_dir = (
        tmp_path
        / "projects"
        / "project-1"
        / "chats"
        / "chatgpt"
        / "chat-1"
    )

    markdown_files = list(chat_dir.glob("*.md"))

    assert markdown_files == [
        chat_dir / "001-user.md"
    ]

    assert (
        chat_dir / "001-user.md"
    ).read_text(encoding="utf-8") == "Changed"

def test_chat_timestamps_are_saved_and_loaded(tmp_path):
    storage = FileStorage(tmp_path / "projects")

    storage.save_project(
        Project(
            id="project-1",
            name="Test Project",
        )
    )

    created_at = datetime(
        2026,
        1,
        1,
        10,
        0,
        tzinfo=timezone.utc,
    )

    updated_at = datetime(
        2026,
        1,
        1,
        10,
        5,
        tzinfo=timezone.utc,
    )

    chat = Chat(
        id="chat-1",
        provider="chatgpt",
        title="Test Chat",
        project_id="project-1",
        created_at=created_at,
        updated_at=updated_at,
    )

    storage.save_chat(chat)

    loaded = storage.load_chat(
        "project-1",
        "chatgpt",
        "chat-1",
    )

    assert loaded.created_at == created_at
    assert loaded.updated_at == updated_at


def test_updated_chat_preserves_created_at_and_updates_updated_at(
    tmp_path,
    monkeypatch,
):
    storage = FileStorage(tmp_path / "projects")

    storage.save_project(
        Project(
            id="project-1",
            name="Test Project",
        )
    )

    first_time = datetime(
        2026,
        1,
        1,
        10,
        0,
        tzinfo=timezone.utc,
    )

    second_time = datetime(
        2026,
        1,
        1,
        10,
        5,
        tzinfo=timezone.utc,
    )

    chat = Chat(
        id="chat-1",
        provider="chatgpt",
        title="Original Title",
        project_id="project-1",
        created_at=first_time,
        updated_at=first_time,
    )

    storage.save_chat(chat)

    loaded = storage.load_chat(
        "project-1",
        "chatgpt",
        "chat-1",
    )

    original_created_at = loaded.created_at
    original_updated_at = loaded.updated_at

    monkeypatch.setattr(
        "chat.storage.utc_now",
        lambda: second_time,
    )

    updated_chat = Chat(
        id="chat-1",
        provider="chatgpt",
        title="Changed Title",
        project_id="project-1",
        created_at=second_time,
        updated_at=second_time,
    )

    storage.save_chat(updated_chat)

    loaded = storage.load_chat(
        "project-1",
        "chatgpt",
        "chat-1",
    )

    assert loaded.created_at == original_created_at
    assert loaded.updated_at == second_time
    assert loaded.updated_at != original_updated_at

def test_missing_chat_raises(tmp_path):
    storage = FileStorage(tmp_path / "projects")

    storage.save_project(
        Project(
            id="project-1",
            name="Test Project",
        )
    )

    try:
        storage.load_chat(
            "project-1",
            "chatgpt",
            "missing-chat",
        )
        assert False, "Expected ChatNotFoundError"
    except ChatNotFoundError:
        pass

def test_list_chats_returns_chats_from_project(tmp_path):
    storage = FileStorage(tmp_path / "projects")

    storage.save_project(
        Project(
            id="project-1",
            name="Test Project",
        )
    )

    first_chat = Chat(
        id="chat-1",
        provider="chatgpt",
        title="First Chat",
        project_id="project-1",
        messages=[
            Message(
                number=1,
                role="user",
                content="Question",
            ),
            Message(
                number=2,
                role="assistant",
                content="Answer",
            ),
        ],
    )

    second_chat = Chat(
        id="chat-2",
        provider="claude",
        title="Second Chat",
        project_id="project-1",
        messages=[
            Message(
                number=1,
                role="user",
                content="Hello",
            ),
        ],
    )

    storage.save_chat(first_chat)
    storage.save_chat(second_chat)

    chats = storage.list_chats("project-1")

    assert len(chats) == 2

    chat_by_id = {
        chat.id: chat
        for chat in chats
    }

    assert chat_by_id["chat-1"].provider == "chatgpt"
    assert chat_by_id["chat-1"].title == "First Chat"

    assert [
        message.number
        for message in chat_by_id["chat-1"].messages
    ] == [1, 2]

    assert [
        message.content
        for message in chat_by_id["chat-1"].messages
    ] == [
        "Question",
        "Answer",
    ]

    assert chat_by_id["chat-2"].provider == "claude"
    assert chat_by_id["chat-2"].title == "Second Chat"

def test_list_chats_missing_project_raises(tmp_path):
    storage = FileStorage(tmp_path / "projects")

    try:
        storage.list_chats("missing-project")
        assert False, "Expected ProjectNotFoundError"
    except ProjectNotFoundError:
        pass