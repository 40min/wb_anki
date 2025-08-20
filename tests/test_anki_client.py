"""Tests for the AnkiConnect client module."""

from unittest.mock import Mock, patch

import httpx
import pytest

from src.wb_anki.client.anki_client import AnkiConnectClient


class TestAnkiConnectClient:
    """Test cases for AnkiConnectClient class."""

    def test_init_default_url(self):
        """Test client initialization with default URL."""
        with patch("src.wb_anki.client.anki_client.Config") as mock_config:
            mock_config.ANKI_URL = "http://localhost:8765"
            mock_config.TIMEOUT = 30.0

            client = AnkiConnectClient()
            assert client.anki_url == "http://localhost:8765"

    def test_init_custom_url(self):
        """Test client initialization with custom URL."""
        with patch("src.wb_anki.client.anki_client.Config"):
            client = AnkiConnectClient("http://custom:9999")
            assert client.anki_url == "http://custom:9999"

    @patch("httpx.Client")
    def test_context_manager(self, mock_client_class):
        """Test context manager functionality."""
        mock_client = Mock()
        mock_client_class.return_value = mock_client

        with AnkiConnectClient() as client:
            assert client is not None

        mock_client.close.assert_called_once()

    @patch("httpx.Client")
    def test_make_request_success(self, mock_client_class):
        """Test successful API request."""
        mock_response = Mock()
        mock_response.json.return_value = {"result": ["deck1", "deck2"], "error": None}
        mock_response.raise_for_status.return_value = None

        mock_client = Mock()
        mock_client.post.return_value = mock_response
        mock_client_class.return_value = mock_client

        with AnkiConnectClient() as client:
            result = client._make_request("deckNames")

        expected_payload = {"action": "deckNames", "version": 6, "params": {}}
        mock_client.post.assert_called_once_with(client.anki_url, json=expected_payload)
        assert result == {"result": ["deck1", "deck2"], "error": None}

    @patch("httpx.Client")
    def test_make_request_with_params(self, mock_client_class):
        """Test API request with parameters."""
        mock_response = Mock()
        mock_response.json.return_value = {"result": 123, "error": None}
        mock_response.raise_for_status.return_value = None

        mock_client = Mock()
        mock_client.post.return_value = mock_response
        mock_client_class.return_value = mock_client

        with AnkiConnectClient() as client:
            client._make_request("createDeck", {"deck": "TestDeck"})

        expected_payload = {"action": "createDeck", "version": 6, "params": {"deck": "TestDeck"}}
        mock_client.post.assert_called_once_with(client.anki_url, json=expected_payload)

    @patch("httpx.Client")
    def test_make_request_api_error(self, mock_client_class):
        """Test API request with API error response."""
        mock_response = Mock()
        mock_response.json.return_value = {"result": None, "error": "API Error Message"}
        mock_response.raise_for_status.return_value = None

        mock_client = Mock()
        mock_client.post.return_value = mock_response
        mock_client_class.return_value = mock_client

        with AnkiConnectClient() as client:
            with pytest.raises(Exception, match="API Error Message"):
                client._make_request("deckNames")

    @patch("httpx.Client")
    def test_make_request_connection_error(self, mock_client_class):
        """Test API request with connection error."""
        mock_client = Mock()
        mock_client.post.side_effect = httpx.RequestError("Connection failed")
        mock_client_class.return_value = mock_client

        with AnkiConnectClient() as client:
            with pytest.raises(Exception, match="Error connecting to Anki"):
                client._make_request("deckNames")

    @patch("httpx.Client")
    def test_get_deck_names(self, mock_client_class):
        """Test getting deck names."""
        mock_response = Mock()
        mock_response.json.return_value = {"result": ["Default", "Swedish"], "error": None}
        mock_response.raise_for_status.return_value = None

        mock_client = Mock()
        mock_client.post.return_value = mock_response
        mock_client_class.return_value = mock_client

        with AnkiConnectClient() as client:
            result = client.get_deck_names()

        assert result == ["Default", "Swedish"]

    @patch("httpx.Client")
    def test_deck_exists_true(self, mock_client_class):
        """Test deck exists returns True when deck is found."""
        mock_response = Mock()
        mock_response.json.return_value = {"result": ["Default", "Swedish"], "error": None}
        mock_response.raise_for_status.return_value = None

        mock_client = Mock()
        mock_client.post.return_value = mock_response
        mock_client_class.return_value = mock_client

        with AnkiConnectClient() as client:
            result = client.deck_exists("Swedish")

        assert result is True

    @patch("httpx.Client")
    def test_deck_exists_false(self, mock_client_class):
        """Test deck exists returns False when deck is not found."""
        mock_response = Mock()
        mock_response.json.return_value = {"result": ["Default"], "error": None}
        mock_response.raise_for_status.return_value = None

        mock_client = Mock()
        mock_client.post.return_value = mock_response
        mock_client_class.return_value = mock_client

        with AnkiConnectClient() as client:
            result = client.deck_exists("Swedish")

        assert result is False

    @patch("httpx.Client")
    def test_card_exists_true(self, mock_client_class):
        """Test card exists returns True when card is found."""
        mock_response = Mock()
        mock_response.json.return_value = {"result": [123456], "error": None}
        mock_response.raise_for_status.return_value = None

        mock_client = Mock()
        mock_client.post.return_value = mock_response
        mock_client_class.return_value = mock_client

        with AnkiConnectClient() as client:
            result = client.card_exists("Swedish", "hello")

        assert result is True

    @patch("httpx.Client")
    def test_card_exists_false(self, mock_client_class):
        """Test card exists returns False when card is not found."""
        mock_response = Mock()
        mock_response.json.return_value = {"result": [], "error": None}
        mock_response.raise_for_status.return_value = None

        mock_client = Mock()
        mock_client.post.return_value = mock_response
        mock_client_class.return_value = mock_client

        with AnkiConnectClient() as client:
            result = client.card_exists("Swedish", "hello")

        assert result is False
