# VS Code Debug MCP Setup Guide

## 📋 Overview

This project integrates VS Code debugging with a Model Context Protocol (MCP) server to capture and forward debug session data. The setup allows you to monitor debug variables, console output, stack traces, and breakpoints through a centralized server.

## 🏗️ Architecture

```
VS Code Debugger → Extension → HTTP → MCP Server → FastMCP Tools
```

### Components
- **VS Code Extension**: Captures debug events and forwards them
- **MCP Server**: FastAPI server with FastMCP integration
- **Data Store**: In-memory storage for debug information
- **API Endpoints**: RESTful endpoints for data access

## 🚀 Quick Start

### 1. Start the MCP Server
```bash
cd server
python -m uvicorn main:app --host 127.0.0.1 --port 8001
```

### 2. Install and Activate Extension
The extension is already compiled in `extension/dist/extension.js`. VS Code will automatically load it when debugging starts.

### 3. Start Debugging
1. Open `test_debug.py` in VS Code
2. Set breakpoints as needed
3. Press F5 or use the debug panel
4. Debug data will automatically be sent to the server

### 4. Monitor Debug Data
Visit `http://localhost:8001/debug-data` to see captured information.

## 🔧 Configuration

### Extension Settings
Configure in VS Code settings (JSON):
```json
{
  "debugDataForwarder.serverUrl": "http://localhost:8001/debug-data",
  "debugDataForwarder.enabled": true
}
```

### Server Configuration
- **Host**: `127.0.0.1`
- **Port**: `8001`
- **Debug Endpoint**: `/debug-data`
- **Health Check**: `/health`
- **MCP Tools**: `/mcp/*`

## 📡 API Endpoints

### Health Check
```http
GET /health
```
Response:
```json
{"status": "healthy"}
```

### Debug Data
```http
GET /debug-data
POST /debug-data
```

#### GET Response Example:
```json
{
  "variables": {"x": 10, "y": 20},
  "stack": [{"id": 1, "name": "main", "line": 25}],
  "breakpoints": [{"id": "bp1", "enabled": true}],
  "sessionStarted": {"name": "test.py", "type": "debugpy"},
  "debugEvent": {"event": "output", "body": {...}}
}
```

#### POST Request Example:
```json
{
  "variables": {"new_var": "value"},
  "sessionStarted": {
    "name": "script.py",
    "type": "debugpy",
    "id": "session-123",
    "timestamp": "2025-10-21T20:30:00"
  }
}
```

## 🔍 What Gets Captured

### Debug Session Events
- Session start/termination
- Session metadata (name, type, ID)
- Timestamps for all events

### Variables
- Local variables in current scope
- Variable types and values
- Complex objects (lists, dictionaries)

### Console Output
- stdout/stderr output
- Debug console messages
- Print statements and logs

### Stack Traces
- Function call stack
- Line numbers and source files
- Stack frame IDs

### Breakpoints
- Breakpoint locations
- Enabled/disabled status
- Conditions and hit counts
- Log messages

## 🛠️ Development

### File Structure
```
vscode-debug-mcp/
├── extension/
│   ├── src/extension.ts          # Extension source code
│   ├── package.json             # Extension manifest
│   └── dist/extension.js        # Compiled extension
├── server/
│   ├── main.py                  # FastAPI server
│   ├── tools.py                 # MCP tools definitions
│   ├── store.py                 # Data storage
│   └── requirements.txt         # Python dependencies
├── test_debug.py                # Sample debug script
├── .vscode/launch.json          # Debug configuration
└── comprehensive_test.py        # Test suite
```

### Building the Extension
```bash
cd extension
npm install
npm run compile
```

### Running Tests
```bash
# Test the complete setup
python comprehensive_test.py

# Test extension data flow
python test_extension_flow.py

# Test MCP tools
cd server
python test_mcp_tools.py
```

## 🔧 Troubleshooting

### Common Issues

#### Server Not Starting
- Check if port 8001 is available
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Verify Python path: Set `PYTHONPATH=.` before running

#### Extension Not Working
- Ensure extension is compiled: `npm run compile`
- Check VS Code settings for `debugDataForwarder.*`
- Verify server URL in configuration

#### No Debug Data
- Confirm server is running: `curl http://localhost:8001/health`
- Check browser network tab for HTTP errors
- Verify debug session is actually starting

### Debug Commands
```bash
# Check server health
curl http://localhost:8001/health

# View current debug data
curl http://localhost:8001/debug-data

# Test server directly
python -c "import requests; print(requests.get('http://localhost:8001/health').json())"
```

## 📚 Dependencies

### Server
- `fastapi` - Web framework
- `fastmcp` - MCP integration
- `uvicorn` - ASGI server

### Extension
- `@types/vscode` - VS Code API types
- `node-fetch` - HTTP client
- `typescript` - TypeScript compiler

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.