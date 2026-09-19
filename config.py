from dataclasses import dataclass
import json
from pathlib import Path


@dataclass(frozen=True)
class AppConfig:
    archive_root: Path
    projects: list[dict]


def load_config(path: Path | None = None) -> AppConfig:
    path = path or Path("config/projects.json")

    if not path.exists():
        return AppConfig(
            archive_root=Path("chats"),
            projects=[],
        )

    data = json.loads(path.read_text(encoding="utf-8"))

    return AppConfig(
        archive_root=Path(data.get("archive_root", "chats")),
        projects=data.get("projects", []),
    )
