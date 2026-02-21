import logging
import sys

from src.config.settings import BotSettings


def configure_logging(settings: BotSettings) -> logging.Logger:
    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper()),
        format=settings.log_format,
        handlers=[logging.StreamHandler(sys.stdout)],
        force=True,
    )
    return logging.getLogger("telegram_to_google_bot")
