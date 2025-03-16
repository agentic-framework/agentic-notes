"""
Tests for the CLI module.
"""

import argparse
import io
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from agentic_note.cli import create_parser, main, parse_tags
from agentic_note.note import Note, NoteManager


class TestCLI(unittest.TestCase):
    """Test the CLI module."""
    
    def test_create_parser(self):
        """Test creating the argument parser."""
        parser = create_parser()
        self.assertIsInstance(parser, argparse.ArgumentParser)
    
    def test_parse_tags(self):
        """Test parsing tags."""
        # Test with a valid tags string
        tags = parse_tags("tag1,tag2,tag3")
        self.assertEqual(tags, ["tag1", "tag2", "tag3"])
        
        # Test with a tags string containing spaces
        tags = parse_tags("tag1, tag2, tag3")
        self.assertEqual(tags, ["tag1", "tag2", "tag3"])
        
        # Test with an empty tags string
        tags = parse_tags("")
        self.assertIsNone(tags)
        
        # Test with None
        tags = parse_tags(None)
        self.assertIsNone(tags)


class TestCLICommands(unittest.TestCase):
    """Test the CLI commands."""
    
    def setUp(self):
        """Set up a temporary directory for testing."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.storage_dir = Path(self.temp_dir.name)
        
        # Create a test note
        self.note_manager = NoteManager(self.storage_dir)
        self.test_note = self.note_manager.create_note(
            title="Test Note",
            content="This is a test note.",
            tags=["tag1", "tag2"]
        )
    
    def tearDown(self):
        """Clean up the temporary directory."""
        self.temp_dir.cleanup()
    
    @patch("sys.stdout", new_callable=io.StringIO)
    @patch("agentic_note.cli.NoteManager")
    def test_create_command(self, mock_note_manager_class, mock_stdout):
        """Test the create command."""
        # Mock the NoteManager instance
        mock_note_manager = mock_note_manager_class.return_value
        mock_note = Note(title="Test Note", content="This is a test note.")
        mock_note_manager.create_note.return_value = mock_note
        
        # Call main with create command arguments
        with patch("sys.argv", ["ag-note", "create", "Test Note", "This is a test note.", "--tags", "tag1,tag2"]):
            main()
        
        # Check that create_note was called with the correct arguments
        mock_note_manager.create_note.assert_called_once_with(
            "Test Note",
            "This is a test note.",
            ["tag1", "tag2"]
        )
        
        # Check that the output contains the note ID
        self.assertIn(f"Note created with ID: {mock_note.id}", mock_stdout.getvalue())
    
    @patch("sys.stdout", new_callable=io.StringIO)
    @patch("agentic_note.cli.NoteManager")
    def test_list_command(self, mock_note_manager_class, mock_stdout):
        """Test the list command."""
        # Mock the NoteManager instance
        mock_note_manager = mock_note_manager_class.return_value
        mock_note_manager.list_notes.return_value = [
            {
                "id": "note-id-1",
                "title": "Note 1",
                "tags": ["tag1", "tag2"],
                "created_at": "2025-03-15T12:00:00",
                "updated_at": "2025-03-15T12:00:00"
            },
            {
                "id": "note-id-2",
                "title": "Note 2",
                "tags": ["tag2", "tag3"],
                "created_at": "2025-03-15T12:00:00",
                "updated_at": "2025-03-15T12:00:00"
            }
        ]
        
        # Call main with list command arguments
        with patch("sys.argv", ["ag-note", "list"]):
            main()
        
        # Check that list_notes was called with the correct arguments
        mock_note_manager.list_notes.assert_called_once_with(None)
        
        # Check that the output contains the note information
        output = mock_stdout.getvalue()
        self.assertIn("ID: note-id-1", output)
        self.assertIn("Title: Note 1", output)
        self.assertIn("Tags: tag1, tag2", output)
        self.assertIn("ID: note-id-2", output)
        self.assertIn("Title: Note 2", output)
        self.assertIn("Tags: tag2, tag3", output)
    
    @patch("sys.stdout", new_callable=io.StringIO)
    @patch("agentic_note.cli.NoteManager")
    def test_view_command(self, mock_note_manager_class, mock_stdout):
        """Test the view command."""
        # Mock the NoteManager instance
        mock_note_manager = mock_note_manager_class.return_value
        mock_note = Note(
            title="Test Note",
            content="This is a test note.",
            tags=["tag1", "tag2"],
            id="note-id"
        )
        mock_note_manager.get_note.return_value = mock_note
        
        # Call main with view command arguments
        with patch("sys.argv", ["ag-note", "view", "note-id"]):
            main()
        
        # Check that get_note was called with the correct arguments
        mock_note_manager.get_note.assert_called_once_with("note-id")
        
        # Check that the output contains the note information
        output = mock_stdout.getvalue()
        self.assertIn("ID: note-id", output)
        self.assertIn("Title: Test Note", output)
        self.assertIn("Tags: tag1, tag2", output)
        self.assertIn("This is a test note.", output)
