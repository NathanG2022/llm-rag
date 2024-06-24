from fastapi import APIRouter
from pydantic import BaseModel
from story.story_service import get_prompts

router = APIRouter(prefix='/stories', tags=["stories"])


class GeneratePromptsReq(BaseModel):
    story: str


@router.post("/prompts", description="generate prompts from a story")
async def generate_prompts(payload: GeneratePromptsReq):
    return {'prompts': get_prompts(payload.story)}
