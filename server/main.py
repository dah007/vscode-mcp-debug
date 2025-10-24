from fastapi import FastAPI, Request
from tools import mcp

# NOTE about mounting FastMCP http_app:
# The FastMCP helper `http_app(path=...)` registers routes relative to the
# provided `path`. When mounting that Starlette/Starlette-like app into a
# parent FastAPI app (via `app.mount("/sse", subapp)`), you must ensure the
# inner app's registered routes are rooted correctly. If the inner app
# registers the same prefix you mount it at (for example, inner path="/sse"
# and you mount at "/sse"), requests will need to hit "/sse/sse" which is
# confusing and leads to 404s. Additionally, the StreamableHTTP session
# manager requires its lifespan to be executed so that its task group is
# initialized; to ensure that happens we pass the subapp's lifespan into the
# parent `FastAPI(lifespan=...)` so the inner lifecycle starts/stops with the
# parent app. This prevents runtime errors that would otherwise result in 500
# responses on SSE connection attempts.
from store import debug_data, debug_sessions, current_session
from datetime import datetime

# Create a FastAPI app
app = FastAPI()

# Create the MCP http app and pass its lifespan into the parent FastAPI app.
# This ensures the FastMCP StreamableHTTP session manager is started as part
# of the parent's lifespan and avoids "Task group is not initialized" runtime
# errors which resulted in 500 responses on SSE requests.
mcp_app = mcp.http_app(path="/")

# Pass the subapp lifespan into the parent app so subapp lifespan runs.
app = FastAPI(lifespan=mcp_app.lifespan)

# Mount the MCP HTTP server at /sse (supports SSE protocol)
app.mount("/sse", mcp_app)

@app.post("/debug-data")
async def receive_debug_data(request: Request):
    global current_session
    data = await request.json()
    
    # Check if this is a new session starting
    if "sessionStarted" in data:
        # Create a new session object
        session_info = data["sessionStarted"]
        current_session = {
            "id": session_info.get("id"),
            "name": session_info.get("name"),
            "type": session_info.get("type"),
            "startTime": session_info.get("timestamp"),
            "endTime": None,
            "events": [],
            "variables": {},
            "stack": [],
            "breakpoints": []
        }
        debug_sessions.append(current_session)
        current_session["events"].append({"type": "sessionStarted", "data": session_info})
    
    # If we have a current session, add events to it
    elif current_session:
        if "sessionTerminated" in data:
            current_session["endTime"] = data["sessionTerminated"].get("timestamp")
            current_session["events"].append({"type": "sessionTerminated", "data": data["sessionTerminated"]})
            current_session = None
        elif "debugEvent" in data:
            current_session["events"].append({"type": "debugEvent", "data": data["debugEvent"]})
        elif "variables" in data:
            current_session["variables"] = data["variables"]
            current_session["events"].append({"type": "variables", "data": data["variables"]})
        elif "stack" in data:
            current_session["stack"] = data["stack"]
            current_session["events"].append({"type": "stack", "data": data["stack"]})
        elif "breakpoints" in data:
            current_session["breakpoints"] = data["breakpoints"]
            current_session["events"].append({"type": "breakpoints", "data": data["breakpoints"]})
    
    # Also update the legacy debug_data structure with latest values
    debug_data.update(data)
    debug_data["sessions"] = debug_sessions
    
    return {"status": "ok", "sessionsCount": len(debug_sessions)}

@app.get("/debug-data")
async def send_debug_data():
    return {
        **debug_data,
        "sessions": debug_sessions,
        "totalSessions": len(debug_sessions)
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/mcp-info")
async def mcp_info():
    """Get information about available MCP tools"""
    return {
        "mcp_server": mcp.name,
        "sse_endpoint": "/sse",
        "tools": [
            {
                "name": "get_variables",
                "description": "Returns the latest debug variables"
            },
            {
                "name": "get_stack_trace",
                "description": "Returns the current stack trace"
            },
            {
                "name": "get_breakpoints",
                "description": "Returns the current breakpoints"
            }
        ],
        "usage": {
            "description": "MCP tools are accessed via SSE (Server-Sent Events) protocol",
            "endpoint": "http://127.0.0.1:8001/sse",
            "protocol": "Model Context Protocol (MCP)",
            "clients": "Use MCP-compatible clients like Claude Desktop, or MCP client libraries"
        }
    }