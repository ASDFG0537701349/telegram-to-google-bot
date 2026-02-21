import pytest
import requests
import responses

from src.clients.google_chat_webhook_client import GoogleChatWebhookClient
from src.config.settings import BotSettings
from src.exceptions.google_chat_errors import (
    GoogleChatPayloadBuildError,
    GoogleChatWebhookError,
)

WEBHOOK_URL = "https://chat.googleapis.com/v1/spaces/test/messages?key=k&token=t"


@pytest.fixture
def settings():
    return BotSettings(
        telegram_token="test-token",
        google_chat_webhook=WEBHOOK_URL,
    )


@pytest.fixture
def client(settings):
    return GoogleChatWebhookClient(settings)


class TestSendText:
    @responses.activate
    def test_posts_text_payload(self, client):
        responses.add(responses.POST, WEBHOOK_URL, json={}, status=200)

        client.send_text("Hello Google Chat")

        assert len(responses.calls) == 1
        assert responses.calls[0].request.body == b'{"text": "Hello Google Chat"}'

    @responses.activate
    def test_raises_on_http_error(self, client):
        responses.add(responses.POST, WEBHOOK_URL, json={"error": "bad"}, status=500)

        with pytest.raises(GoogleChatWebhookError):
            client.send_text("Hello")

    @responses.activate
    def test_raises_on_network_error(self, client):
        responses.add(
            responses.POST,
            WEBHOOK_URL,
            body=requests.ConnectionError("Network down"),
        )

        with pytest.raises(GoogleChatWebhookError):
            client.send_text("Hello")


class TestSendPhoto:
    @responses.activate
    def test_posts_cards_v2_payload(self, client):
        responses.add(responses.POST, WEBHOOK_URL, json={}, status=200)

        client.send_photo(
            "https://api.telegram.org/file/bot123/photo.jpg", "My caption"
        )

        assert len(responses.calls) == 1
        body = responses.calls[0].request.body
        assert b"cardsV2" in body
        assert b"https://api.telegram.org/file/bot123/photo.jpg" in body
        assert b"My caption" in body

    @responses.activate
    def test_uses_default_caption_when_none(self, client):
        responses.add(responses.POST, WEBHOOK_URL, json={}, status=200)

        client.send_photo("https://api.telegram.org/file/bot123/photo.jpg", None)

        body = responses.calls[0].request.body
        assert b"Photo" in body

    def test_rejects_non_https_url(self, client):
        with pytest.raises(GoogleChatPayloadBuildError, match="HTTPS"):
            client.send_photo("http://insecure.com/photo.jpg", "Test")

    @responses.activate
    def test_raises_on_webhook_failure(self, client):
        responses.add(responses.POST, WEBHOOK_URL, json={}, status=403)

        with pytest.raises(GoogleChatWebhookError):
            client.send_photo(
                "https://api.telegram.org/file/bot123/photo.jpg", "Test"
            )


class TestBuildImageCardPayload:
    def test_card_structure(self, client):
        payload = client._build_image_card_payload(
            "https://example.com/img.jpg", "Caption"
        )

        card = payload["cardsV2"][0]["card"]
        assert card["header"]["title"] == "Caption"
        widget = card["sections"][0]["widgets"][0]
        assert widget["image"]["imageUrl"] == "https://example.com/img.jpg"
        assert widget["image"]["altText"] == "Caption"
