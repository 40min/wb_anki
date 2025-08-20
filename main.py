#!/usr/bin/env python3
"""
WB_Anki: Anki Card Creator CLI
Main entry point for the WB_Anki application.
"""

import sys

from src.wb_anki.cli.cli import main

if __name__ == "__main__":
    sys.exit(main())
