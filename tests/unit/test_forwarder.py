import pytest

from src.exceptions.base import BotBaseError
from src.exceptions.google_chat_errors import GoogleChatWebhookError
from src.models.message import ForwardableMessage
from src.services.forwarder import MessageForwarder


@pytest.fixture
def forwarder(mock_google_chat_client):
    return MessageForwarder(mock_google_chat_client)


class TestForwardTextMessage:
    def test_routes_text_to_google_chat(
        self, forwarder, mock_google_chat_client, sample_text_message
    ):
        forwarder.forward(sample_text_message)

        mock_google_chat_client.send_text.assert_called_once_with("Hello world")

    def test_does_not_call_send_photo(
        self, forwarder, mock_google_chat_client, sample_text_message
    ):
        forwarder.forward(sample_text_message)

        mock_google_chat_client.send_photo.assert_not_called()


class TestForwardPhotoMessage:
    def test_routes_photo_to_google_chat(
        self, forwarder, mock_google_chat_client, sample_photo_message
    ):
        forwarder.forward(sample_photo_message)

        mock_google_chat_client.send_photo.assert_called_once_with(
            "https://api.telegram.org/file/bottest-token-123/photos/file_1.jpg",
            "Test caption",
        )

    def test_routes_photo_without_caption(
        self, forwarder, mock_google_chat_client, sample_photo_message_no_caption
    ):
        forwarder.forward(sample_photo_message_no_caption)

        mock_google_chat_client.send_photo.assert_called_once_with(
            "https://api.telegram.org/file/bottest-token-123/photos/file_1.jpg",
            None,
        )

    def test_does_not_call_send_text(
        self, forwarder, mock_google_chat_client, sample_photo_message
    ):
        forwarder.forward(sample_photo_message)

        mock_google_chat_client.send_text.assert_not_called()


class TestForwardEmptyMessage:
    def test_skips_empty_message(self, forwarder, mock_google_chat_client):
        empty = ForwardableMessage()

        forwarder.forward(empty)

        mock_google_chat_client.send_text.assert_not_called()
        mock_google_chat_client.send_photo.assert_not_called()


class TestForwardErrorHandling:
    def test_propagates_bot_base_error(
        self, forwarder, mock_google_chat_client, sample_text_message
    ):
        mock_google_chat_client.send_text.side_effect = GoogleChatWebhookError("fail")

        with pytest.raises(GoogleChatWebhookError):
            forwarder.forward(sample_text_message)

    def test_wraps_unexpected_error_in_bot_base_error(
        self, forwarder, mock_google_chat_client, sample_text_message
    ):
        mock_google_chat_client.send_text.side_effect = RuntimeError("boom")

        with pytest.raises(BotBaseError, match="boom"):
            forwarder.forward(sample_text_message)
