from fastapi import FastAPI, Request
from tools import mcp
from store import debug_data

# Create a FastAPI app
app = FastAPI()

# Mount the MCP server at a subpath
app.mount("/mcp", mcp.http_app())

@app.post("/debug-data")
async def receive_debug_data(request: Request):
    data = await request.json()
    debug_data.update(data)
    return {"status": "ok"}

@app.get("/debug-data")
async def send_debug_data():
    return debug_data

@app.get("/health")
async def health_check():
    return {"status": "healthy"}