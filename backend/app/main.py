"""
FastAPI server — exposes the ReAct agent over HTTP with Server-Sent Events (SSE).

Endpoints
---------
POST /query          — run the agent; streams SSE events back to the client
GET  /tools          — list all tools currently loaded from the MCP server
GET  /health         — liveness probe
"""

import logging
import os
from contextlib import asynccontextmanager

from app.mcp_client import get_mcp_tools
from app.routers import health, query, tools
from app.state import state
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
)
logger = logging.getLogger(__name__)


# ── Lifespan ───────────────────────────────────────────────────────────────────


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load MCP tools once at startup."""
    logger.info("Loading tools from MCP server …")
    try:
        state.tools = await get_mcp_tools()
        state.tools_loaded = True
        logger.info("Tools loaded: %s", [t.name for t in state.tools])
    except Exception as exc:
        logger.warning("Tool loading failed: %s — agent will run without tools.", exc)
        state.tools = []
        state.tools_loaded = False
    yield
    logger.info("Shutting down.")


# ── Application ────────────────────────────────────────────────────────────────

app = FastAPI(
    title="ReAct Agent",
    description="LangGraph ReAct agent with MCP tool integration — streaming via SSE.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(tools.router)
app.include_router(query.router)


# ── Dev entrypoint ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", "8080")),
        reload=True,
    )
