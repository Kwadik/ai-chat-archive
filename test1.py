import time
from pathlib import Path
import pytest

from chat.models import Chat, Message, Project
from chat.storage import FileStorage


@pytest.fixture
def temp_storage(tmp_path: Path) -> FileStorage:
    return FileStorage(projects_dir=tmp_path / "projects")


def test_project_crud(temp_storage: FileStorage):
    project = Project(id="ai-archive", name="AI Chat Archive", description="Test project")
    temp_storage.save_project(project)

    loaded = temp_storage.load_project("ai-archive")
    assert loaded is not None
    assert loaded.id == "ai-archive"
    assert loaded.name == "AI Chat Archive"
    assert loaded.description == "Test project"

    all_projects = temp_storage.list_projects()
    assert len(all_projects) == 1
    assert all_projects[0].id == "ai-archive"


def test_chat_save_and_load_roundtrip(temp_storage: FileStorage):
    project = Project(id="ai-archive", name="AI Chat Archive")
    temp_storage.save_project(project)

    messages = [
        Message(number=1, role="user", content="Hello, how do I design a file storage?"),
        Message(number=2, role="assistant", content="You can use a local-first JSON + MD structure."),
    ]

    chat = Chat(
        id="chat-123",
        provider="chatgpt",
        title="File Storage Design",
        project_id="ai-archive",
        messages=messages,
    )

    temp_storage.save_chat(chat)

    # Verify physical file layout (Option A)
    chat_dir = temp_storage.get_chat_dir("ai-archive", "chatgpt", "chat-123")
    assert chat_dir.exists()
    assert (chat_dir / "chat.json").exists()
    assert (chat_dir / "001-user.md").exists()
    assert (chat_dir / "002-assistant.md").exists()

    # Load back
    loaded_chat = temp_storage.load_chat("ai-archive", "chatgpt", "chat-123")
    assert loaded_chat is not None
    assert loaded_chat.id == "chat-123"
    assert loaded_chat.title == "File Storage Design"
    assert len(loaded_chat.messages) == 2
    assert loaded_chat.messages[0].content == "Hello, how do I design a file storage?"
    assert loaded_chat.messages[1].content == "You can use a local-first JSON + MD structure."


def test_chat_update_no_duplicates_and_timestamps(temp_storage: FileStorage):
    project = Project(id="ai-archive", name="AI Chat Archive")
    temp_storage.save_project(project)

    initial_msg = Message(number=1, role="user", content="Initial draft message")
    chat = Chat(
        id="chat-123",
        provider="chatgpt",
        title="Iterative Discussion",
        project_id="ai-archive",
        messages=[initial_msg],
    )

    temp_storage.save_chat(chat)
    first_load = temp_storage.load_chat("ai-archive", "chatgpt", "chat-123")
    assert first_load is not None
    created_at_msg = first_load.messages[0].created_at
    created_at_chat = first_load.created_at

    # Wait a small delay to guarantee timestamp difference if updated
    time.sleep(0.01)

    # Update message 1 and add message 2
    updated_msg_1 = Message(number=1, role="user", content="Updated draft message content")
    new_msg_2 = Message(number=2, role="assistant", content="Response to updated draft")

    updated_chat = Chat(
        id="chat-123",
        provider="chatgpt",
        title="Iterative Discussion",
        project_id="ai-archive",
        messages=[updated_msg_1, new_msg_2],
    )

    temp_storage.save_chat(updated_chat)

    second_load = temp_storage.load_chat("ai-archive", "chatgpt", "chat-123")
    assert second_load is not None
    assert len(second_load.messages) == 2

    # Verify no file duplicates on disk
    chat_dir = temp_storage.get_chat_dir("ai-archive", "chatgpt", "chat-123")
    md_files = list(chat_dir.glob("*.md"))
    assert len(md_files) == 2  # Exactly 001-user.md and 002-assistant.md

    # Check timestamp logic
    # Message 1 created_at must be preserved from initial creation
    assert second_load.messages[0].created_at == created_at_msg
    # Message 1 updated_at should be greater than initial created_at
    assert second_load.messages[0].updated_at > created_at_msg

    # Chat created_at preserved
    assert second_load.created_at == created_at_chat
    assert second_load.updated_at > created_at_chat


def test_cross_project_search_metadata(temp_storage: FileStorage):
    # Setup multiple projects and chats
    temp_storage.save_chat(
        Chat(
            id="c1",
            provider="chatgpt",
            title="Python Refactoring",
            project_id="proj-a",
            messages=[Message(number=1, role="user", content="Refactor code")],
        )
    )
    temp_storage.save_chat(
        Chat(
            id="c2",
            provider="claude",
            title="Database Schema Design",
            project_id="proj-b",
            messages=[Message(number=1, role="user", content="Design DB")],
        )
    )

    # Search query
    python_results = temp_storage.search_metadata(query="python")
    assert len(python_results) == 1
    assert python_results[0][0] == "proj-a"
    assert python_results[0][1].title == "Python Refactoring"

    # Search all
    all_results = temp_storage.search_metadata()
    assert len(all_results) == 2