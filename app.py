from chat.models import Chat, Message, Project
from chat.storage import FileStorage
from config import load_config


def main() -> None:
    config = load_config()
    storage = FileStorage(config.archive_root)

    print("AI Chat Archive")
    print(f"Archive: {storage.root}")
    print(f"Projects: {len(config.projects)}")

    # Core smoke test: create/load a project without involving HTTP or UI.
    if config.projects:
        project_config = config.projects[0]
        project = Project(
            id=project_config["id"],
            name=project_config["name"],
            root_path=Path(project_config["root_path"]),
        )
        storage.save_project(project)

        chat = Chat(
            id="example-chat",
            provider="chatgpt",
            title="Example Chat",
            project_id=project.id,
        )
        storage.save_chat(chat)

        message = Message(
            number=1,
            role="user",
            content="# Hello\n\nThis is a Markdown message.",
        )
        storage.save_message(chat, message)

        print(f"Created example chat: {chat.id}")


if __name__ == "__main__":
    main()
