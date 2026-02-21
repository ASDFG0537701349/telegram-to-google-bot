import logging

from src.clients.google_chat_webhook_client import GoogleChatWebhookClient
from src.clients.telegram_client import TelegramClient
from src.config.logging_config import configure_logging
from src.config.settings import BotSettings
from src.handlers.message_handler import TelegramMessageHandler
from src.server.health_server import HealthServer
from src.services.forwarder import MessageForwarder

logger = logging.getLogger(__name__)


def main() -> None:
    settings = BotSettings()
    configure_logging(settings)

    logger.info("Initializing bot components")

    telegram_client = TelegramClient(settings)
    google_chat_client = GoogleChatWebhookClient(settings)
    forwarder = MessageForwarder(google_chat_client)
    handler = TelegramMessageHandler(telegram_client, forwarder)

    telegram_client.register_message_handler(
        handler.handle, content_types=["text", "photo"]
    )

    health_server = HealthServer(settings)
    health_server.start_in_background()

    logger.info("Bot started, entering polling loop")
    telegram_client.start_polling()


if __name__ == "__main__":
    main()
