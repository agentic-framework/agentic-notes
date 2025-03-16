# agentic-note

Agent's notebook - Provides note-taking capabilities for the agent

## Overview

Agentic Note is a command-line tool for managing notes. It allows agents to create, view, update, delete, and search notes with support for tagging and organization. Notes are stored in a structured format in the Agentic shared directory.

## Features

- Create notes with title, content, and optional tags
- List all notes or filter by tag
- View detailed note content
- Update existing notes (title, content, tags)
- Delete notes
- Search notes by title and content
- Persistent storage in the Agentic shared directory

## Installation

1. Activate the virtual environment:
   ```bash
   source .venv/bin/activate
   ```

2. Install the package in development mode:
   ```bash
   uv pip install -e .
   ```

This will install the `ag-note` command-line tool.

## Usage

The `agentic-note` tool can be used in two ways:

1. As a standalone command: `ag-note`
2. As a subcommand of the Agentic framework: `ag note`

### Creating a Note

```bash
ag note create "Note Title" "Note content goes here" --tags tag1,tag2
```

### Listing Notes

List all notes:
```bash
ag note list
```

List notes with a specific tag:
```bash
ag note list --tag tag1
```

### Viewing a Note

```bash
ag note view note-id
```

### Updating a Note

```bash
ag note update note-id --title "New Title" --content "New content" --tags tag1,tag3
```

You can update any combination of title, content, and tags.

### Deleting a Note

```bash
ag note delete note-id
```

### Searching Notes

```bash
ag note search "query"
```

## Storage

Notes are stored in the Agentic shared directory at `$HOME/Agentic/shared/notes`. Each note is stored as a separate JSON file, with an index file (`index.json`) that maintains metadata for quick listing and searching.

## Development

### Directory Structure

```
agentic-note/
├── .venv/                 # Virtual environment (not in version control)
├── src/                   # Source code
│   └── agentic_note/      # Main package
│       ├── __init__.py    # Package initialization
│       ├── note.py        # Core note functionality
│       └── cli.py         # Command-line interface
├── tests/                 # Test files
├── docs/                  # Documentation
├── data/                  # Data files
├── notebooks/             # Jupyter notebooks
├── .gitignore             # Git ignore file
├── README.md              # This file
├── LICENSE                # License file
└── pyproject.toml         # Project configuration
```

### Running Tests

```bash
pytest
```

## License

See the [LICENSE](LICENSE) file for details.
