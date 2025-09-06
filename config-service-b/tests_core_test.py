"""
Tests for core modules.
"""
import unittest
from unittest.mock import patch

from app.core.config import Settings, get_settings, setup_logging


class TestConfig(unittest.TestCase):

    @patch('app.core.config.BaseSettings')
    def test_settings_creation(self, mock_base_settings):
        """Test settings creation."""
        mock_base_settings.return_value.db_host = 'localhost'
        mock_base_settings.return_value.db_port = 5432

        settings = Settings()
        self.assertEqual(settings.db_host, 'localhost')
        self.assertEqual(settings.db_port, 5432)

    def test_get_settings(self):
        """Test get_settings function."""
        settings = get_settings()
        self.assertIsInstance(settings, Settings)

    @patch('logging.basicConfig')
    def test_setup_logging(self, mock_basic_config):
        """Test logging setup."""
        setup_logging('DEBUG')
        mock_basic_config.assert_called_once()
        args, kwargs = mock_basic_config.call_args
        self.assertEqual(kwargs['level'], 10)  # DEBUG level


if __name__ == '__main__':
    unittest.main()
