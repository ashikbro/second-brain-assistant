from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class NoteBase(BaseModel):
    """Base note model"""
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)
    tags: Optional[List[str]] = []


class NoteCreate(NoteBase):
    """Model for creating a note"""
    pass


class NoteUpdate(BaseModel):
    """Model for updating a note"""
    title: Optional[str] = None
    content: Optional[str] = None
    tags: Optional[List[str]] = None


class Note(NoteBase):
    """Full note model with metadata"""
    id: str
    created_at: datetime
    updated_at: datetime
    summary: Optional[str] = None
    auto_tags: Optional[List[str]] = []
    
    class Config:
        from_attributes = True


class SearchQuery(BaseModel):
    """Model for search queries"""
    query: str = Field(..., min_length=1)
    limit: Optional[int] = Field(10, ge=1, le=100)


class SearchResult(BaseModel):
    """Model for search results"""
    note: Note
    similarity_score: float


class GraphNode(BaseModel):
    """Model for graph nodes"""
    id: str
    title: str
    tags: List[str]


class GraphRelationship(BaseModel):
    """Model for graph relationships"""
    source: str
    target: str
    relationship_type: str
    weight: float


class KnowledgeGraph(BaseModel):
    """Model for complete knowledge graph"""
    nodes: List[GraphNode]
    relationships: List[GraphRelationship]


class SummarizeRequest(BaseModel):
    """Model for summarization request"""
    content: str = Field(..., min_length=1)


class IdeaGenerationRequest(BaseModel):
    """Model for idea generation request"""
    topic: str = Field(..., min_length=1)
    context: Optional[str] = None
