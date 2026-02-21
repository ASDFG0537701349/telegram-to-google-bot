from unittest.mock import MagicMock, patch


class TestMain:
    @patch("src.main.BotSettings")
    @patch("src.main.configure_logging")
    @patch("src.main.TelegramClient")
    @patch("src.main.GoogleChatWebhookClient")
    @patch("src.main.MessageForwarder")
    @patch("src.main.TelegramMessageHandler")
    @patch("src.main.HealthServer")
    def test_wires_all_components(
        self,
        mock_health_server_cls,
        mock_handler_cls,
        mock_forwarder_cls,
        mock_google_cls,
        mock_telegram_cls,
        mock_logging,
        mock_settings_cls,
    ):
        mock_settings = MagicMock()
        mock_settings_cls.return_value = mock_settings

        from src.main import main

        main()

        mock_settings_cls.assert_called_once()
        mock_logging.assert_called_once_with(mock_settings)
        mock_telegram_cls.assert_called_once_with(mock_settings)
        mock_google_cls.assert_called_once_with(mock_settings)
        mock_forwarder_cls.assert_called_once_with(mock_google_cls.return_value)
        mock_handler_cls.assert_called_once_with(
            mock_telegram_cls.return_value,
            mock_forwarder_cls.return_value,
        )
        mock_telegram_cls.return_value.register_message_handler.assert_called_once()
        mock_health_server_cls.return_value.start_in_background.assert_called_once()
        mock_telegram_cls.return_value.start_polling.assert_called_once()
