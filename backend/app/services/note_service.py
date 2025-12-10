from typing import List, Optional
from datetime import datetime
import uuid
from app.models.schemas import Note, NoteCreate, NoteUpdate, SearchResult
from app.db.chroma_connection import chroma_conn
from app.services.ai_service import embedding_service, gpt_service


class NoteService:
    """Service for managing notes"""
    
    def __init__(self):
        self.notes_db = {}  # In-memory storage for demo
    
    async def create_note(self, note_create: NoteCreate) -> Note:
        """Create a new note with embeddings and auto-tags"""
        note_id = str(uuid.uuid4())
        now = datetime.utcnow()
        
        # Generate summary and auto-tags
        summary = await gpt_service.summarize(note_create.content)
        auto_tags = await gpt_service.extract_tags(note_create.content)
        
        # Create note object
        note = Note(
            id=note_id,
            title=note_create.title,
            content=note_create.content,
            tags=note_create.tags or [],
            created_at=now,
            updated_at=now,
            summary=summary,
            auto_tags=auto_tags
        )
        
        # Store in memory
        self.notes_db[note_id] = note
        
        # Generate embedding and store in ChromaDB
        embedding = embedding_service.generate_embedding(
            f"{note.title} {note.content}"
        )
        
        collection = chroma_conn.get_collection()
        collection.add(
            embeddings=[embedding],
            documents=[note.content],
            metadatas=[{
                "id": note_id,
                "title": note.title,
                "tags": ",".join(note.tags + auto_tags)
            }],
            ids=[note_id]
        )
        
        return note
    
    async def get_note(self, note_id: str) -> Optional[Note]:
        """Get a note by ID"""
        return self.notes_db.get(note_id)
    
    async def list_notes(self) -> List[Note]:
        """List all notes"""
        return list(self.notes_db.values())
    
    async def update_note(self, note_id: str, note_update: NoteUpdate) -> Optional[Note]:
        """Update a note"""
        note = self.notes_db.get(note_id)
        if not note:
            return None
        
        # Update fields
        if note_update.title is not None:
            note.title = note_update.title
        if note_update.content is not None:
            note.content = note_update.content
            # Regenerate summary and tags for content changes
            note.summary = await gpt_service.summarize(note_update.content)
            note.auto_tags = await gpt_service.extract_tags(note_update.content)
        if note_update.tags is not None:
            note.tags = note_update.tags
        
        note.updated_at = datetime.utcnow()
        
        # Update embedding in ChromaDB
        embedding = embedding_service.generate_embedding(
            f"{note.title} {note.content}"
        )
        
        collection = chroma_conn.get_collection()
        collection.update(
            embeddings=[embedding],
            documents=[note.content],
            metadatas=[{
                "id": note_id,
                "title": note.title,
                "tags": ",".join(note.tags + note.auto_tags)
            }],
            ids=[note_id]
        )
        
        return note
    
    async def delete_note(self, note_id: str) -> bool:
        """Delete a note"""
        if note_id not in self.notes_db:
            return False
        
        del self.notes_db[note_id]
        
        # Remove from ChromaDB
        collection = chroma_conn.get_collection()
        collection.delete(ids=[note_id])
        
        return True
    
    async def search_notes(self, query: str, limit: int = 10) -> List[SearchResult]:
        """Search notes using semantic similarity"""
        # Generate query embedding
        query_embedding = embedding_service.generate_embedding(query)
        
        # Search in ChromaDB
        collection = chroma_conn.get_collection()
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=min(limit, len(self.notes_db))
        )
        
        # Format results
        search_results = []
        if results['ids'] and results['ids'][0]:
            for i, note_id in enumerate(results['ids'][0]):
                note = self.notes_db.get(note_id)
                if note:
                    similarity_score = 1 - results['distances'][0][i]  # Convert distance to similarity
                    search_results.append(
                        SearchResult(note=note, similarity_score=similarity_score)
                    )
        
        return search_results


note_service = NoteService()
