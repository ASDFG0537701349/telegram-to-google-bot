import logging
from collections.abc import Callable

import telebot
import telebot.apihelper

from src.clients.interfaces import TelegramClientInterface
from src.config.settings import BotSettings
from src.exceptions.telegram_errors import TelegramFileRetrievalError

logger = logging.getLogger(__name__)


class TelegramClient(TelegramClientInterface):
    def __init__(self, settings: BotSettings) -> None:
        self._bot = telebot.TeleBot(settings.telegram_token)
        self._api_base_url = settings.telegram_api_base_url
        self._token = settings.telegram_token

    def resolve_photo_url(self, file_id: str) -> str:
        logger.debug("Resolving file URL for file_id=%s", file_id)
        try:
            file_info = self._bot.get_file(file_id)
        except telebot.apihelper.ApiTelegramException as exc:
            logger.error("Telegram getFile failed: %s", exc)
            raise TelegramFileRetrievalError(str(exc)) from exc

        url = f"{self._api_base_url}/file/bot{self._token}/{file_info.file_path}"
        logger.info("Resolved photo URL for file_id=%s", file_id)
        return url

    def register_message_handler(
        self, callback: Callable, content_types: list[str]
    ) -> None:
        self._bot.message_handler(content_types=content_types)(callback)
        logger.info("Registered handler for content_types=%s", content_types)

    def start_polling(self) -> None:
        logger.info("Starting Telegram polling")
        self._bot.polling(none_stop=True)
