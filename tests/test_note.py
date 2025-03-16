"""
Tests for the Note class.
"""

import os
import pathlib
import tempfile
import uuid
from unittest import TestCase

from agentic_note.note import Note, NoteManager


class TestNote(TestCase):
    """Test the Note class."""
    
    def test_note_creation(self):
        """Test creating a new note."""
        note = Note(title="Test Note", content="This is a test note.")
        
        self.assertEqual(note.title, "Test Note")
        self.assertEqual(note.content, "This is a test note.")
        self.assertEqual(note.tags, [])
        self.assertIsNotNone(note.created_at)
        self.assertIsNotNone(note.updated_at)
        self.assertIsNotNone(note.id)
    
    def test_note_update(self):
        """Test updating a note."""
        note = Note(title="Test Note", content="This is a test note.")
        original_created_at = note.created_at
        original_updated_at = note.updated_at
        
        # Update the note
        note.update(title="Updated Title", content="Updated content", tags=["tag1", "tag2"])
        
        self.assertEqual(note.title, "Updated Title")
        self.assertEqual(note.content, "Updated content")
        self.assertEqual(note.tags, ["tag1", "tag2"])
        self.assertEqual(note.created_at, original_created_at)
        self.assertNotEqual(note.updated_at, original_updated_at)
    
    def test_note_to_dict(self):
        """Test converting a note to a dictionary."""
        note = Note(title="Test Note", content="This is a test note.", tags=["tag1"])
        note_dict = note.to_dict()
        
        self.assertEqual(note_dict["title"], "Test Note")
        self.assertEqual(note_dict["content"], "This is a test note.")
        self.assertEqual(note_dict["tags"], ["tag1"])
        self.assertIsNotNone(note_dict["created_at"])
        self.assertIsNotNone(note_dict["updated_at"])
        self.assertIsNotNone(note_dict["id"])
    
    def test_note_from_dict(self):
        """Test creating a note from a dictionary."""
        note_dict = {
            "title": "Test Note",
            "content": "This is a test note.",
            "tags": ["tag1", "tag2"],
            "created_at": "2025-03-15T12:00:00",
            "updated_at": "2025-03-15T12:00:00",
            "id": str(uuid.uuid4())
        }
        
        note = Note.from_dict(note_dict)
        
        self.assertEqual(note.title, "Test Note")
        self.assertEqual(note.content, "This is a test note.")
        self.assertEqual(note.tags, ["tag1", "tag2"])
        self.assertEqual(note.created_at, "2025-03-15T12:00:00")
        self.assertEqual(note.updated_at, "2025-03-15T12:00:00")
        self.assertEqual(note.id, note_dict["id"])


class TestNoteManager(TestCase):
    """Test the NoteManager class."""
    
    def setUp(self):
        """Set up a temporary directory for testing."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.storage_dir = pathlib.Path(self.temp_dir.name)
        self.note_manager = NoteManager(self.storage_dir)
    
    def tearDown(self):
        """Clean up the temporary directory."""
        self.temp_dir.cleanup()
    
    def test_create_note(self):
        """Test creating a note."""
        note = self.note_manager.create_note(
            title="Test Note",
            content="This is a test note.",
            tags=["tag1", "tag2"]
        )
        
        self.assertEqual(note.title, "Test Note")
        self.assertEqual(note.content, "This is a test note.")
        self.assertEqual(note.tags, ["tag1", "tag2"])
        
        # Check that the note was saved to disk
        note_path = self.storage_dir / f"{note.id}.json"
        self.assertTrue(note_path.exists())
        
        # Check that the index was updated
        self.assertIn(note.id, self.note_manager.index)
        self.assertEqual(self.note_manager.index[note.id]["title"], "Test Note")
        self.assertEqual(self.note_manager.index[note.id]["tags"], ["tag1", "tag2"])
    
    def test_get_note(self):
        """Test getting a note."""
        # Create a note
        note = self.note_manager.create_note(
            title="Test Note",
            content="This is a test note."
        )
        
        # Get the note
        retrieved_note = self.note_manager.get_note(note.id)
        
        self.assertEqual(retrieved_note.title, "Test Note")
        self.assertEqual(retrieved_note.content, "This is a test note.")
        
        # Try to get a non-existent note
        non_existent_note = self.note_manager.get_note("non-existent-id")
        self.assertIsNone(non_existent_note)
    
    def test_update_note(self):
        """Test updating a note."""
        # Create a note
        note = self.note_manager.create_note(
            title="Test Note",
            content="This is a test note."
        )
        
        # Update the note
        updated_note = self.note_manager.update_note(
            note_id=note.id,
            title="Updated Title",
            content="Updated content",
            tags=["tag1", "tag2"]
        )
        
        self.assertEqual(updated_note.title, "Updated Title")
        self.assertEqual(updated_note.content, "Updated content")
        self.assertEqual(updated_note.tags, ["tag1", "tag2"])
        
        # Check that the index was updated
        self.assertEqual(self.note_manager.index[note.id]["title"], "Updated Title")
        self.assertEqual(self.note_manager.index[note.id]["tags"], ["tag1", "tag2"])
        
        # Try to update a non-existent note
        non_existent_note = self.note_manager.update_note(
            note_id="non-existent-id",
            title="Updated Title"
        )
        self.assertIsNone(non_existent_note)
    
    def test_delete_note(self):
        """Test deleting a note."""
        # Create a note
        note = self.note_manager.create_note(
            title="Test Note",
            content="This is a test note."
        )
        
        # Delete the note
        success = self.note_manager.delete_note(note.id)
        
        self.assertTrue(success)
        
        # Check that the note was deleted from disk
        note_path = self.storage_dir / f"{note.id}.json"
        self.assertFalse(note_path.exists())
        
        # Check that the index was updated
        self.assertNotIn(note.id, self.note_manager.index)
        
        # Try to delete a non-existent note
        success = self.note_manager.delete_note("non-existent-id")
        self.assertFalse(success)
    
    def test_list_notes(self):
        """Test listing notes."""
        # Create some notes
        note1 = self.note_manager.create_note(
            title="Note 1",
            content="Content 1",
            tags=["tag1", "tag2"]
        )
        
        note2 = self.note_manager.create_note(
            title="Note 2",
            content="Content 2",
            tags=["tag2", "tag3"]
        )
        
        # List all notes
        notes = self.note_manager.list_notes()
        
        self.assertEqual(len(notes), 2)
        
        # List notes with a specific tag
        notes = self.note_manager.list_notes(tag="tag1")
        
        self.assertEqual(len(notes), 1)
        self.assertEqual(notes[0]["id"], note1.id)
    
    def test_search_notes(self):
        """Test searching notes."""
        # Create some notes
        note1 = self.note_manager.create_note(
            title="Apple Pie Recipe",
            content="Ingredients: apples, sugar, flour"
        )
        
        note2 = self.note_manager.create_note(
            title="Banana Bread",
            content="Ingredients: bananas, sugar, flour"
        )
        
        # Search by title
        results = self.note_manager.search_notes("apple")
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["id"], note1.id)
        self.assertEqual(results[0]["matched"], "title")
        
        # Search by content
        results = self.note_manager.search_notes("banana")
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["id"], note2.id)
        self.assertEqual(results[0]["matched"], "title")
        
        # Search by content
        results = self.note_manager.search_notes("sugar")
        
        self.assertEqual(len(results), 2)
