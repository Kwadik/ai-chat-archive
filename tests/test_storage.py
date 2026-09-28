import pytest

from datetime import datetime, timezone
from pathlib import Path

from chat.models import Chat, ChatSummary, Message, Project
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

def test_chat_and_message_metadata_are_preserved(tmp_path):
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
            "conversation_id": "provider-conversation-1",
            "tags": ["python", "architecture"],
        },
        messages=[
            Message(
                number=1,
                role="user",
                content="Hello",
                metadata={
                    "language": "en",
                    "source": "chatgpt",
                },
            ),
            Message(
                number=2,
                role="assistant",
                content="Hello!",
                metadata={
                    "model": "example-model",
                    "tokens": 42,
                },
            ),
        ],
    )

    storage.save_chat(chat)

    loaded = storage.load_chat(
        "project-1",
        "chatgpt",
        "chat-1",
    )

    assert loaded.metadata == {
        "conversation_id": "provider-conversation-1",
        "tags": ["python", "architecture"],
    }

    assert loaded.messages[0].metadata == {
        "language": "en",
        "source": "chatgpt",
    }

    assert loaded.messages[1].metadata == {
        "model": "example-model",
        "tokens": 42,
    }

def test_chat_messages_are_loaded_in_number_order(tmp_path):
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
                number=3,
                role="assistant",
                content="Third",
            ),
            Message(
                number=1,
                role="user",
                content="First",
            ),
            Message(
                number=2,
                role="assistant",
                content="Second",
            ),
        ],
    )

    storage.save_chat(chat)

    loaded = storage.load_chat(
        "project-1",
        "chatgpt",
        "chat-1",
    )

    assert [
        message.number
        for message in loaded.messages
    ] == [1, 2, 3]

    assert [
        message.content
        for message in loaded.messages
    ] == [
        "First",
        "Second",
        "Third",
    ]

def test_list_chats_returns_deterministic_order(tmp_path):
    storage = FileStorage(tmp_path / "projects")

    storage.save_project(
        Project(
            id="project-1",
            name="Test Project",
        )
    )

    chats = [
        Chat(
            id="chat-2",
            provider="chatgpt",
            title="Chat 2",
            project_id="project-1",
        ),
        Chat(
            id="chat-1",
            provider="chatgpt",
            title="Chat 1",
            project_id="project-1",
        ),
        Chat(
            id="chat-1",
            provider="claude",
            title="Claude Chat",
            project_id="project-1",
        ),
    ]

    for chat in chats:
        storage.save_chat(chat)

    loaded_chats = storage.list_chats("project-1")

    assert [
        (chat.provider, chat.id)
        for chat in loaded_chats
    ] == [
        ("chatgpt", "chat-1"),
        ("chatgpt", "chat-2"),
        ("claude", "chat-1"),
    ]

def test_search_metadata_does_not_read_message_markdown(
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

    chat = Chat(
        id="chat-1",
        provider="chatgpt",
        title="Important Chat",
        project_id="project-1",
        messages=[
            Message(
                number=1,
                role="user",
                content="This content should not be read",
            ),
        ],
    )

    storage.save_chat(chat)

    original_read_text = Path.read_text

    def fail_on_markdown(
        self: Path,
        *args,
        **kwargs,
    ):
        if self.suffix == ".md":
            raise AssertionError(
                "Metadata search must not read Markdown files"
            )

        return original_read_text(
            self,
            *args,
            **kwargs,
        )

    monkeypatch.setattr(
        Path,
        "read_text",
        fail_on_markdown,
    )

    results = storage.search_metadata(
        project_id="project-1",
        provider="chatgpt",
        chat_id="chat-1",
    )

    assert len(results) == 1
    assert results[0].id == "chat-1"

def test_chat_summary_does_not_load_message_content(tmp_path):
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
        title="Important Chat",
        project_id="project-1",
        messages=[
            Message(
                number=1,
                role="user",
                content="Secret message content",
            ),
            Message(
                number=2,
                role="assistant",
                content="Assistant response",
            ),
        ],
    )

    storage.save_chat(chat)

    chat_data = storage._read_json(
        storage.get_chat_file(
            "project-1",
            "chatgpt",
            "chat-1",
        )
    )

    summary = storage._chat_summary_from_data(
        chat_data
    )

    assert summary.id == "chat-1"
    assert summary.provider == "chatgpt"
    assert summary.title == "Important Chat"
    assert summary.project_id == "project-1"
    assert summary.message_roles == {
        "user",
        "assistant",
    }

