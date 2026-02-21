import pytest
from pydantic import ValidationError

from src.config.settings import BotSettings


class TestBotSettings:
    def test_loads_required_fields(self, monkeypatch):
        monkeypatch.setenv("TELEGRAM_TOKEN", "tok-123")
        monkeypatch.setenv("GOOGLE_CHAT_WEBHOOK", "https://chat.example.com/webhook")

        settings = BotSettings()

        assert settings.telegram_token == "tok-123"
        assert settings.google_chat_webhook == "https://chat.example.com/webhook"

    def test_applies_defaults(self, monkeypatch):
        monkeypatch.setenv("TELEGRAM_TOKEN", "tok-123")
        monkeypatch.setenv("GOOGLE_CHAT_WEBHOOK", "https://chat.example.com/webhook")

        settings = BotSettings()

        assert settings.port == 5000
        assert settings.log_level == "INFO"
        assert settings.telegram_api_base_url == "https://api.telegram.org"

    def test_overrides_defaults(self, monkeypatch):
        monkeypatch.setenv("TELEGRAM_TOKEN", "tok-123")
        monkeypatch.setenv("GOOGLE_CHAT_WEBHOOK", "https://chat.example.com/webhook")
        monkeypatch.setenv("PORT", "8080")
        monkeypatch.setenv("LOG_LEVEL", "DEBUG")

        settings = BotSettings()

        assert settings.port == 8080
        assert settings.log_level == "DEBUG"

    def test_missing_required_field_raises(self, monkeypatch):
        monkeypatch.delenv("TELEGRAM_TOKEN", raising=False)
        monkeypatch.delenv("GOOGLE_CHAT_WEBHOOK", raising=False)

        with pytest.raises(ValidationError):
            BotSettings()

    def test_missing_telegram_token_raises(self, monkeypatch):
        monkeypatch.delenv("TELEGRAM_TOKEN", raising=False)
        monkeypatch.setenv("GOOGLE_CHAT_WEBHOOK", "https://chat.example.com/webhook")

        with pytest.raises(ValidationError):
            BotSettings()
