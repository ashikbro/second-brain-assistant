"""
Basic usage example for Second Brain Assistant.
"""

from second_brain import KnowledgeGraph, Note, SemanticSearch


def main():
    """Demonstrate basic usage of the Second Brain Assistant."""
    
    # Initialize knowledge graph
    print("Initializing Knowledge Graph...")
    kg = KnowledgeGraph()
    
    # Create some notes
    print("\nCreating notes...")
    note1 = Note(
        title="Python Programming",
        content="Python is a versatile programming language widely used in data science and AI.",
        tags=["python", "programming", "ai"]
    )
    
    note2 = Note(
        title="Machine Learning",
        content="Machine learning is a subset of AI that enables systems to learn from data.",
        tags=["ai", "ml", "data-science"]
    )
    
    note3 = Note(
        title="Deep Learning",
        content="Deep learning uses neural networks with multiple layers for complex pattern recognition.",
        tags=["ai", "ml", "deep-learning"]
    )
    
    # Add notes to knowledge graph
    id1 = kg.add_note(note1)
    id2 = kg.add_note(note2)
    id3 = kg.add_note(note3)
    
    print(f"Added {len(kg)} notes to the knowledge graph")
    
    # Link related notes
    print("\nLinking related notes...")
    kg.link_notes(id1, id2)  # Python → ML
    kg.link_notes(id2, id3)  # ML → Deep Learning
    
    # Search for notes
    print("\nSearching for 'machine learning'...")
    search = SemanticSearch(kg)
    results = search.search("machine learning", top_k=3)
    
    print(f"\nFound {len(results)} results:")
    for note, score in results:
        print(f"  - {note.title} (score: {score:.2f})")
    
    # Find notes by tag
    print("\nFinding notes with 'ai' tag...")
    ai_notes = kg.get_notes_by_tag("ai")
    print(f"Found {len(ai_notes)} notes with 'ai' tag:")
    for note in ai_notes:
        print(f"  - {note.title}")
    
    # Get connected notes
    print(f"\nNotes connected to '{note1.title}':")
    connected = kg.get_connected_notes(id1)
    for note in connected:
        print(f"  - {note.title}")


if __name__ == "__main__":
    main()