def test_search_metadata_filters_by_project_provider_chat_and_role(
    tmp_path,
):
    storage = FileStorage(tmp_path / "projects")

    storage.save_project(
        Project(
            id="project-1",
            name="Project 1",
        )
    )
    storage.save_project(
        Project(
            id="project-2",
            name="Project 2",
        )
    )

    chats = [
        Chat(
            id="chat-1",
            provider="chatgpt",
            title="ChatGPT User Chat",
            project_id="project-1",
            messages=[
                Message(
                    number=1,
                    role="user",
                    content="User message",
                ),
            ],
        ),
        Chat(
            id="chat-2",
            provider="chatgpt",
            title="ChatGPT Assistant Chat",
            project_id="project-1",
            messages=[
                Message(
                    number=1,
                    role="assistant",
                    content="Assistant message",
                ),
            ],
        ),
        Chat(
            id="chat-1",
            provider="claude",
            title="Claude User Chat",
            project_id="project-1",
            messages=[
                Message(
                    number=1,
                    role="user",
                    content="Claude message",
                ),
            ],
        ),
        Chat(
            id="chat-1",
            provider="chatgpt",
            title="Other Project Chat",
            project_id="project-2",
            messages=[
                Message(
                    number=1,
                    role="user",
                    content="Other project message",
                ),
            ],
        ),
    ]

    for chat in chats:
        storage.save_chat(chat)

    results = storage.search_metadata(
        project_id="project-1",
        provider="chatgpt",
        chat_id="chat-1",
        role="user",
    )

    assert [
        (
            result.project_id,
            result.provider,
            result.id,
        )
        for result in results
    ] == [
        (
            "project-1",
            "chatgpt",
            "chat-1",
        )
    ]

def test_search_metadata_date_filters_include_boundaries(
    tmp_path,
):
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
        15,
        12,
        0,
        tzinfo=timezone.utc,
    )

    storage.save_chat(
        Chat(
            id="chat-1",
            provider="chatgpt",
            title="Test Chat",
            project_id="project-1",
            created_at=created_at,
            updated_at=created_at,
        )
    )

    results_at_start = storage.search_metadata(
        created_after=created_at,
    )

    results_at_end = storage.search_metadata(
        created_before=created_at,
    )

    assert [
        result.id
        for result in results_at_start
    ] == ["chat-1"]

    assert [
        result.id
        for result in results_at_end
    ] == ["chat-1"]

def test_search_metadata_date_filters_exclude_outside_range(
    tmp_path,
):
    storage = FileStorage(tmp_path / "projects")

    storage.save_project(
        Project(
            id="project-1",
            name="Test Project",
        )
    )

    before = datetime(
        2026,
        1,
        10,
        12,
        0,
        tzinfo=timezone.utc,
    )

    inside = datetime(
        2026,
        1,
        15,
        12,
        0,
        tzinfo=timezone.utc,
    )

    after = datetime(
        2026,
        1,
        20,
        12,
        0,
        tzinfo=timezone.utc,
    )

    for chat_id, created_at in [
        ("chat-before", before),
        ("chat-inside", inside),
        ("chat-after", after),
    ]:
        storage.save_chat(
            Chat(
                id=chat_id,
                provider="chatgpt",
                title=chat_id,
                project_id="project-1",
                created_at=created_at,
                updated_at=created_at,
            )
        )

    results = storage.search_metadata(
        created_after=inside,
        created_before=inside,
    )

    assert [
        result.id
        for result in results
    ] == ["chat-inside"]

