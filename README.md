# WB_Anki: Anki Card Creator CLI

A command-line Python script that automates the creation of Anki flashcards from word pairs using the AnkiConnect API.

![Python](https://img.shields.io/badge/python-3.13+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## Features

- ✅ **Bidirectional Cards**: Automatically creates both forward and reverse cards for complete learning
- ✅ **Duplicate Detection**: Checks for existing cards before adding to prevent duplicates
- ✅ **Flexible Input**: Accepts input from files or stdin (pipe support)
- ✅ **Multiple Delimiters**: Supports `-`, `--`, `---`, and tab delimiters
- ✅ **Deck Management**: Auto-creates decks if they don't exist
- ✅ **Rich UI**: Beautiful progress bars and colored status reports
- ✅ **Error Handling**: Comprehensive error reporting and recovery

## Requirements

- Python 3.13 or higher
- Anki desktop application with [AnkiConnect](https://ankiweb.net/shared/info/2055492159) plugin installed
- AnkiConnect plugin running (default: `http://localhost:8765`)

## Installation

### Prerequisites

This project uses [uv](https://docs.astral.sh/uv/) as the package manager. Install uv first:

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### From Source

```bash
# Clone the repository
git clone https://github.com/wb-anki/wb-anki.git
cd wb-anki

# Install the package in editable mode
uv pip install -e .
```

### Using Makefile (Recommended)

The project includes a Makefile with useful commands for development and maintenance:

```bash
# Install all dependencies (production + development)
make install-all

# Run tests
make test

# Run code quality checks
make check

# Format code
make format

# Display all available commands
make help
```

### Dependencies

The following Python packages are required (managed by uv):
- `click>=8.0.0` - Command-line interface
- `httpx>=0.24.0` - HTTP client for AnkiConnect API
- `rich>=13.0.0` - Rich terminal output
- `python-dotenv>=1.0.0` - Environment variable support

## Setup

1. **Install Anki**: Download and install [Anki](https://apps.ankiweb.net/)

2. **Install AnkiConnect**: 
   - Open Anki
   - Go to Tools → Add-ons
   - Click "Get Add-ons..."
   - Enter code: `2055492159`
   - Restart Anki

3. **Configure AnkiConnect** (optional):
   - Create a `.env` file in the project root:
   ```env
   ANKI_URL=http://localhost:8765
   DEFAULT_DECK_NAME=WB_Anki
   ANKI_TIMEOUT=30.0
   DEBUG=false
   ```

## Usage

### Command Line Options

```
wb-anki --deck-name DECK [OPTIONS]

Options:
  --deck-name TEXT          Name of the Anki deck to add cards to [required]
  --file PATH              Path to text file containing word pairs
  --anki-url TEXT          AnkiConnect API URL (default: http://localhost:8765)
  --create-deck / --no-create-deck  
                           Automatically create deck if it does not exist (default: True)
  --version                Show the version and exit
  --help                   Show this message and exit
```

### Input Format

Each line should contain a word pair separated by one or more dashes (`-`, `--`, `---`) or tabs:

```
hello - hej
goodbye -- hej då  
thank you --- tack så mycket
word	translation
```

### Examples

#### From File
```bash
# Basic usage
wb-anki --deck-name "Swedish Vocabulary" --file vocabulary.txt

# Custom AnkiConnect URL
wb-anki --deck-name "Spanish" --file words.txt --anki-url http://localhost:9999

# Prevent automatic deck creation
wb-anki --deck-name "French" --file french.txt --no-create-deck
```

#### From Standard Input (Pipe)
```bash
# From another command
cat vocabulary.txt | wb-anki --deck-name "Swedish"

# From echo
echo "hello - hej" | wb-anki --deck-name "Swedish"
```

#### Interactive Input
```bash
# Type words manually
wb-anki --deck-name "Swedish"
# Then type:
> hello - hej
> goodbye - hej då
> (Press Ctrl+D on Unix/Linux/Mac or Ctrl+Z on Windows to finish)
```

### Using uv to run the CLI

```bash
# Run the CLI directly with uv
uv run wb-anki --deck-name "Swedish" --file vocabulary.txt
```

## Output Example

```
✅ Created deck: Swedish Vocabulary
Processing 3 word pairs...
Processing word pairs... ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:01

                    Processing Results                    
┏━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┓
┃ Word               ┃ Translation              ┃ Status       ┃
┡━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━┩
│ hello              │ hej                      │ ✅ Added     │
│ goodbye            │ hej då                   │ ✅ Added     │
│ thank you          │ tack så mycket           │ ☑️ Exists    │
└────────────────────┴──────────────────────────┴──────────────┘

Summary: 2 added, 1 already existed, 0 failed
```

## Card Types Created

The application creates **bidirectional cards** using Anki's "Basic (and reversed card)" note type:

1. **Forward Card**: `word` → `translation`
2. **Reverse Card**: `translation` → `word`

This ensures you can practice both recognition and recall of vocabulary.

## Development

### Setting up Development Environment

```bash
# Clone the repository
git clone https://github.com/wb-anki/wb-anki.git
cd wb-anki

# Install development dependencies using uv
uv pip install -e .
```

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src --cov-report=term-missing

# Run specific test file
uv run pytest tests/test_parser.py
```

### Using Makefile for Development

```bash
# Install all dependencies (production + development)
make install-all

# Run tests
make test

# Run code quality checks
make check

# Format code
make format

# Display all available commands
make help
```

### Code Quality

```bash
# Format code
make format

# Run all code quality checks
make check

# Run individual checks
make lint
make type-check
```

## Project Structure

```
wb-anki/
├── wb_anki/                # Main package directory
│   ├── __init__.py         # Package initialization
│   ├── cli.py              # Command-line interface
│   ├── anki_client.py      # AnkiConnect client
│   ├── config.py           # Configuration
│   └── parser.py           # Word pair parsing
├── main.py                 # Main entry point (for direct execution)
├── Makefile                # Development and maintenance commands
├── tests/                  # Unit tests
├── pyproject.toml          # Project configuration (uv-based)
└── README.md               # This file
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass (`make test`)
6. Format your code (`make format`)
7. Commit your changes (`git commit -m 'Add amazing feature'`)
8. Push to the branch (`git push origin feature/amazing-feature`)
9. Open a Pull Request

## Troubleshooting

### Common Issues

**AnkiConnect not responding**
- Make sure Anki is running
- Verify AnkiConnect plugin is installed and enabled
- Check if AnkiConnect is listening on the correct port (default: 8765)

**Deck creation fails**
- Ensure Anki is running and accessible
- Check deck name doesn't contain special characters that Anki doesn't support
- Verify you have permission to create decks

**Cards not appearing as expected**
- Ensure you have the "Basic (and reversed card)" note type in Anki
- Check if similar cards already exist (duplicate detection)

**Import fails with file not found**
- Verify the file path is correct
- Ensure the file has read permissions
- Check the file encoding is UTF-8

### Debug Mode

Enable debug mode by setting the environment variable:

```bash
export DEBUG=true
uv run wb-anki --deck-name "Test" --file test.txt
```

## License

This project is licensed under the MIT License.

## Acknowledgments

- [AnkiConnect](https://foosoft.net/projects/anki-connect/) plugin for providing the API
- [Anki](https://apps.ankiweb.net/) for the amazing flashcard system
- [Rich](https://github.com/Textualize/rich) for beautiful terminal output
- [Click](https://click.palletsprojects.com/) for the CLI framework
- [uv](https://docs.astral.sh/uv/) for fast Python package management