from unittest.mock import MagicMock

import pytest

from src.clients.interfaces import GoogleChatClientInterface, TelegramClientInterface
from src.config.settings import BotSettings
from src.models.message import ForwardableMessage, PhotoData


@pytest.fixture
def test_settings():
    return BotSettings(
        telegram_token="test-token-123",
        google_chat_webhook="https://chat.googleapis.com/v1/spaces/test/messages?key=k&token=t",
        port=5000,
        log_level="DEBUG",
    )


@pytest.fixture
def mock_telegram_client():
    mock = MagicMock(spec=TelegramClientInterface)
    mock.resolve_photo_url.return_value = (
        "https://api.telegram.org/file/bottest-token-123/photos/file_1.jpg"
    )
    return mock


@pytest.fixture
def mock_google_chat_client():
    return MagicMock(spec=GoogleChatClientInterface)


@pytest.fixture
def sample_text_message():
    return ForwardableMessage(
        text="Hello world",
        sender_name="Test User",
        chat_title="Test Chat",
    )


@pytest.fixture
def sample_photo_message():
    return ForwardableMessage(
        photo=PhotoData(
            file_url="https://api.telegram.org/file/bottest-token-123/photos/file_1.jpg",
            caption="Test caption",
        ),
        sender_name="Test User",
        chat_title="Test Chat",
    )


@pytest.fixture
def sample_photo_message_no_caption():
    return ForwardableMessage(
        photo=PhotoData(
            file_url="https://api.telegram.org/file/bottest-token-123/photos/file_1.jpg",
        ),
        sender_name="Test User",
        chat_title="Test Chat",
    )


@pytest.fixture
def raw_telegram_text_message():
    msg = MagicMock()
    msg.text = "Hello from Telegram"
    msg.photo = None
    msg.caption = None
    msg.chat.title = "My Group"
    msg.from_user.first_name = "John"
    msg.from_user.last_name = "Doe"
    return msg


@pytest.fixture
def raw_telegram_photo_message():
    photo_size = MagicMock()
    photo_size.file_id = "AgACAgIAAx0CZ"

    msg = MagicMock()
    msg.text = None
    msg.photo = [MagicMock(), photo_size]
    msg.caption = "Nice photo"
    msg.chat.title = "My Group"
    msg.from_user.first_name = "Jane"
    msg.from_user.last_name = "Smith"
    return msg
