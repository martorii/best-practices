from app.state import state
from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health():
    return {
        "status": "ok",
        "tools_loaded": state.tools_loaded,
        "tool_count": len(state.tools),
    }
