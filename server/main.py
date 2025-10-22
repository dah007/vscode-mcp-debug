from fastapi import FastAPI, Request
from tools import mcp
from store import debug_data, debug_sessions, current_session
from datetime import datetime

# Create a FastAPI app
app = FastAPI()

# Mount the MCP server at a subpath
app.mount("/mcp", mcp.http_app())

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