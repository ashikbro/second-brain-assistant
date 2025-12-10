"""
Example script demonstrating how to use the Second Brain Assistant API
"""
import requests
import json

API_URL = "http://localhost:8000"

def create_note(title, content, tags):
    """Create a new note"""
    response = requests.post(
        f"{API_URL}/notes/",
        json={
            "title": title,
            "content": content,
            "tags": tags
        }
    )
    return response.json()

def search_notes(query, limit=10):
    """Search notes using natural language"""
    response = requests.post(
        f"{API_URL}/notes/search",
        json={
            "query": query,
            "limit": limit
        }
    )
    return response.json()

def get_knowledge_graph():
    """Get the knowledge graph"""
    # Build graph first
    requests.post(f"{API_URL}/graph/build")
    
    # Get graph data
    response = requests.get(f"{API_URL}/graph/")
    return response.json()

def generate_ideas(topic, context=""):
    """Generate ideas on a topic"""
    response = requests.post(
        f"{API_URL}/ai/generate-ideas",
        json={
            "topic": topic,
            "context": context
        }
    )
    return response.json()

if __name__ == "__main__":
    print("🧠 Second Brain Assistant - API Examples\n")
    
    # Example 1: Create a note
    print("1. Creating a note about Python...")
    note = create_note(
        title="Python Best Practices",
        content="Always use virtual environments, write tests, follow PEP 8 style guide, use type hints, and write clear docstrings.",
        tags=["python", "programming", "best-practices"]
    )
    print(f"   Created note: {note['id']}")
    print(f"   Summary: {note['summary']}")
    print(f"   Auto-tags: {note['auto_tags']}\n")
    
    # Example 2: Search notes
    print("2. Searching for 'coding standards'...")
    results = search_notes("coding standards and good practices")
    for result in results[:3]:
        print(f"   - {result['note']['title']} (score: {result['similarity_score']:.2f})")
    print()
    
    # Example 3: Generate ideas
    print("3. Generating ideas about machine learning...")
    ideas = generate_ideas(
        topic="Machine Learning applications",
        context="Focus on practical real-world applications"
    )
    print(f"   {ideas['ideas']}\n")
    
    # Example 4: Get knowledge graph
    print("4. Getting knowledge graph...")
    graph = get_knowledge_graph()
    print(f"   Nodes: {len(graph['nodes'])}")
    print(f"   Relationships: {len(graph['relationships'])}\n")
    
    print("✅ Examples completed!")
