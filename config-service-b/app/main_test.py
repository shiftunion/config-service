"""
Tests for main FastAPI application.
"""
import unittest
from unittest.mock import patch

from app.main import app


class TestMainApp(unittest.TestCase):

    def test_app_creation(self):
        """Test FastAPI app is created correctly."""
        self.assertEqual(app.title, "Config Service API")
        self.assertEqual(app.version, "1.0.0")

    def test_health_endpoint(self):
        """Test health check endpoint."""
        # This would require fastapi.testclient.TestClient in dependencies
        # For now, just test the endpoint exists
        routes = [route.path for route in app.routes]
        self.assertIn("/health", routes)

    @patch('app.core.config.get_settings')
    @patch('app.core.config.setup_logging')
    def test_lifespan_startup(self, mock_setup_logging, mock_get_settings):
        """Test application startup in lifespan."""
        from app.main import lifespan
        import asyncio

        async def run_test():
            async with lifespan(app):
                pass
            mock_get_settings.assert_called_once()
            mock_setup_logging.assert_called_once()

        asyncio.run(run_test())


if __name__ == '__main__':
    unittest.main()
