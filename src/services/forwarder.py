import logging

from src.clients.interfaces import GoogleChatClientInterface
from src.exceptions.base import BotBaseError
from src.models.message import ForwardableMessage, PhotoData

logger = logging.getLogger(__name__)


class MessageForwarder:
    def __init__(self, google_chat_client: GoogleChatClientInterface) -> None:
        self._google_chat = google_chat_client

    def forward(self, message: ForwardableMessage) -> None:
        logger.info(
            "Forwarding message from sender=%s, chat=%s",
            message.sender_name,
            message.chat_title,
        )
        try:
            if message.photo:
                self._forward_photo(message.photo)
            elif message.text:
                self._forward_text(message.text)
            else:
                logger.warning("Message with no text and no photo, skipping")
        except BotBaseError:
            raise
        except Exception as exc:
            logger.critical("Unexpected error during forwarding: %s", exc)
            raise BotBaseError(str(exc)) from exc

    def _forward_text(self, text: str) -> None:
        logger.debug("Forwarding text message")
        self._google_chat.send_text(text)

    def _forward_photo(self, photo: PhotoData) -> None:
        logger.debug("Forwarding photo message")
        self._google_chat.send_photo(photo.file_url, photo.caption)
