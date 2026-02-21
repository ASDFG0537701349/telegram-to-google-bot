from src.exceptions.base import BotBaseError


class TelegramClientError(BotBaseError):
    pass


class TelegramFileRetrievalError(TelegramClientError):
    pass
