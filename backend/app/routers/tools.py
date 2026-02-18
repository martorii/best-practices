from app.schemas import ToolInfo
from app.state import state
from fastapi import APIRouter

router = APIRouter()


@router.get("/tools", response_model=list[ToolInfo])
async def list_tools():
    """Return the tools currently available to the agent."""
    return [ToolInfo(name=t.name, description=t.description or "") for t in state.tools]
