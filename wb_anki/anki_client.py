"""AnkiConnect client module for interacting with Anki API."""

from typing import Any, Dict, List, Optional

import httpx

from .config import Config


class AnkiConnectClient:
    """Client for interacting with AnkiConnect API."""

    def __init__(self, anki_url: Optional[str] = None):
        self.anki_url = anki_url or Config.ANKI_URL
        self.client = httpx.Client(timeout=Config.TIMEOUT)

    def __enter__(self) -> "AnkiConnectClient":
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.client.close()

    def _make_request(self, action: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a request to AnkiConnect API."""
        payload = {"action": action, "version": 6, "params": params or {}}

        try:
            response = self.client.post(self.anki_url, json=payload)
            response.raise_for_status()
            data = response.json()

            if data.get("error"):
                raise Exception(data["error"])

            return data  # type: ignore[no-any-return]
        except httpx.RequestError as e:
            raise Exception(f"Error connecting to Anki: {e}")
        except Exception as e:
            raise Exception(f"API Error: {e}")

    def get_deck_names(self) -> List[str]:
        """Get list of all deck names."""
        result = self._make_request("deckNames")
        return result.get("result", [])  # type: ignore[no-any-return]

    def deck_exists(self, deck_name: str) -> bool:
        """Check if a deck exists."""
        return deck_name in self.get_deck_names()

    def create_deck(self, deck_name: str) -> bool:
        """Create a new deck."""
        try:
            result = self._make_request("createDeck", {"deck": deck_name})
            return result.get("error") is None
        except Exception:
            return False

    def find_notes(self, query: str) -> List[str]:
        """Find notes matching a query."""
        result = self._make_request("findNotes", {"query": query})
        return result.get("result", [])  # type: ignore[no-any-return]

    def card_exists(self, deck_name: str, front: str) -> bool:
        """Check if a card with given front text exists."""
        try:
            query = f'deck:"{deck_name}" Front:"{front}"'
            notes = self.find_notes(query)
            return len(notes) > 0
        except Exception:
            return False

    def add_note(self, deck_name: str, front: str, back: str) -> bool:
        """Add a new note with bidirectional cards."""
        params = {
            "note": {
                "deckName": deck_name,
                "modelName": "Basic (and reversed card)",
                "fields": {"Front": front, "Back": back},
                "options": {"allowDuplicate": False},
                "tags": ["wb_anki"],
            }
        }

        try:
            result = self._make_request("addNote", params)
            return result.get("error") is None
        except Exception:
            return False
