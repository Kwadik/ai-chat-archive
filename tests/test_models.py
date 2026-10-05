from datetime import timezone

from chat.models import Chat, Message, Project, SearchResult


def test_message_defaults():
    message = Message(
        number=1,
        role="user",
        content="Hello",
    )

    assert message.number == 1
    assert message.role == "user"
    assert message.content == "Hello"
    assert message.file_name == "001-user.md"

    assert message.created_at.tzinfo is not None
    assert message.updated_at.tzinfo is not None

    assert message.created_at.tzinfo == timezone.utc
    assert message.updated_at.tzinfo == timezone.utc


def test_chat_defaults():
    chat = Chat(
        id="chat-1",
        provider="chatgpt",
        title="Test chat",
        project_id="project-1",
    )

    assert chat.id == "chat-1"
    assert chat.provider == "chatgpt"
    assert chat.title == "Test chat"
    assert chat.project_id == "project-1"

    assert chat.messages == []
    assert chat.metadata == {}

    assert chat.created_at.tzinfo is not None
    assert chat.updated_at.tzinfo is not None


def test_project_defaults():
    project = Project(
        id="project-1",
        name="Test project",
    )

    assert project.id == "project-1"
    assert project.name == "Test project"
    assert project.description == ""
    assert project.root_path == ""

    assert project.created_at.tzinfo is not None
    assert project.updated_at.tzinfo is not None


def test_message_custom_file_name():
    message = Message(
        number=2,
        role="assistant",
        content="Answer",
        file_name="custom.md",
    )

    assert message.file_name == "custom.md"

def test_search_result_contains_project_chat_message_and_provider():
    project = Project(
        id="project-1",
        name="Project One",
    )

    chat = Chat(
        id="chat-1",
        provider="chatgpt",
        title="Chat One",
        project_id="project-1",
    )

    message = Message(
        number=1,
        role="user",
        content="Python is useful.",
    )

    result = SearchResult(
        project=project,
        chat=chat,
        message=message,
        provider="chatgpt",
    )

    assert result.project is project
    assert result.chat is chat
    assert result.message is message
    assert result.provider == "chatgpt"