"""
Command-line interface for the agentic-note tool.
"""

import argparse
import os
import sys
import textwrap
from typing import List, Optional

from .note import NoteManager


def create_parser() -> argparse.ArgumentParser:
    """Create the command-line argument parser."""
    parser = argparse.ArgumentParser(
        description="Agentic Note - Agent's notebook providing note-taking capabilities",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""
        Examples:
          # Create a new note
          ag note create "Note Title" "Note content goes here" --tags tag1,tag2
          
          # List all notes
          ag note list
          
          # List notes with a specific tag
          ag note list --tag tag1
          
          # View a note
          ag note view note-id
          
          # Update a note
          ag note update note-id --title "New Title" --content "New content" --tags tag1,tag3
          
          # Delete a note
          ag note delete note-id
          
          # Search notes
          ag note search "query"
        """)
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Create command
    create_parser = subparsers.add_parser("create", help="Create a new note")
    create_parser.add_argument("title", help="Title of the note")
    create_parser.add_argument("content", help="Content of the note")
    create_parser.add_argument("--tags", help="Comma-separated list of tags")
    
    # List command
    list_parser = subparsers.add_parser("list", help="List notes")
    list_parser.add_argument("--tag", help="Filter notes by tag")
    
    # View command
    view_parser = subparsers.add_parser("view", help="View a note")
    view_parser.add_argument("id", help="ID of the note to view")
    
    # Update command
    update_parser = subparsers.add_parser("update", help="Update a note")
    update_parser.add_argument("id", help="ID of the note to update")
    update_parser.add_argument("--title", help="New title for the note")
    update_parser.add_argument("--content", help="New content for the note")
    update_parser.add_argument("--tags", help="Comma-separated list of tags")
    
    # Delete command
    delete_parser = subparsers.add_parser("delete", help="Delete a note")
    delete_parser.add_argument("id", help="ID of the note to delete")
    
    # Search command
    search_parser = subparsers.add_parser("search", help="Search notes")
    search_parser.add_argument("query", help="Search query")
    
    return parser


def parse_tags(tags_str: Optional[str]) -> Optional[List[str]]:
    """Parse a comma-separated string of tags into a list."""
    if not tags_str:
        return None
    
    return [tag.strip() for tag in tags_str.split(",") if tag.strip()]


def format_note_list(notes: List[dict]) -> str:
    """Format a list of notes for display."""
    if not notes:
        return "No notes found."
    
    result = []
    for note in notes:
        tags_str = ", ".join(note["tags"]) if note["tags"] else "No tags"
        result.append(f"ID: {note['id']}")
        result.append(f"Title: {note['title']}")
        result.append(f"Tags: {tags_str}")
        result.append(f"Updated: {note['updated_at']}")
        result.append("")
    
    return "\n".join(result)


def format_note(note) -> str:
    """Format a single note for display."""
    tags_str = ", ".join(note.tags) if note.tags else "No tags"
    
    result = [
        f"ID: {note.id}",
        f"Title: {note.title}",
        f"Tags: {tags_str}",
        f"Created: {note.created_at}",
        f"Updated: {note.updated_at}",
        "",
        note.content
    ]
    
    return "\n".join(result)


def process_command(args) -> int:
    """Process the command with the given arguments."""
    if not args.command:
        create_parser().print_help()
        return 1
    
    # Initialize the note manager
    home_dir = os.path.expanduser("~")
    storage_dir = os.path.join(home_dir, "Agentic", "shared", "notes")
    note_manager = NoteManager(storage_dir)
    
    # Execute the requested command
    if args.command == "create":
        tags = parse_tags(args.tags)
        note = note_manager.create_note(args.title, args.content, tags)
        print(f"Note created with ID: {note.id}")
        return 0
    
    elif args.command == "list":
        notes = note_manager.list_notes(args.tag)
        print(format_note_list(notes))
        return 0
    
    elif args.command == "view":
        note = note_manager.get_note(args.id)
        if note:
            print(format_note(note))
            return 0
        else:
            print(f"Note with ID {args.id} not found.")
            return 1
    
    elif args.command == "update":
        tags = parse_tags(args.tags) if args.tags is not None else None
        note = note_manager.update_note(args.id, args.title, args.content, tags)
        if note:
            print(f"Note {args.id} updated successfully.")
            return 0
        else:
            print(f"Note with ID {args.id} not found.")
            return 1
    
    elif args.command == "delete":
        success = note_manager.delete_note(args.id)
        if success:
            print(f"Note {args.id} deleted successfully.")
            return 0
        else:
            print(f"Note with ID {args.id} not found.")
            return 1
    
    elif args.command == "search":
        notes = note_manager.search_notes(args.query)
        if notes:
            print(f"Found {len(notes)} notes matching '{args.query}':")
            print(format_note_list(notes))
            return 0
        else:
            print(f"No notes found matching '{args.query}'.")
            return 0
    
    return 1


def main() -> int:
    """Main entry point for the CLI."""
    parser = create_parser()
    args = parser.parse_args()
    return process_command(args)


def note_command() -> int:
    """
    Entry point for the 'ag note' command.
    
    This function follows the command interface for agentic-core plugins:
    1. Takes no arguments (it parses sys.argv directly)
    2. Returns an integer exit code (0 for success, non-zero for failure)
    3. Handles its own argument parsing
    """
    parser = create_parser()
    args = parser.parse_args(sys.argv[1:])
    return process_command(args)


if __name__ == "__main__":
    sys.exit(main())
