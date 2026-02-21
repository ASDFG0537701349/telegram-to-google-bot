from unittest.mock import MagicMock

import pytest

from src.exceptions.telegram_errors import TelegramFileRetrievalError
from src.handlers.message_handler import TelegramMessageHandler
from src.models.message import ForwardableMessage
from src.services.forwarder import MessageForwarder


@pytest.fixture
def mock_forwarder(mock_google_chat_client):
    return MagicMock(spec=MessageForwarder)


@pytest.fixture
def handler(mock_telegram_client, mock_forwarder):
    return TelegramMessageHandler(mock_telegram_client, mock_forwarder)


class TestHandleTextMessage:
    def test_forwards_text_message(
        self, handler, mock_forwarder, raw_telegram_text_message
    ):
        handler.handle(raw_telegram_text_message)

        mock_forwarder.forward.assert_called_once()
        msg = mock_forwarder.forward.call_args[0][0]
        assert isinstance(msg, ForwardableMessage)
        assert msg.text == "Hello from Telegram"
        assert msg.sender_name == "John Doe"
        assert msg.chat_title == "My Group"

    def test_does_not_resolve_photo_url(
        self, handler, mock_telegram_client, raw_telegram_text_message
    ):
        handler.handle(raw_telegram_text_message)

        mock_telegram_client.resolve_photo_url.assert_not_called()


class TestHandlePhotoMessage:
    def test_forwards_photo_message(
        self, handler, mock_forwarder, mock_telegram_client, raw_telegram_photo_message
    ):
        handler.handle(raw_telegram_photo_message)

        mock_telegram_client.resolve_photo_url.assert_called_once_with("AgACAgIAAx0CZ")
        mock_forwarder.forward.assert_called_once()
        msg = mock_forwarder.forward.call_args[0][0]
        assert isinstance(msg, ForwardableMessage)
        assert msg.photo is not None
        assert msg.photo.caption == "Nice photo"
        assert msg.sender_name == "Jane Smith"

    def test_uses_largest_photo(
        self, handler, mock_telegram_client, raw_telegram_photo_message
    ):
        handler.handle(raw_telegram_photo_message)

        mock_telegram_client.resolve_photo_url.assert_called_once_with("AgACAgIAAx0CZ")


class TestHandleUnsupportedMessage:
    def test_skips_unsupported_message(self, handler, mock_forwarder):
        msg = MagicMock()
        msg.text = None
        msg.photo = None
        msg.chat.title = "Test"
        msg.from_user.first_name = "Test"
        msg.from_user.last_name = None

        handler.handle(msg)

        mock_forwarder.forward.assert_not_called()


class TestSenderNameExtraction:
    def test_extracts_full_name(self, handler, mock_forwarder, raw_telegram_text_message):
        handler.handle(raw_telegram_text_message)

        msg = mock_forwarder.forward.call_args[0][0]
        assert msg.sender_name == "John Doe"

    def test_extracts_first_name_only(self, handler, mock_forwarder):
        msg = MagicMock()
        msg.text = "Hi"
        msg.photo = None
        msg.chat.title = "Chat"
        msg.from_user.first_name = "Alice"
        msg.from_user.last_name = ""

        handler.handle(msg)

        forwarded = mock_forwarder.forward.call_args[0][0]
        assert forwarded.sender_name == "Alice"

    def test_defaults_to_unknown(self, handler, mock_forwarder):
        msg = MagicMock()
        msg.text = "Hi"
        msg.photo = None
        msg.chat.title = "Chat"
        msg.from_user = None

        handler.handle(msg)

        forwarded = mock_forwarder.forward.call_args[0][0]
        assert forwarded.sender_name == "Unknown"


class TestErrorHandling:
    def test_catches_bot_base_error(
        self, handler, mock_forwarder, raw_telegram_text_message
    ):
        mock_forwarder.forward.side_effect = TelegramFileRetrievalError("fail")

        handler.handle(raw_telegram_text_message)

    def test_catches_unexpected_error(
        self, handler, mock_forwarder, raw_telegram_text_message
    ):
        mock_forwarder.forward.side_effect = RuntimeError("unexpected")

        handler.handle(raw_telegram_text_message)
