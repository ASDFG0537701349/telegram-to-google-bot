from unittest.mock import MagicMock

import pytest

from src.clients.interfaces import GoogleChatClientInterface
from src.exceptions.google_chat_errors import GoogleChatWebhookError
from src.models.message import ForwardableMessage, PhotoData
from src.services.forwarder import MessageForwarder


@pytest.fixture
def recording_google_chat_client():
    client = MagicMock(spec=GoogleChatClientInterface)
    client.calls = []

    def record_text(text):
        client.calls.append(("text", text))

    def record_photo(url, caption):
        client.calls.append(("photo", url, caption))

    client.send_text.side_effect = record_text
    client.send_photo.side_effect = record_photo
    return client


@pytest.fixture
def forwarder(recording_google_chat_client):
    return MessageForwarder(recording_google_chat_client)


class TestTextForwardingFlow:
    def test_text_reaches_google_chat(self, forwarder, recording_google_chat_client):
        message = ForwardableMessage(
            text="Integration test message",
            sender_name="Tester",
            chat_title="Test Chat",
        )

        forwarder.forward(message)

        assert len(recording_google_chat_client.calls) == 1
        assert recording_google_chat_client.calls[0] == ("text", "Integration test message")


class TestPhotoForwardingFlow:
    def test_photo_reaches_google_chat(self, forwarder, recording_google_chat_client):
        message = ForwardableMessage(
            photo=PhotoData(
                file_url="https://api.telegram.org/file/bot123/photo.jpg",
                caption="Integration photo",
            ),
            sender_name="Tester",
            chat_title="Test Chat",
        )

        forwarder.forward(message)

        assert len(recording_google_chat_client.calls) == 1
        assert recording_google_chat_client.calls[0] == (
            "photo",
            "https://api.telegram.org/file/bot123/photo.jpg",
            "Integration photo",
        )


class TestMultipleMessagesFlow:
    def test_forwards_mixed_messages(self, forwarder, recording_google_chat_client):
        text_msg = ForwardableMessage(text="First", sender_name="A")
        photo_msg = ForwardableMessage(
            photo=PhotoData(file_url="https://example.com/img.jpg"),
            sender_name="B",
        )

        forwarder.forward(text_msg)
        forwarder.forward(photo_msg)

        assert len(recording_google_chat_client.calls) == 2
        assert recording_google_chat_client.calls[0] == ("text", "First")
        assert recording_google_chat_client.calls[1] == (
            "photo", "https://example.com/img.jpg", None
        )


class TestErrorRecoveryFlow:
    def test_error_does_not_corrupt_state(self, recording_google_chat_client):
        forwarder = MessageForwarder(recording_google_chat_client)
        recording_google_chat_client.send_text.side_effect = [
            GoogleChatWebhookError("temporary"),
            None,
        ]

        msg = ForwardableMessage(text="Retry me", sender_name="X")

        with pytest.raises(GoogleChatWebhookError):
            forwarder.forward(msg)

        recording_google_chat_client.send_text.side_effect = None
        forwarder.forward(msg)

        assert recording_google_chat_client.send_text.call_count == 2
