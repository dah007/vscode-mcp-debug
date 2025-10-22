# API Reference - VS Code Debug MCP

[< Back](../README.md)

## Base URL
```
http://localhost:8001
```

## Authentication
No authentication required for local development.

---

## Health Check

### GET /health
Check if the server is running and healthy.

**Response:**
```json
{
  "status": "healthy"
}
```

**Status Codes:**
- `200` - Server is healthy
- `500` - Server error

**Example:**
```bash
curl http://localhost:8001/health
```

---

## Debug Data Management

### GET /debug-data
Retrieve all currently stored debug data.

**Response:**
```json
{
  "variables": {
    "x": 10,
    "y": 20,
    "result": 30,
    "items": [1, 2, 3]
  },
  "stack": [
    {
      "id": 1,
      "name": "main",
      "line": 25,
      "source": "test_debug.py"
    }
  ],
  "breakpoints": [
    {
      "id": "bp1",
      "enabled": true,
      "condition": null,
      "hitCondition": null,
      "logMessage": null
    }
  ],
  "sessionStarted": {
    "name": "test_debug.py",
    "type": "debugpy",
    "id": "session-abc123",
    "timestamp": "2025-10-21T20:30:00.000Z"
  },
  "sessionTerminated": {
    "name": "test_debug.py",
    "id": "session-abc123",
    "timestamp": "2025-10-21T20:35:00.000Z"
  },
  "debugEvent": {
    "event": "output",
    "body": {
      "category": "stdout",
      "output": "Debug message\n"
    },
    "timestamp": "2025-10-21T20:32:00.000Z",
    "sessionId": "session-abc123",
    "sessionName": "test_debug.py"
  }
}
```

**Example:**
```bash
curl http://localhost:8001/debug-data
```

### POST /debug-data
Send debug data to be stored on the server. The request body can contain any combination of the supported data types.

**Request Body:**
```json
{
  "variables": { /* variable data */ },
  "stack": [ /* stack frame data */ ],
  "breakpoints": [ /* breakpoint data */ ],
  "sessionStarted": { /* session start data */ },
  "sessionTerminated": { /* session end data */ },
  "debugEvent": { /* debug event data */ }
}
```

**Response:**
```json
{
  "status": "ok"
}
```

**Status Codes:**
- `200` - Data stored successfully
- `400` - Invalid JSON
- `500` - Server error

---

## Data Types

### Variables
```json
{
  "variables": {
    "variable_name": "value",
    "number": 42,
    "list": [1, 2, 3],
    "object": {"key": "value"}
  }
}
```

### Stack Trace
```json
{
  "stack": [
    {
      "id": 1,
      "name": "function_name",
      "line": 25,
      "source": "filename.py"
    }
  ]
}
```

### Breakpoints
```json
{
  "breakpoints": [
    {
      "id": "unique_id",
      "enabled": true,
      "condition": "x > 10",
      "hitCondition": ">=2",
      "logMessage": "Value is {x}"
    }
  ]
}
```

### Session Started
```json
{
  "sessionStarted": {
    "name": "script_name.py",
    "type": "debugpy",
    "id": "unique_session_id",
    "timestamp": "2025-10-21T20:30:00.000Z"
  }
}
```

### Session Terminated
```json
{
  "sessionTerminated": {
    "name": "script_name.py",
    "id": "unique_session_id",
    "timestamp": "2025-10-21T20:35:00.000Z"
  }
}
```

### Debug Event
```json
{
  "debugEvent": {
    "event": "output",
    "body": {
      "category": "stdout",
      "output": "Debug message\n"
    },
    "timestamp": "2025-10-21T20:32:00.000Z",
    "sessionId": "unique_session_id",
    "sessionName": "script_name.py"
  }
}
```

---

## MCP Tools

### GET /mcp/tools
List available MCP tools.

### POST /mcp/tools/{tool_name}
Execute an MCP tool.

**Available Tools:**
- `get_variables` - Returns current debug variables
- `get_stack_trace` - Returns current stack trace
- `get_breakpoints` - Returns current breakpoints

---

## Error Responses

All endpoints may return error responses in the following format:

```json
{
  "detail": "Error description"
}
```

**Common Status Codes:**
- `400` - Bad Request (invalid JSON, missing required fields)
- `404` - Not Found (endpoint doesn't exist)
- `500` - Internal Server Error
- `503` - Service Unavailable (server starting up)

---

## Examples

### Complete Debug Session Flow

1. **Session Start:**
```bash
curl -X POST http://localhost:8001/debug-data \
  -H "Content-Type: application/json" \
  -d '{
    "sessionStarted": {
      "name": "my_script.py",
      "type": "debugpy",
      "id": "session-123",
      "timestamp": "2025-10-21T20:30:00.000Z"
    }
  }'
```

2. **Send Variables:**
```bash
curl -X POST http://localhost:8001/debug-data \
  -H "Content-Type: application/json" \
  -d '{
    "variables": {
      "x": 10,
      "y": 20,
      "result": 30
    }
  }'
```

3. **Send Console Output:**
```bash
curl -X POST http://localhost:8001/debug-data \
  -H "Content-Type: application/json" \
  -d '{
    "debugEvent": {
      "event": "output",
      "body": {
        "category": "stdout",
        "output": "Processing data...\n"
      },
      "timestamp": "2025-10-21T20:32:00.000Z",
      "sessionId": "session-123"
    }
  }'
```

4. **Session End:**
```bash
curl -X POST http://localhost:8001/debug-data \
  -H "Content-Type: application/json" \
  -d '{
    "sessionTerminated": {
      "name": "my_script.py",
      "id": "session-123",
      "timestamp": "2025-10-21T20:35:00.000Z"
    }
  }'
```

5. **Retrieve All Data:**
```bash
curl http://localhost:8001/debug-data
```

---

## Rate Limiting
No rate limiting is currently implemented for local development.

## Versioning
API Version: 1.0  
This API follows semantic versioning principles.