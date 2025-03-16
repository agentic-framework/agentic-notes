# Agentic Note Usage Guide

This guide provides detailed instructions on how to use the Agentic Note tool for managing notes.

## Installation

1. Activate the virtual environment:
   ```bash
   source .venv/bin/activate
   ```

2. Install the package in development mode:
   ```bash
   uv pip install -e .
   ```

This will install both the standalone `ag-note` command and the `ag note` subcommand.

## Usage Methods

The Agentic Note tool can be used in two ways:

1. As a standalone command: `ag-note`
2. As a subcommand of the Agentic framework: `ag note`

Both methods provide the same functionality, but the `ag note` method integrates with the Agentic framework's command structure.

## Basic Usage

The command provides several subcommands for managing notes:

```bash
ag note [command] [options]
```

To see the available commands and options:

```bash
ag note --help
```

## Creating Notes

To create a new note:

```bash
ag note create "Note Title" "Note content goes here"
```

You can also add tags to your note:

```bash
ag note create "Note Title" "Note content goes here" --tags tag1,tag2,tag3
```

Tags are optional and can be used to organize and filter your notes.

## Listing Notes

To list all notes:

```bash
ag note list
```

To list notes with a specific tag:

```bash
ag note list --tag tag1
```

The list command displays the ID, title, tags, and last updated time for each note.

## Viewing Notes

To view the full content of a note:

```bash
ag note view note-id
```

Replace `note-id` with the ID of the note you want to view. You can find the ID by using the `list` command.

## Updating Notes

To update a note:

```bash
ag note update note-id --title "New Title" --content "New content" --tags tag1,tag3
```

You can update any combination of title, content, and tags. Only the specified fields will be updated.

## Deleting Notes

To delete a note:

```bash
ag note delete note-id
```

This action is permanent and cannot be undone.

## Searching Notes

To search for notes by title or content:

```bash
ag note search "query"
```

The search is case-insensitive and will match any part of the title or content.

## Storage

Notes are stored in the Agentic shared directory at `$HOME/Agentic/shared/notes`. Each note is stored as a separate JSON file, with an index file (`index.json`) that maintains metadata for quick listing and searching.

## Examples

Here are some examples of how to use the command:

### Creating a note about a meeting

```bash
ag note create "Meeting with Team" "Discussed project timeline and assigned tasks." --tags meeting,project
```

### Listing all meeting notes

```bash
ag note list --tag meeting
```

### Updating a note with new information

```bash
ag note update note-id --content "Discussed project timeline and assigned tasks. Follow-up meeting scheduled for next week."
```

### Searching for notes about a project

```bash
ag note search "project"
```

## Troubleshooting

If you encounter any issues with the command:

1. Make sure you have activated the virtual environment.
2. Check that the package is installed correctly.
3. Verify that the `$HOME/Agentic/shared/notes` directory exists and is writable.
4. If the command is not found, try reinstalling the package.
5. If using the `ag note` command, ensure that the Agentic framework is properly installed and configured.
