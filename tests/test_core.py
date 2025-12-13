"""Tests for core functionality."""

import pytest
from second_brain.core import Note, KnowledgeGraph


def test_note_creation():
    """Test creating a new note."""
    note = Note(title="Test Note", content="This is a test", tags=["test"])
    assert note.title == "Test Note"
    assert note.content == "This is a test"
    assert "test" in note.tags


def test_note_add_tag():
    """Test adding tags to a note."""
    note = Note(title="Test", content="Content")
    note.add_tag("important")
    assert "important" in note.tags


def test_knowledge_graph_add_note():
    """Test adding a note to the knowledge graph."""
    kg = KnowledgeGraph()
    note = Note(title="Test", content="Content")
    note_id = kg.add_note(note)
    
    assert note_id is not None
    assert len(kg) == 1
    assert kg.get_note(note_id) == note


def test_knowledge_graph_link_notes():
    """Test linking two notes together."""
    kg = KnowledgeGraph()
    note1 = Note(title="Note 1", content="Content 1")
    note2 = Note(title="Note 2", content="Content 2")
    
    id1 = kg.add_note(note1)
    id2 = kg.add_note(note2)
    
    kg.link_notes(id1, id2)
    
    connected = kg.get_connected_notes(id1)
    assert len(connected) == 1
    assert connected[0] == note2


def test_knowledge_graph_get_notes_by_tag():
    """Test finding notes by tag."""
    kg = KnowledgeGraph()
    note1 = Note(title="Note 1", content="Content 1", tags=["python"])
    note2 = Note(title="Note 2", content="Content 2", tags=["python", "ai"])
    note3 = Note(title="Note 3", content="Content 3", tags=["javascript"])
    
    kg.add_note(note1)
    kg.add_note(note2)
    kg.add_note(note3)
    
    python_notes = kg.get_notes_by_tag("python")
    assert len(python_notes) == 2
    assert note1 in python_notes
    assert note2 in python_notes
