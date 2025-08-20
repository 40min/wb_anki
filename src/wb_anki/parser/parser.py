"""Word parser module for parsing word pairs from text input."""

import re
from typing import List, Optional, Tuple

import click
from rich.console import Console

console = Console()


def parse_word_pairs(lines: List[str]) -> List[Tuple[str, str]]:
    """Parse word pairs from input lines.

    Args:
        lines: List of input lines to parse

    Returns:
        List of tuples containing (front, back) word pairs

    Example:
        >>> lines = ["hello - hej", "goodbye -- hej då"]
        >>> parse_word_pairs(lines)
        [("hello", "hej"), ("goodbye", "hej då")]
    """
    word_pairs = []

    for line_num, line in enumerate(lines, 1):
        line = line.strip()
        if not line:
            continue

        # Split by one or more dashes or tabs
        parts = re.split(r"[-–—\t]+", line, maxsplit=1)
        if len(parts) != 2:
            console.print(f"[yellow]⚠️ Skipping line {line_num}: invalid format '{line}'[/yellow]")
            continue

        front = parts[0].strip()
        back = parts[1].strip()

        if front and back:
            word_pairs.append((front, back))
        else:
            console.print(f"[yellow]⚠️ Skipping line {line_num}: empty word or translation[/yellow]")

    return word_pairs


def read_input(file_path: Optional[str] = None) -> List[str]:
    """Read input from file or stdin.

    Args:
        file_path: Optional path to input file. If None, reads from stdin.

    Returns:
        List of lines from input

    Raises:
        click.Abort: If file cannot be read
    """
    if file_path:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.readlines()
        except FileNotFoundError:
            console.print(f"[red]❌ File not found: {file_path}[/red]")
            raise click.Abort()
        except Exception as e:
            console.print(f"[red]❌ Error reading file: {e}[/red]")
            raise click.Abort()
    else:
        return click.get_text_stream("stdin").readlines()
