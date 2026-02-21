from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class BotSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    telegram_token: str = Field(description="Telegram Bot API token")
    google_chat_webhook: str = Field(description="Google Chat incoming webhook URL")
    port: int = Field(default=5000, description="Flask health server port")
    log_level: str = Field(default="INFO", description="Root log level")
    log_format: str = Field(
        default="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
        description="Log format string",
    )
    telegram_api_base_url: str = Field(
        default="https://api.telegram.org",
        description="Telegram API base URL for file downloads",
    )
