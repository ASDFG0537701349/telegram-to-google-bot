from abc import ABC, abstractmethod
from collections.abc import Callable


class TelegramClientInterface(ABC):
    @abstractmethod
    def resolve_photo_url(self, file_id: str) -> str:
        pass

    @abstractmethod
    def start_polling(self) -> None:
        pass

    @abstractmethod
    def register_message_handler(
        self, callback: Callable, content_types: list[str]
    ) -> None:
        pass


class GoogleChatClientInterface(ABC):
    @abstractmethod
    def send_text(self, text: str) -> None:
        pass

    @abstractmethod
    def send_photo(self, photo_url: str, caption: str | None) -> None:
        pass
