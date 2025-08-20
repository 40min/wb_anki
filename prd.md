### **WB_Anki: Anki Card Creator CLI**

#### **1. Project Goal**

Create a command-line Python script that automates the creation of Anki flashcards from a list of words and their translations. The script will use the AnkiConnect plugin's REST API to interact with the Anki desktop application. It will handle input from either a file or standard input, check for existing decks and cards, and provide a summary report of its actions.

#### **2. Core Requirements**

*   **Input Handling:** The script must accept a list of word pairs from two sources:
    *   A specified file path (`--file <path>`).
    *   Standard input (piped data).
*   **Input Parsing:**
    *   Each line in the input represents a word pair.
    *   The delimiter between the word and its translation can be one or more dashes (`-`, `--`, `---`, etc.).
    *   The script should trim any leading/trailing whitespace from the words and translations.
*   **Anki Integration:**
    *   The script must communicate with Anki via the AnkiConnect API (default URL: `http://localhost:8765`).
    *   It should allow the user to specify the target Anki deck using a command-line argument (`--deck-name <name>`). If not provided, it should fall back to a default value (e.g., from a `.env` file or a hardcoded default).
*   **Card Creation Logic:**
    *   **Deck Verification:** Before processing, the script must verify that the target deck exists in Anki. If it doesn't, the script should ask for user confirmation to create it.
    *   **Duplicate Checking:** For each word pair, the script must check if a card with the "Front" word already exists *in that specific deck*.
    *   **Conditional Card Addition:** If the card does not already exist, the script should add two new cards (notes) to ensure bidirectional learning:
        1.  Card 1: Front -> Back (e.g., `huvudsats` -> `main clause`)
        2.  Card 2: Back -> Front (e.g., `main clause` -> `huvudsats`)
*   **Reporting:** After processing all word pairs, the script must print a summary report to the console, indicating the status of each word:
    *   `✅ (added)`: The word was successfully added.
    *   `☑️ (exists)`: The word already existed in the deck.
    *   `❌ (error)`: An error occurred during processing.

---

### **3. Technical Implementation Details & AnkiConnect API Examples**

The script will need to make HTTP POST requests to the AnkiConnect server. Here are the key API actions and examples of the required JSON payloads.

#### **Action: Check if Deck Exists**

*   **API Endpoint:** `deckNames`
*   **Purpose:** To get a list of all available deck names.
*   **Example Request:**
    ```json
    {
        "action": "deckNames",
        "version": 6
    }
    ```
*   **Example Success Response:**
    ```json
    {
        "result": ["Default", "Swedish::Vocabulary", "Swedish::Grammar"],
        "error": null
    }
    ```
*   **Implementation:** Fetch the list of deck names and check if the target deck name is present in the `result` array.

#### **Action: Create Deck (If it doesn't exist)**

*   **API Endpoint:** `createDeck`
*   **Purpose:** To create a new deck.
*   **Example Request:**
    ```json
    {
        "action": "createDeck",
        "version": 6,
        "params": {
            "deck": "Swedish::Vocabulary"
        }
    }
    ```
*   **Example Success Response:**
    ```json
    {
        "result": 1652889434737, // Deck ID
        "error": null
    }
    ```

#### **Action: Check if a Card Already Exists**

*   **API Endpoint:** `findNotes`
*   **Purpose:** To find notes based on a query. This is the most reliable way to check for duplicates.
*   **Example Request (searching for "huvudsats" in the "Swedish::Vocabulary" deck):**
    ```json
    {
        "action": "findNotes",
        "version": 6,
        "params": {
            "query": "deck:\"Swedish::Vocabulary\" Front:huvudsats"
        }
    }
    ```
*   **Example Success Response (if found):**
    ```json
    {
        "result": [1502298033753], // An array of Note IDs
        "error": null
    }
    ```
*   **Implementation:** If the `result` array is not empty, it means the note already exists.

#### **Action: Add a New Note (Creates Cards)**

*   **API Endpoint:** `addNote`
*   **Purpose:** To add a new note. Anki will automatically generate cards based on the note type. For a basic note type, this will create one card. For a "Basic (and reversed card)" note type, it will create two.
*   **Example Request:**
    ```json
    {
        "action": "addNote",
        "version": 6,
        "params": {
            "note": {
                "deckName": "Swedish::Vocabulary",
                "modelName": "Basic (and reversed card)",
                "fields": {
                    "Front": "huvudsats",
                    "Back": "main clause"
                },
                "options": {
                    "allowDuplicate": false
                },
                "tags": [
                    "swedish_script"
                ]
            }
        }
    }
    ```
*   **Implementation:** Use the `Basic (and reversed card)` model to automatically create both forward and reverse cards. Set `allowDuplicate` to `false` as a safeguard, although our primary check is the `findNotes` call.

---

### **4. Command-Line Interface (CLI) Specification**

The script should be executable from the command line and support the following arguments:

*   `--deck-name`: (Required) The name of the Anki deck to add cards to.
*   `--file`: (Optional) The path to a text file containing word pairs.
*   If the `--file` argument is not provided, the script should read from standard input.

#### **Example Usage:**

```bash
# From a file
python anki_importer.py --deck-name "Swedish" --file "vocabulary.txt"

# From standard input (piping)
cat vocabulary.txt | python anki_importer.py --deck-name "Swedish"

# From standard input (manual entry)
python anki_importer.py --deck-name "Swedish"
> huvudsats -- main clause
> bisats - subordinate clause
> (Press Ctrl+D to end input)
```

---

### **5. Final Report Format**

The script should conclude by printing a summary of its operations.

#### **Example Output:**

```
Processing complete.

Report:
- huvudsats -- main clause: ✅ (added)
- bisats -- subordinate clause: ✅ (added)
- stryk under -- underline: ☑️ (exists)
- varandra -- each other: ❌ (error: failed to connect to Anki)

Summary: 2 added, 1 already existed, 1 failed.
```