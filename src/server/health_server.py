import logging
from threading import Thread

from flask import Flask

from src.config.settings import BotSettings

logger = logging.getLogger(__name__)


class HealthServer:
    def __init__(self, settings: BotSettings) -> None:
        self._app = Flask("health")
        self._port = settings.port
        self._app.add_url_rule("/", view_func=self._health_check)

    @staticmethod
    def _health_check() -> str:
        return "OK"

    def start_in_background(self) -> None:
        logger.info("Starting health server on port %d", self._port)
        thread = Thread(
            target=self._app.run,
            kwargs={"host": "0.0.0.0", "port": self._port},
            daemon=True,
        )
        thread.start()
