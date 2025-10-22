from fastmcp import FastMCP
from store import debug_data

mcp = FastMCP("VS Code Debug Tools")

@mcp.tool
def get_variables() -> dict:
    """Returns the latest debug variables"""
    return debug_data.get("variables", {})

@mcp.tool
def get_stack_trace() -> list:
    """Returns the current stack trace"""
    return debug_data.get("stack", [])

@mcp.tool
def get_breakpoints() -> list:
    """Returns the current breakpoints"""
    return debug_data.get("breakpoints", [])
