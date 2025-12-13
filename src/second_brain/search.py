"""
Semantic search functionality for finding related notes.
"""

from typing import List, Tuple
from .core import Note, KnowledgeGraph


class SemanticSearch:
    """Provides semantic search capabilities over the knowledge base."""
    
    def __init__(self, knowledge_graph: KnowledgeGraph):
        self.knowledge_graph = knowledge_graph
    
    def search(self, query: str, top_k: int = 5) -> List[Tuple[Note, float]]:
        """
        Search for notes semantically similar to the query.
        
        Args:
            query: The search query
            top_k: Number of top results to return
            
        Returns:
            List of (Note, similarity_score) tuples
        """
        import heapq
        
        results = []
        
        for note in self.knowledge_graph.notes.values():
            score = self._calculate_similarity(query, note)
            if score > 0:
                results.append((note, score))
        
        # Use heapq for efficient top-k selection
        return heapq.nlargest(top_k, results, key=lambda x: x[1])
    
    def _calculate_similarity(self, query: str, note: Note) -> float:
        """
        Calculate similarity between query and note.
        This is a placeholder for actual semantic similarity.
        """
        query_lower = query.lower()
        title_match = query_lower in note.title.lower()
        content_match = query_lower in note.content.lower()
        tag_match = any(query_lower in tag.lower() for tag in note.tags)
        
        score = 0.0
        if title_match:
            score += 0.5
        if content_match:
            score += 0.3
        if tag_match:
            score += 0.2
        
        return score
