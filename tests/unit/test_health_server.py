from src.server.health_server import HealthServer


class TestHealthServer:
    def test_health_check_returns_ok(self, test_settings):
        server = HealthServer(test_settings)

        with server._app.test_client() as client:
            response = client.get("/")

        assert response.status_code == 200
        assert response.data == b"OK"

    def test_starts_in_background(self, test_settings, mocker):
        server = HealthServer(test_settings)
        mock_thread_cls = mocker.patch(
            "src.server.health_server.Thread", autospec=True
        )

        server.start_in_background()

        mock_thread_cls.assert_called_once()
        mock_thread_cls.return_value.start.assert_called_once()
