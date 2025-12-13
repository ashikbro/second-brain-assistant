"""Tests for search functionality."""

import pytest
from second_brain.core import Note, KnowledgeGraph
from second_brain.search import SemanticSearch


def test_semantic_search_initialization():
    """Test creating a semantic search instance."""
    kg = KnowledgeGraph()
    search = SemanticSearch(kg)
    assert search.knowledge_graph == kg


def test_semantic_search_basic():
    """Test basic semantic search."""
    kg = KnowledgeGraph()
    note1 = Note(title="Python Programming", content="Learn Python basics", tags=["python"])
    note2 = Note(title="JavaScript Guide", content="JavaScript fundamentals", tags=["javascript"])
    
    kg.add_note(note1)
    kg.add_note(note2)
    
    search = SemanticSearch(kg)
    results = search.search("python", top_k=2)
    
    assert len(results) > 0
    assert results[0][0] == note1


def test_semantic_search_empty_graph():
    """Test search on empty knowledge graph."""
    kg = KnowledgeGraph()
    search = SemanticSearch(kg)
    results = search.search("test", top_k=5)
    
    assert len(results) == 0
