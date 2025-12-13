"""
Command-line interface for Second Brain Assistant.
"""

import sys
from .core import KnowledgeGraph, Note


def main():
    """Main entry point for the CLI."""
    print("Second Brain Assistant v0.1.0")
    print("AI-powered personal knowledge management system")
    print("\nThis is a placeholder CLI. Full implementation coming soon!")
    
    kg = KnowledgeGraph()
    print(f"\nKnowledge graph initialized with {len(kg)} notes.")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
