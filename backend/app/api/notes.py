from fastapi import APIRouter, HTTPException, status
from typing import List
from app.models.schemas import (
    Note, NoteCreate, NoteUpdate, SearchQuery, SearchResult
)
from app.services.note_service import note_service

router = APIRouter(prefix="/notes", tags=["notes"])


@router.post("/", response_model=Note, status_code=status.HTTP_201_CREATED)
async def create_note(note: NoteCreate):
    """Create a new note with auto-generated summary and tags"""
    return await note_service.create_note(note)


@router.get("/", response_model=List[Note])
async def list_notes():
    """Get all notes"""
    return await note_service.list_notes()


@router.get("/{note_id}", response_model=Note)
async def get_note(note_id: str):
    """Get a specific note by ID"""
    note = await note_service.get_note(note_id)
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found"
        )
    return note


@router.put("/{note_id}", response_model=Note)
async def update_note(note_id: str, note_update: NoteUpdate):
    """Update a note"""
    note = await note_service.update_note(note_id, note_update)
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found"
        )
    return note


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(note_id: str):
    """Delete a note"""
    success = await note_service.delete_note(note_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found"
        )


@router.post("/search", response_model=List[SearchResult])
async def search_notes(search_query: SearchQuery):
    """Search notes using natural language"""
    return await note_service.search_notes(
        search_query.query,
        search_query.limit
    )
