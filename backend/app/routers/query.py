import json
from collections.abc import AsyncIterator
from typing import Any

from app.agent import run_agent_stream
from app.schemas import QueryRequest
from app.state import state
from fastapi import APIRouter
from sse_starlette.sse import EventSourceResponse

router = APIRouter()


def serialize_event(event: Any) -> Any:
    if hasattr(event, "model_dump"):  # Pydantic v2
        return json.dumps(event.model_dump())
    elif hasattr(event, "dict"):  # Pydantic v1
        return json.dumps(event.dict())
    elif hasattr(event, "__dict__"):
        return json.dumps(event.__dict__)
    else:
        return str(event)


@router.post("/query")
async def query(request: QueryRequest):
    """
    Run the ReAct agent on the given query.

    Streams Server-Sent Events with the following JSON payloads:

    ```
    data: {"type": "thinking",    "content": "<partial LLM token>"}
    data: {"type": "tool_call",   "content": {"tool": "...", "input": {...}}}
    data: {"type": "tool_result", "content": {"tool": "...", "output": "..."}}
    data: {"type": "answer",      "content": "<final answer>"}
    data: {"type": "error",       "content": "<error message>"}
    data: [DONE]
    ```
    """

    async def event_generator() -> AsyncIterator[dict]:
        async for event in run_agent_stream(request.query, state.tools):
            yield {"data": serialize_event(event)}
        yield {"data": "[DONE]"}

    return EventSourceResponse(event_generator())
