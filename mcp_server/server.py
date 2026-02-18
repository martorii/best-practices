from fastmcp import FastMCP

# 1. Initialize the FastMCP server
mcp = FastMCP("MCPServer")


# 2. Define a Tool (Functions the AI can execute)
@mcp.tool()
def add_numbers(a: int, b: int) -> int:
    """Adds two numbers together."""
    return a + b


# 3. Define a Resource (Data the AI can read)
@mcp.resource("info://about")
def get_info() -> str:
    """Provides information about this server."""
    return "This is a simple MCP server running in Python!"


# 4. Run the server using the standard input/output transport
if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8000)
