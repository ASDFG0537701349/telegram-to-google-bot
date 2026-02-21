from src.exceptions.base import BotBaseError


class GoogleChatClientError(BotBaseError):
    pass


class GoogleChatWebhookError(GoogleChatClientError):
    pass


class GoogleChatPayloadBuildError(GoogleChatClientError):
    pass
