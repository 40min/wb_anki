"""Tests for the configuration module."""

import os
from unittest.mock import patch

import pytest

from src.wb_anki.config.config import Config


class TestConfig:
    """Test cases for Config class."""

    @patch.dict(os.environ, {}, clear=True)
    def test_default_values(self):
        """Test that default configuration values are set correctly."""
        # Clear any cached module and re-import
        import importlib

        from src.wb_anki.config import config

        importlib.reload(config)

        assert config.Config.ANKI_URL == "http://localhost:8765"
        assert config.Config.DEFAULT_DECK_NAME == "WB_Anki"
        assert config.Config.TIMEOUT == 30.0
        assert config.Config.DEBUG is False

    @patch.dict(
        os.environ,
        {"ANKI_URL": "http://localhost:9999", "DEFAULT_DECK_NAME": "TestDeck", "ANKI_TIMEOUT": "60.0", "DEBUG": "true"},
        clear=True,
    )
    def test_environment_variables(self):
        """Test that environment variables override defaults."""
        # Clear any cached module and re-import
        import importlib

        from src.wb_anki.config import config

        importlib.reload(config)

        assert config.Config.ANKI_URL == "http://localhost:9999"
        assert config.Config.DEFAULT_DECK_NAME == "TestDeck"
        assert config.Config.TIMEOUT == 60.0
        assert config.Config.DEBUG is True

    def test_validate_success(self):
        """Test successful validation."""
        result = Config.validate()
        assert result is True

    @patch.object(Config, "ANKI_URL", "")
    def test_validate_empty_anki_url(self):
        """Test validation fails with empty ANKI_URL."""
        with pytest.raises(ValueError, match="ANKI_URL must be provided"):
            Config.validate()

    @patch.object(Config, "DEFAULT_DECK_NAME", "")
    def test_validate_empty_deck_name(self):
        """Test validation fails with empty DEFAULT_DECK_NAME."""
        with pytest.raises(ValueError, match="DEFAULT_DECK_NAME must be provided"):
            Config.validate()
