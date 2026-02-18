"""
MCP Client — connects to the MCP server over Streamable HTTP and exposes
its tools as LangChain tools.

The server is expected to accept HTTP POST requests at MCP_SERVER_URL + MCP_SERVER_PATH.
"""

import logging
import os

from langchain_core.tools import BaseTool
from langchain_mcp_adapters.client import MultiServerMCPClient

logger = logging.getLogger(__name__)

MCP_SERVER_URL = os.getenv("MCP_SERVER_URL", "http://mcp_server")
MCP_SERVER_PORT = os.getenv("MCP_SERVER_PORT", "8000")
MCP_SERVER_PATH = os.getenv("MCP_SERVER_PATH", "/mcp")


async def get_mcp_tools() -> list[BaseTool]:
    """
    Connect to the MCP server via Streamable HTTP and return all available tools.

    Returns an empty list if the server is unreachable so the agent can still
    answer queries from its own knowledge.
    """
    url = f"{MCP_SERVER_URL}:{MCP_SERVER_PORT}{MCP_SERVER_PATH}"
    logger.info("Connecting to MCP server (streamable_http): %s", url)

    config = {
        "mcp_server": {
            "url": url,
            "transport": "streamable_http",
        }
    }

    try:
        client = MultiServerMCPClient(config)
        tools = await client.get_tools()
        logger.info(
            "Loaded %d tool(s) from MCP server: %s",
            len(tools),
            [t.name for t in tools],
        )
        return tools
    except* Exception as eg:
        import traceback

        for exc in eg.exceptions:
            traceback.print_exception(type(exc), exc, exc.__traceback__)
        raise
