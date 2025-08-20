"""Tests for the configuration module."""

import os
import sys
from unittest.mock import patch

import pytest

from wb_anki.config import Config


class TestConfig:
    """Test cases for Config class."""

    @patch.dict(os.environ, {}, clear=True)
    def test_default_values(self):
        """Test that default configuration values are set correctly."""

        # Remove the module from cache if it exists
        if "wb_anki.config" in sys.modules:
            del sys.modules["wb_anki.config"]

        # Access Config directly from the module
        from wb_anki.config import Config

        assert Config.ANKI_URL == "http://localhost:8765"
        assert Config.DEFAULT_DECK_NAME == "WB_Anki"
        assert Config.TIMEOUT == 30.0
        assert Config.DEBUG is False

    @patch.dict(
        os.environ,
        {"ANKI_URL": "http://localhost:9999", "DEFAULT_DECK_NAME": "TestDeck", "ANKI_TIMEOUT": "60.0", "DEBUG": "true"},
        clear=True,
    )
    def test_environment_variables(self):
        """Test that environment variables override defaults."""

        # Remove the module from cache if it exists
        if "wb_anki.config" in sys.modules:
            del sys.modules["wb_anki.config"]

        # Access Config directly from the module
        from wb_anki.config import Config

        assert Config.ANKI_URL == "http://localhost:9999"
        assert Config.DEFAULT_DECK_NAME == "TestDeck"
        assert Config.TIMEOUT == 60.0
        assert Config.DEBUG is True

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