def test_search_metadata_returns_chat_summary(
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
        metadata={
            "model": "gpt-test",
        },
        messages=[
            Message(
                number=1,
                role="user",
                content="Hello",
            ),
            Message(
                number=2,
                role="assistant",
                content="Hi",
            ),
        ],
    )

    storage.save_chat(chat)

    results = storage.search_metadata(
        project_id="project-1",
    )

    assert len(results) == 1

    result = results[0]

    assert isinstance(result, ChatSummary)
    assert result.id == "chat-1"
    assert result.provider == "chatgpt"
    assert result.title == "Test Chat"
    assert result.project_id == "project-1"
    assert result.metadata == {
        "model": "gpt-test",
    }
    assert result.message_roles == {
        "user",
        "assistant",
    }

def test_save_message_to_existing_chat(
    tmp_path,
):
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
            title="Python Learning",
            project_id="project-1",
            messages=[
                Message(
                    number=1,
                    role="user",
                    content="How does pytest work?",
                ),
            ],
        )
    )

    message = Message(
        number=2,
        role="assistant",
        content="# Pytest\n\nPytest runs tests.",
    )

    storage.save_message(
        project_id="project-1",
        provider="chatgpt",
        chat_id="chat-1",
        message=message,
    )

    loaded_chat = storage.load_chat(
        "project-1",
        "chatgpt",
        "chat-1",
    )

    assert len(loaded_chat.messages) == 2

    assert loaded_chat.messages[1].number == 2
    assert loaded_chat.messages[1].role == "assistant"
    assert loaded_chat.messages[1].content == (
        "# Pytest\n\nPytest runs tests."
    )

def test_save_message_assigns_next_number(
    tmp_path,
):
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
            title="Python Learning",
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
    )

    message = Message(
        number=0,
        role="assistant",
        content="Another useful answer",
    )

    storage.save_message(
        project_id="project-1",
        provider="chatgpt",
        chat_id="chat-1",
        message=message,
    )

    loaded_chat = storage.load_chat(
        "project-1",
        "chatgpt",
        "chat-1",
    )

    assert [
        loaded_message.number
        for loaded_message in loaded_chat.messages
    ] == [1, 2, 3]

    assert loaded_chat.messages[2].file_name == (
        "003-assistant.md"
    )
    assert loaded_chat.messages[2].content == (
        "Another useful answer"
    )

def test_save_message_ignores_orphan_markdown_for_numbering(
    tmp_path,
):
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
            title="Python Learning",
            project_id="project-1",
            messages=[
                Message(
                    number=1,
                    role="user",
                    content="Question",
                ),
            ],
        )
    )

    chat_dir = storage.get_chat_dir(
        "project-1",
        "chatgpt",
        "chat-1",
    )

    (chat_dir / "999-orphan.md").write_text(
        "Orphan content",
        encoding="utf-8",
    )

    storage.save_message(
        project_id="project-1",
        provider="chatgpt",
        chat_id="chat-1",
        message=Message(
            number=0,
            role="assistant",
            content="Useful answer",
        ),
    )

    assert (
        chat_dir / "002-assistant.md"
    ).exists()

    assert (
        chat_dir / "999-orphan.md"
    ).exists()

def test_save_message_preserves_metadata_and_timestamps(
    tmp_path,
):
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
            title="Python Learning",
            project_id="project-1",
            messages=[
                Message(
                    number=1,
                    role="user",
                    content="Question",
                ),
            ],
        )
    )

    created_at = datetime(
        2026,
        1,
        15,
        12,
        0,
        tzinfo=timezone.utc,
    )

    updated_at = datetime(
        2026,
        1,
        15,
        12,
        5,
        tzinfo=timezone.utc,
    )

    message = Message(
        number=0,
        role="assistant",
        content="# Answer\n\nUseful information.",
        created_at=created_at,
        updated_at=updated_at,
        metadata={
            "source": "chatgpt",
            "model": "test-model",
        },
    )

    storage.save_message(
        project_id="project-1",
        provider="chatgpt",
        chat_id="chat-1",
        message=message,
    )

    loaded_chat = storage.load_chat(
        "project-1",
        "chatgpt",
        "chat-1",
    )

    saved_message = loaded_chat.messages[-1]

    assert saved_message.created_at == created_at
    assert saved_message.metadata == {
        "source": "chatgpt",
        "model": "test-model",
    }
    assert saved_message.file_name == (
        "002-assistant.md"
    )

