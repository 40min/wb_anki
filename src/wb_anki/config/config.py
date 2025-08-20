"""Environment configuration module for WB_Anki."""

import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Configuration class for WB_Anki."""

    ANKI_URL: str = os.getenv("ANKI_URL", "http://localhost:8765")
    DEFAULT_DECK_NAME: str = os.getenv("DEFAULT_DECK_NAME", "WB_Anki")
    TIMEOUT: float = float(os.getenv("ANKI_TIMEOUT", "30.0"))
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"

    @classmethod
    def validate(cls) -> bool:
        """Validate configuration values."""
        if not cls.ANKI_URL:
            raise ValueError("ANKI_URL must be provided")
        if not cls.DEFAULT_DECK_NAME:
            raise ValueError("DEFAULT_DECK_NAME must be provided")
        return True
