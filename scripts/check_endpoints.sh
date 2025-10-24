#!/usr/bin/env bash
set -euo pipefail

BASE="http://127.0.0.1:8001"

echo "Checking ${BASE}/health..."
HC=$(curl -s -o /dev/null -w "%{http_code}" ${BASE}/health)
if [ "$HC" != "200" ]; then
  echo "health check failed: HTTP $HC"
  exit 2
fi
echo "  OK (200)"

echo "Checking ${BASE}/mcp-info..."
MCP_INFO=$(curl -s ${BASE}/mcp-info)
if [ -z "$MCP_INFO" ]; then
  echo "mcp-info returned empty"
  exit 3
fi
echo "  mcp-info returned"
echo "$MCP_INFO" | head -n 1

echo "Posting test session to ${BASE}/debug-data..."
POST_CODE=$(curl -s -o /dev/null -w "%{http_code}" -X POST ${BASE}/debug-data -H 'Content-Type: application/json' -d '{"sessionStarted":{"id":"test-1","name":"check","type":"automated","timestamp":"2025-10-22T00:00:00Z"}}')
if [ "$POST_CODE" != "200" ]; then
  echo "POST /debug-data failed: HTTP $POST_CODE"
  exit 4
fi
echo "  POST accepted (200)"

echo "Probing SSE endpoint ${BASE}/sse/ for 4 seconds..."
# Use curl to probe headers and status; allow either 200 or a streaming response
SSE_OUTPUT=$(timeout 4s curl -i -s -H "Accept: text/event-stream" ${BASE}/sse/ || true)
if echo "$SSE_OUTPUT" | grep -q "HTTP/1.1 404"; then
  echo "SSE endpoint returned 404"
  echo "$SSE_OUTPUT" | sed -n '1,40p'
  exit 5
fi
if echo "$SSE_OUTPUT" | grep -q "HTTP/1.1 500"; then
  echo "SSE endpoint returned 500"
  echo "$SSE_OUTPUT" | sed -n '1,80p'
  exit 6
fi

# Print first few lines of headers/body for visibility
echo "SSE endpoint probe response (first 40 lines):"
echo "$SSE_OUTPUT" | sed -n '1,40p'

echo "All checks passed."
exit 0
