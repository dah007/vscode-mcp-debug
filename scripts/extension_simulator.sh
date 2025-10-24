#!/usr/bin/env bash
set -euo pipefail

BASE=http://127.0.0.1:8001/sse/

echo "1) Probe SSE endpoint for session id"
HEADERS=$(curl -i -s -H "Accept: text/event-stream" ${BASE} | sed -n '1,120p')
echo "$HEADERS"
SID=$(echo "$HEADERS" | sed -n '1,120p' | grep -i '^mcp-session-id:' | awk '{print $2}' | tr -d '\r') || true
if [ -n "$SID" ]; then
  echo "Found mcp-session-id: $SID"
else
  echo "No mcp-session-id found in probe (server may accept direct subscriptions)"
fi

echo
echo "2) Attempt a short streaming GET (4s)"
if [ -n "$SID" ]; then
  timeout 4s curl -H "Accept: text/event-stream" -H "mcp-session-id: $SID" ${BASE} || true
else
  timeout 4s curl -H "Accept: text/event-stream" ${BASE} || true
fi

echo
echo "3) POST sample debug events to /debug-data"
curl -s -X POST http://127.0.0.1:8001/debug-data -H 'Content-Type: application/json' -d '{"sessionStarted":{"id":"sim-1","name":"sim","type":"sim","timestamp":"2025-10-23T00:00:00Z"}}' | sed -n '1,120p' || true
curl -s -X POST http://127.0.0.1:8001/debug-data -H 'Content-Type: application/json' -d '{"debugEvent":{"event":"simulated","body":{"msg":"hello"},"timestamp":"2025-10-23T00:00:01Z"}}' | sed -n '1,120p' || true

echo
echo "Simulator finished"
