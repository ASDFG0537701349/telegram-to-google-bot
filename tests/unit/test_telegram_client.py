from unittest.mock import MagicMock, patch

import pytest

from src.clients.telegram_client import TelegramClient
from src.config.settings import BotSettings
from src.exceptions.telegram_errors import TelegramFileRetrievalError


@pytest.fixture
def settings():
    return BotSettings(
        telegram_token="test-token-abc",
        google_chat_webhook="https://chat.example.com/webhook",
        telegram_api_base_url="https://api.telegram.org",
    )


@pytest.fixture
def mock_bot():
    with patch("src.clients.telegram_client.telebot.TeleBot") as mock_cls:
        yield mock_cls.return_value


@pytest.fixture
def client(settings, mock_bot):
    with patch("src.clients.telegram_client.telebot.TeleBot", return_value=mock_bot):
        return TelegramClient(settings)


class TestResolvePhotoUrl:
    def test_constructs_correct_url(self, client, mock_bot):
        file_info = MagicMock()
        file_info.file_path = "photos/file_42.jpg"
        mock_bot.get_file.return_value = file_info

        url = client.resolve_photo_url("file-id-42")

        mock_bot.get_file.assert_called_once_with("file-id-42")
        assert url == "https://api.telegram.org/file/bottest-token-abc/photos/file_42.jpg"

    def test_raises_on_telegram_api_error(self, client, mock_bot):
        from telebot.apihelper import ApiTelegramException

        mock_bot.get_file.side_effect = ApiTelegramException(
            "getFile", "Bad Request", {"error_code": 400, "description": "Bad Request"}
        )

        with pytest.raises(TelegramFileRetrievalError):
            client.resolve_photo_url("bad-file-id")


class TestRegisterMessageHandler:
    def test_delegates_to_bot(self, client, mock_bot):
        callback = MagicMock()
        handler_decorator = MagicMock()
        mock_bot.message_handler.return_value = handler_decorator

        client.register_message_handler(callback, ["text", "photo"])

        mock_bot.message_handler.assert_called_once_with(
            content_types=["text", "photo"]
        )
        handler_decorator.assert_called_once_with(callback)


class TestStartPolling:
    def test_calls_bot_polling(self, client, mock_bot):
        client.start_polling()

        mock_bot.polling.assert_called_once_with(none_stop=True)