def test_save_message_requires_existing_chat(tmp_path):
    storage = FileStorage(tmp_path / "projects")

    storage.save_project(
        Project(
            id="project-1",
            name="Test Project",
        )
    )

    message = Message(
        number=0,
        role="assistant",
        content="Answer",
    )

    with pytest.raises(ChatNotFoundError):
        storage.save_message(
            project_id="project-1",
            provider="chatgpt",
            chat_id="missing-chat",
            message=message,
        )

def test_save_message_preserves_chat_created_at_and_updates_updated_at(
    tmp_path,
):
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
        15,
        12,
        0,
        tzinfo=timezone.utc,
    )

    chat = Chat(
        id="chat-1",
        provider="chatgpt",
        title="Python Learning",
        project_id="project-1",
        created_at=created_at,
        updated_at=created_at,
        messages=[
            Message(
                number=1,
                role="user",
                content="Question",
            ),
        ],
    )

    storage.save_chat(chat)

    before = storage.load_chat(
        "project-1",
        "chatgpt",
        "chat-1",
    )

    message = Message(
        number=0,
        role="assistant",
        content="Answer",
    )

    storage.save_message(
        project_id="project-1",
        provider="chatgpt",
        chat_id="chat-1",
        message=message,
    )

    after = storage.load_chat(
        "project-1",
        "chatgpt",
        "chat-1",
    )

    assert after.created_at == before.created_at
    assert after.created_at == created_at
    assert after.updated_at > before.updated_at

def test_save_message_writes_markdown_file(
    tmp_path,
):
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
            title="Python Learning",
            project_id="project-1",
            messages=[
                Message(
                    number=1,
                    role="user",
                    content="Question",
                ),
            ],
        )
    )

    message = Message(
        number=0,
        role="assistant",
        content="# Answer\n\nUseful information.",
    )

    storage.save_message(
        project_id="project-1",
        provider="chatgpt",
        chat_id="chat-1",
        message=message,
    )

    message_path = (
        tmp_path
        / "projects"
        / "project-1"
        / "chats"
        / "chatgpt"
        / "chat-1"
        / "002-assistant.md"
    )

    assert message_path.exists()
    assert message_path.read_text(encoding="utf-8") == (
        "# Answer\n\nUseful information."
    )

def test_search_metadata_filters_by_exact_chat_id(
    tmp_path,
):
    storage = FileStorage(tmp_path / "projects")

    storage.save_project(
        Project(
            id="project-1",
            name="Test Project",
        )
    )

    storage.save_chat(
        Chat(
            id="chat-123",
            provider="chatgpt",
            title="First Chat",
            project_id="project-1",
        )
    )

    storage.save_chat(
        Chat(
            id="chat-123-extra",
            provider="chatgpt",
            title="Second Chat",
            project_id="project-1",
        )
    )

    results = storage.search_metadata(
        chat_id="chat-123",
    )

    assert [chat.id for chat in results] == [
        "chat-123",
    ]

def test_search_metadata_without_filters_returns_all_chats(
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
            id="chat-b",
            provider="chatgpt",
            title="Chat B",
            project_id="project-1",
        )
    )

    storage.save_chat(
        Chat(
            id="chat-a",
            provider="chatgpt",
            title="Chat A",
            project_id="project-2",
        )
    )

    results = storage.search_metadata()

    assert [
        (chat.project_id, chat.provider, chat.id)
        for chat in results
    ] == [
        ("project-1", "chatgpt", "chat-b"),
        ("project-2", "chatgpt", "chat-a"),
    ]