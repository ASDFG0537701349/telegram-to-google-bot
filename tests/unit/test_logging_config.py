import logging

from src.config.logging_config import configure_logging
from src.config.settings import BotSettings


class TestConfigureLogging:
    def test_returns_named_logger(self, test_settings):
        logger = configure_logging(test_settings)

        assert logger.name == "telegram_to_google_bot"

    def test_sets_log_level_from_settings(self, test_settings):
        configure_logging(test_settings)

        root_logger = logging.getLogger()
        assert root_logger.level == logging.DEBUG

    def test_uses_info_level_by_default(self):
        settings = BotSettings(
            telegram_token="tok",
            google_chat_webhook="https://example.com/webhook",
        )

        configure_logging(settings)

        root_logger = logging.getLogger()
        assert root_logger.level == logging.INFO
