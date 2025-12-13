"""
Second Brain Assistant - An AI-powered personal knowledge management system.
"""

__version__ = "0.1.0"
__author__ = "Second Brain Assistant Contributors"
__license__ = "MIT"

from .core import KnowledgeGraph, Note
from .search import SemanticSearch

__all__ = ["KnowledgeGraph", "Note", "SemanticSearch", "__version__"]
