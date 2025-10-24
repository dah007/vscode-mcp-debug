#!/usr/bin/env python3
"""Example MCP StreamableHTTP client.

This script demonstrates the minimal handshake required to subscribe to the
server's StreamableHTTP/SSE endpoint mounted at /sse/. It performs an initial
GET to obtain an `mcp-session-id` (if the server issues one on 400 responses),
then performs a persistent GET including that header to receive streaming
events.

Usage, from the project root:
    python3 scripts/example_mcp_client.py --base http://127.0.0.1:8001/sse/ --timeout 20

Notes:
- This is a minimal example for development/debugging. A full MCP client
    should implement the session lifecycle, message formats, and error handling
    according to the MCP/fastmcp docs or use an official client library.
"""

import argparse
import requests
import time
import sys


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", default="http://127.0.0.1:8001/sse/", help="Base SSE URL (include trailing slash)")
    parser.add_argument("--timeout", type=int, default=20, help="How many seconds to listen before exiting")
    args = parser.parse_args()

    base = args.base
    timeout = args.timeout

    headers = {"Accept": "text/event-stream"}

    print(f"Probing {base} to get session id...")
    
    try:
        r = requests.get(base, headers=headers, timeout=5, allow_redirects=False)
    except Exception as e:
        print("Initial probe failed:", e)
        sys.exit(2)

    print("Initial response:", r.status_code)
    sid = r.headers.get("mcp-session-id")
    if sid:
        print("Received mcp-session-id:", sid)
    else:
        print("No mcp-session-id received. Server may accept direct sessions or returned an error body.")

    if not sid:
        # If server didn't provide an mcp-session-id but returned 200, try subscribe directly
        if r.status_code == 200:
            print("Server accepted direct subscription. Streaming...\n")
            try:
                with requests.get(base, headers=headers, stream=True, timeout=timeout) as stream:
                    start = time.time()
                    for line in stream.iter_lines(decode_unicode=True):
                        if line:
                            print("EVENT:", line)
                        if time.time() - start > timeout:
                            break
            except Exception as e:
                print("Streaming error:", e)
                sys.exit(3)
        else:
            print("Cannot proceed without an MCP session id. Exiting.")
            sys.exit(4)
    else:
        # Use the provided session id to subscribe
        sub_headers = headers.copy()
        sub_headers["mcp-session-id"] = sid
        print(f"Opening streaming connection with mcp-session-id for up to {timeout}s...")
        try:
            with requests.get(base, headers=sub_headers, stream=True, timeout=timeout) as stream:
                start = time.time()
                for line in stream.iter_lines(decode_unicode=True):
                    if line:
                        print("EVENT:", line)
                    if time.time() - start > timeout:
                        print("Timeout reached, closing subscription")
                        break
        except Exception as e:
            print("Streaming connection failed:", e)
            sys.exit(5)

    print("Client finished")


if __name__ == "__main__":
    main()
