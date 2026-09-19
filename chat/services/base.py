from abc import ABC, abstractmethod
from typing import Any


class AIService(ABC):
    """Provider adapter interface."""

    name: str = "unknown"

    @abstractmethod
    def can_handle(self, url: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def get_chat_id(self, url: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_chat_title(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_messages(self) -> list[Any]:
        raise NotImplementedError
