"""
Core module for note-taking functionality.
"""

import datetime
import json
import os
import pathlib
import uuid
from dataclasses import asdict, dataclass
from typing import Dict, List, Optional, Union


@dataclass
class Note:
    """Represents a single note."""
    
    title: str
    content: str
    tags: Optional[List[str]] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    id: Optional[str] = None
    
    def __post_init__(self):
        """Initialize default values for a new note."""
        now = datetime.datetime.now().isoformat()
        
        if self.tags is None:
            self.tags = []
            
        if self.created_at is None:
            self.created_at = now
            
        if self.updated_at is None:
            self.updated_at = now
            
        if self.id is None:
            self.id = str(uuid.uuid4())
    
    def update(self, title: Optional[str] = None, content: Optional[str] = None, 
               tags: Optional[List[str]] = None) -> None:
        """Update the note with new values."""
        if title is not None:
            self.title = title
            
        if content is not None:
            self.content = content
            
        if tags is not None:
            self.tags = tags
            
        self.updated_at = datetime.datetime.now().isoformat()
    
    def to_dict(self) -> Dict:
        """Convert the note to a dictionary."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Note':
        """Create a Note instance from a dictionary."""
        return cls(**data)


class NoteManager:
    """Manages notes storage and operations."""
    
    def __init__(self, storage_dir: Optional[Union[str, pathlib.Path]] = None):
        """Initialize the NoteManager with a storage directory."""
        if storage_dir is None:
            home_dir = os.path.expanduser("~")
            storage_dir = os.path.join(home_dir, "Agentic", "shared", "notes")
            
        self.storage_dir = pathlib.Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.index_file = self.storage_dir / "index.json"
        self._load_index()
    
    def _load_index(self) -> None:
        """Load the note index from disk."""
        if self.index_file.exists():
            with open(self.index_file, "r", encoding="utf-8") as f:
                self.index = json.load(f)
        else:
            self.index = {}
            self._save_index()
    
    def _save_index(self) -> None:
        """Save the note index to disk."""
        with open(self.index_file, "w", encoding="utf-8") as f:
            json.dump(self.index, f, indent=2)
    
    def _get_note_path(self, note_id: str) -> pathlib.Path:
        """Get the file path for a note."""
        return self.storage_dir / f"{note_id}.json"
    
    def create_note(self, title: str, content: str, tags: Optional[List[str]] = None) -> Note:
        """Create a new note."""
        note = Note(title=title, content=content, tags=tags)
        
        # Save the note to disk
        if note.id is not None:  # This should always be true due to __post_init__
            note_path = self._get_note_path(note.id)
            with open(note_path, "w", encoding="utf-8") as f:
                json.dump(note.to_dict(), f, indent=2)
        
        # Update the index
        self.index[note.id] = {
            "title": note.title,
            "tags": note.tags,
            "created_at": note.created_at,
            "updated_at": note.updated_at
        }
        self._save_index()
        
        return note
    
    def get_note(self, note_id: str) -> Optional[Note]:
        """Get a note by ID."""
        if note_id not in self.index:
            return None
        
        note_path = self._get_note_path(note_id)
        if not note_path.exists():
            return None
        
        with open(note_path, "r", encoding="utf-8") as f:
            note_data = json.load(f)
            
        return Note.from_dict(note_data)
    
    def update_note(self, note_id: str, title: Optional[str] = None, 
                   content: Optional[str] = None, tags: Optional[List[str]] = None) -> Optional[Note]:
        """Update an existing note."""
        note = self.get_note(note_id)
        if note is None:
            return None
        
        note.update(title=title, content=content, tags=tags)
        
        # Save the updated note to disk
        if note.id is not None:  # This should always be true for an existing note
            note_path = self._get_note_path(note.id)
            with open(note_path, "w", encoding="utf-8") as f:
                json.dump(note.to_dict(), f, indent=2)
        
        # Update the index
        self.index[note.id]["title"] = note.title
        self.index[note.id]["tags"] = note.tags
        self.index[note.id]["updated_at"] = note.updated_at
        self._save_index()
        
        return note
    
    def delete_note(self, note_id: str) -> bool:
        """Delete a note by ID."""
        if note_id not in self.index:
            return False
        
        note_path = self._get_note_path(note_id)
        if note_path.exists():
            note_path.unlink()
        
        del self.index[note_id]
        self._save_index()
        
        return True
    
    def list_notes(self, tag: Optional[str] = None) -> List[Dict]:
        """List all notes, optionally filtered by tag."""
        notes = []
        
        for note_id, note_info in self.index.items():
            if tag is None or tag in note_info["tags"]:
                notes.append({
                    "id": note_id,
                    **note_info
                })
        
        # Sort by updated_at (newest first)
        notes.sort(key=lambda x: x["updated_at"], reverse=True)
        
        return notes
    
    def search_notes(self, query: str) -> List[Dict]:
        """Search notes by title and content."""
        query = query.lower()
        results = []
        
        for note_id, note_info in self.index.items():
            # Check if query matches title
            if query in note_info["title"].lower():
                results.append({
                    "id": note_id,
                    **note_info,
                    "matched": "title"
                })
                continue
            
            # Check if query matches content
            note = self.get_note(note_id)
            if note and query in note.content.lower():
                results.append({
                    "id": note_id,
                    **note_info,
                    "matched": "content"
                })
        
        # Sort by updated_at (newest first)
        results.sort(key=lambda x: x["updated_at"], reverse=True)
        
        return results
