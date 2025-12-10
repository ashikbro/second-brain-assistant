from fastapi import APIRouter
from app.models.schemas import SummarizeRequest, IdeaGenerationRequest
from app.services.ai_service import gpt_service

router = APIRouter(prefix="/ai", tags=["ai"])


@router.post("/summarize")
async def summarize_content(request: SummarizeRequest):
    """Generate a summary of provided content"""
    summary = await gpt_service.summarize(request.content)
    return {"summary": summary}


@router.post("/generate-ideas")
async def generate_ideas(request: IdeaGenerationRequest):
    """Generate ideas based on a topic"""
    ideas = await gpt_service.generate_ideas(
        request.topic,
        request.context or ""
    )
    return {"ideas": ideas}


@router.post("/extract-tags")
async def extract_tags(request: SummarizeRequest):
    """Extract tags from content"""
    tags = await gpt_service.extract_tags(request.content)
    return {"tags": tags}
