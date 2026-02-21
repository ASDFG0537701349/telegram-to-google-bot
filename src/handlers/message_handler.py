import logging
from typing import Any

from src.clients.interfaces import TelegramClientInterface
from src.exceptions.base import BotBaseError
from src.models.message import ForwardableMessage, PhotoData
from src.services.forwarder import MessageForwarder

logger = logging.getLogger(__name__)


class TelegramMessageHandler:
    def __init__(
        self,
        telegram_client: TelegramClientInterface,
        forwarder: MessageForwarder,
    ) -> None:
        self._telegram = telegram_client
        self._forwarder = forwarder

    def handle(self, raw_message: Any) -> None:
        try:
            forwarded = self._parse_message(raw_message)
            if forwarded:
                self._forwarder.forward(forwarded)
        except BotBaseError as exc:
            logger.error("Failed to forward message: %s", exc)
        except Exception as exc:
            logger.critical("Unhandled error in message handler: %s", exc)

    def _parse_message(self, raw_message: Any) -> ForwardableMessage | None:
        sender_name = self._extract_sender_name(raw_message)
        chat_title = getattr(raw_message.chat, "title", "DM") or "DM"

        if getattr(raw_message, "photo", None):
            return self._parse_photo_message(raw_message, sender_name, chat_title)
        if getattr(raw_message, "text", None):
            return ForwardableMessage(
                text=raw_message.text,
                sender_name=sender_name,
                chat_title=chat_title,
            )
        logger.warning("Unsupported message type, skipping")
        return None

    def _parse_photo_message(
        self, raw_message: Any, sender_name: str, chat_title: str
    ) -> ForwardableMessage:
        largest_photo = raw_message.photo[-1]
        file_url = self._telegram.resolve_photo_url(largest_photo.file_id)
        return ForwardableMessage(
            photo=PhotoData(
                file_url=file_url,
                caption=getattr(raw_message, "caption", None),
            ),
            sender_name=sender_name,
            chat_title=chat_title,
        )

    @staticmethod
    def _extract_sender_name(raw_message: Any) -> str:
        user = getattr(raw_message, "from_user", None)
        if user:
            parts = [user.first_name or "", user.last_name or ""]
            return " ".join(p for p in parts if p) or "Unknown"
        return "Unknown"
