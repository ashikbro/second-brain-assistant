"""
Core functionality for the Second Brain Assistant.
"""

from datetime import datetime
from typing import List, Dict, Optional, Set
import networkx as nx


class Note:
    """Represents a single note in the knowledge base."""
    
    def __init__(self, title: str, content: str, tags: Optional[List[str]] = None):
        self.id = None
        self.title = title
        self.content = content
        self.tags = tags or []
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.links: Set[str] = set()
    
    def add_tag(self, tag: str) -> None:
        """Add a tag to the note."""
        if tag not in self.tags:
            self.tags.append(tag)
            self.updated_at = datetime.now()
    
    def link_to(self, note_id: str) -> None:
        """Create a link to another note."""
        self.links.add(note_id)
        self.updated_at = datetime.now()
    
    def __repr__(self) -> str:
        return f"Note(id={self.id}, title={self.title}, tags={self.tags})"


class KnowledgeGraph:
    """Manages the knowledge graph of interconnected notes."""
    
    def __init__(self):
        self.graph = nx.DiGraph()
        self.notes: Dict[str, Note] = {}
        self._next_id = 0
    
    def add_note(self, note: Note) -> str:
        """Add a note to the knowledge graph."""
        note.id = str(self._next_id)
        self._next_id += 1
        
        self.notes[note.id] = note
        self.graph.add_node(note.id, note=note)
        
        return note.id
    
    def link_notes(self, from_id: str, to_id: str) -> None:
        """Create a directed link between two notes."""
        if from_id not in self.notes or to_id not in self.notes:
            raise ValueError("Both notes must exist in the knowledge graph")
        
        self.notes[from_id].link_to(to_id)
        self.graph.add_edge(from_id, to_id)
    
    def get_note(self, note_id: str) -> Optional[Note]:
        """Retrieve a note by its ID."""
        return self.notes.get(note_id)
    
    def get_connected_notes(self, note_id: str) -> List[Note]:
        """Get all notes connected to the given note."""
        if note_id not in self.graph:
            return []
        
        connected_ids = list(self.graph.successors(note_id)) + list(self.graph.predecessors(note_id))
        return [self.notes[nid] for nid in connected_ids if nid in self.notes]
    
    def get_notes_by_tag(self, tag: str) -> List[Note]:
        """Find all notes with a specific tag."""
        return [note for note in self.notes.values() if tag in note.tags]
    
    def __len__(self) -> int:
        return len(self.notes)
