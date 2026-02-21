import logging

import requests

from src.clients.interfaces import GoogleChatClientInterface
from src.config.settings import BotSettings
from src.exceptions.google_chat_errors import (
    GoogleChatPayloadBuildError,
    GoogleChatWebhookError,
)

logger = logging.getLogger(__name__)

_DEFAULT_PHOTO_CAPTION = "Photo"


class GoogleChatWebhookClient(GoogleChatClientInterface):
    def __init__(self, settings: BotSettings) -> None:
        self._webhook_url = settings.google_chat_webhook

    def send_text(self, text: str) -> None:
        logger.debug("Sending text message via webhook")
        self._post({"text": text})
        logger.info("Text message sent successfully")

    def send_photo(self, photo_url: str, caption: str | None = None) -> None:
        logger.debug("Sending photo via webhook card (url=%s)", photo_url)
        display_caption = caption or _DEFAULT_PHOTO_CAPTION
        payload = self._build_image_card_payload(photo_url, display_caption)
        self._post(payload)
        logger.info("Photo card sent successfully")

    def _build_image_card_payload(
        self, image_url: str, caption: str
    ) -> dict[str, object]:
        if not image_url.startswith("https://"):
            raise GoogleChatPayloadBuildError(
                f"Image URL must be HTTPS, got: {image_url}"
            )
        return {
            "cardsV2": [
                {
                    "cardId": "forwarded-image",
                    "card": {
                        "header": {"title": caption},
                        "sections": [
                            {
                                "widgets": [
                                    {
                                        "image": {
                                            "imageUrl": image_url,
                                            "altText": caption,
                                        }
                                    }
                                ]
                            }
                        ],
                    },
                }
            ]
        }

    def _post(self, payload: dict[str, object]) -> None:
        try:
            response = requests.post(self._webhook_url, json=payload, timeout=30)
            response.raise_for_status()
        except requests.RequestException as exc:
            logger.error("Webhook POST failed: %s", exc)
            raise GoogleChatWebhookError(str(exc)) from exc
