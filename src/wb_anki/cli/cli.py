"""CLI module for WB_Anki command-line interface."""

from typing import Dict, List, Optional, Tuple

import click
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

from ..client import AnkiConnectClient
from ..parser import parse_word_pairs, read_input

console = Console()


@click.command()
@click.option("--deck-name", required=True, help="Name of the Anki deck to add cards to")
@click.option("--file", type=click.Path(exists=True, readable=True), help="Path to text file containing word pairs")
@click.option(
    "--anki-url", default="http://localhost:8765", help="AnkiConnect API URL (default: http://localhost:8765)"
)
@click.option("--create-deck/--no-create-deck", default=True, help="Automatically create deck if it does not exist")
@click.version_option(version="1.0.0")
def main(deck_name: str, file: Optional[str], anki_url: str, create_deck: bool) -> None:
    """WB_Anki: Anki Card Creator CLI

    Create Anki flashcards from word pairs in text format.

    Input format (one per line):
    word - translation
    hello - hej
    goodbye - hej då

    Examples:

    \b
    # From file
    python -m wb_anki.cli --deck-name Swedish --file vocabulary.txt

    \b
    # From stdin
    cat vocabulary.txt | python -m wb_anki.cli --deck-name Swedish

    \b
    # With custom AnkiConnect URL
    python -m wb_anki.cli --deck-name Spanish --anki-url http://localhost:8765
    """

    try:
        with AnkiConnectClient(anki_url) as client:
            # Check if deck exists
            if not client.deck_exists(deck_name):
                if create_deck:
                    if client.create_deck(deck_name):
                        console.print(f"[green]✅ Created deck: {deck_name}[/green]")
                    else:
                        console.print(f"[red]❌ Failed to create deck: {deck_name}[/red]")
                        raise click.Abort()
                else:
                    console.print(f"[red]❌ Deck '{deck_name}' does not exist and --no-create-deck specified[/red]")
                    raise click.Abort()

            # Read input
            lines = read_input(file)

            # Parse word pairs
            word_pairs = parse_word_pairs(lines)

            if not word_pairs:
                console.print("[red]❌ No valid word pairs found.[/red]")
                raise click.Abort()

            console.print(f"[blue]Processing {len(word_pairs)} word pairs...[/blue]")

            # Process word pairs
            stats, results = process_word_pairs(client, word_pairs, deck_name)

            # Print report
            print_report(stats, results)

            if stats["error"] > 0:
                raise click.Abort()

    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")
        raise click.Abort()


def process_word_pairs(
    client: AnkiConnectClient, word_pairs: List[Tuple[str, str]], deck_name: str
) -> Tuple[Dict[str, int], List[Tuple[str, str, str]]]:
    """Process word pairs and return statistics."""
    stats = {"added": 0, "exists": 0, "error": 0}
    results = []

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Processing word pairs...", total=len(word_pairs))

        for front, back in word_pairs:
            try:
                if client.card_exists(deck_name, front):
                    results.append((front, back, "exists"))
                    stats["exists"] += 1
                else:
                    if client.add_note(deck_name, front, back):
                        results.append((front, back, "added"))
                        stats["added"] += 1
                    else:
                        results.append((front, back, "error"))
                        stats["error"] += 1
            except Exception as e:
                results.append((front, back, "error"))
                stats["error"] += 1
                console.print(f"[red]❌ Error processing '{front}': {e}[/red]")

            progress.advance(task)

    return stats, results


def print_report(stats: Dict[str, int], results: List[Tuple[str, str, str]]) -> None:
    """Print the final report."""
    console.print("\n[bold green]Processing complete![/bold green]\n")

    if results:
        table = Table(title="Processing Results")
        table.add_column("Word", style="cyan")
        table.add_column("Translation", style="magenta")
        table.add_column("Status", style="green")

        for front, back, status in results:
            if status == "added":
                table.add_row(front, back, "[green]✅ Added[/green]")
            elif status == "exists":
                table.add_row(front, back, "[blue]☑️ Exists[/blue]")
            elif status == "error":
                table.add_row(front, back, "[red]❌ Error[/red]")

        console.print(table)

    console.print(
        f"\n[bold]Summary:[/bold] {stats['added']} added, {stats['exists']} already existed, {stats['error']} failed"
    )


if __name__ == "__main__":
    main()
