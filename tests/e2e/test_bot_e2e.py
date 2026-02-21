from unittest.mock import MagicMock, patch

import pytest
import responses

from src.clients.google_chat_webhook_client import GoogleChatWebhookClient
from src.clients.telegram_client import TelegramClient
from src.config.settings import BotSettings
from src.handlers.message_handler import TelegramMessageHandler
from src.services.forwarder import MessageForwarder

WEBHOOK_URL = "https://chat.googleapis.com/v1/spaces/test/messages?key=k&token=t"


@pytest.fixture
def settings():
    return BotSettings(
        telegram_token="e2e-token",
        google_chat_webhook=WEBHOOK_URL,
        telegram_api_base_url="https://api.telegram.org",
    )


@pytest.fixture
def google_chat_client(settings):
    return GoogleChatWebhookClient(settings)


@pytest.fixture
def mock_telebot():
    with patch("src.clients.telegram_client.telebot.TeleBot") as mock_cls:
        yield mock_cls.return_value


@pytest.fixture
def telegram_client(settings, mock_telebot):
    with patch(
        "src.clients.telegram_client.telebot.TeleBot", return_value=mock_telebot
    ):
        return TelegramClient(settings)


@pytest.fixture
def full_stack(telegram_client, google_chat_client):
    forwarder = MessageForwarder(google_chat_client)
    handler = TelegramMessageHandler(telegram_client, forwarder)
    return handler


class TestEndToEndTextFlow:
    @responses.activate
    def test_telegram_text_reaches_google_chat_webhook(self, full_stack):
        responses.add(responses.POST, WEBHOOK_URL, json={}, status=200)

        raw_msg = MagicMock()
        raw_msg.text = "E2E text message"
        raw_msg.photo = None
        raw_msg.chat.title = "E2E Group"
        raw_msg.from_user.first_name = "E2E"
        raw_msg.from_user.last_name = "User"

        full_stack.handle(raw_msg)

        assert len(responses.calls) == 1
        body = responses.calls[0].request.body
        assert b"E2E text message" in body


class TestEndToEndPhotoFlow:
    @responses.activate
    def test_telegram_photo_reaches_google_chat_as_card(
        self, full_stack, mock_telebot
    ):
        responses.add(responses.POST, WEBHOOK_URL, json={}, status=200)

        file_info = MagicMock()
        file_info.file_path = "photos/e2e_test.jpg"
        mock_telebot.get_file.return_value = file_info

        photo_size = MagicMock()
        photo_size.file_id = "e2e-file-id"

        raw_msg = MagicMock()
        raw_msg.text = None
        raw_msg.photo = [MagicMock(), photo_size]
        raw_msg.caption = "E2E photo caption"
        raw_msg.chat.title = "E2E Group"
        raw_msg.from_user.first_name = "E2E"
        raw_msg.from_user.last_name = "User"

        full_stack.handle(raw_msg)

        mock_telebot.get_file.assert_called_once_with("e2e-file-id")
        assert len(responses.calls) == 1
        body = responses.calls[0].request.body
        assert b"cardsV2" in body
        assert b"photos/e2e_test.jpg" in body
        assert b"E2E photo caption" in body


class TestEndToEndErrorResilience:
    @responses.activate
    def test_webhook_failure_does_not_crash_handler(self, full_stack):
        responses.add(responses.POST, WEBHOOK_URL, json={}, status=500)

        raw_msg = MagicMock()
        raw_msg.text = "Will fail"
        raw_msg.photo = None
        raw_msg.chat.title = "Chat"
        raw_msg.from_user.first_name = "Test"
        raw_msg.from_user.last_name = None

        full_stack.handle(raw_msg)

    @responses.activate
    def test_telegram_api_failure_does_not_crash_handler(
        self, full_stack, mock_telebot
    ):
        from telebot.apihelper import ApiTelegramException

        mock_telebot.get_file.side_effect = ApiTelegramException(
            "getFile",
            "Not Found",
            {"error_code": 404, "description": "Not Found"},
        )

        photo_size = MagicMock()
        photo_size.file_id = "bad-id"

        raw_msg = MagicMock()
        raw_msg.text = None
        raw_msg.photo = [photo_size]
        raw_msg.caption = None
        raw_msg.chat.title = "Chat"
        raw_msg.from_user.first_name = "Test"
        raw_msg.from_user.last_name = None

        full_stack.handle(raw_msg)
