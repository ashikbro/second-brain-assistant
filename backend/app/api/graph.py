from fastapi import APIRouter
from app.models.schemas import KnowledgeGraph
from app.services.graph_service import graph_service

router = APIRouter(prefix="/graph", tags=["graph"])


@router.post("/build")
async def build_graph():
    """Build/rebuild the knowledge graph from all notes"""
    await graph_service.build_graph()
    return {"message": "Knowledge graph built successfully"}


@router.get("/", response_model=KnowledgeGraph)
async def get_graph():
    """Get the complete knowledge graph"""
    return await graph_service.get_graph()


@router.get("/related/{note_id}")
async def get_related_notes(note_id: str, limit: int = 5):
    """Get notes related to a specific note"""
    related_ids = await graph_service.get_related_notes(note_id, limit)
    return {"note_id": note_id, "related_notes": related_ids}
