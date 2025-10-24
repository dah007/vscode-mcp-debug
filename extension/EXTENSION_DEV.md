# Extension development and testing

This file shows two quick ways to test the extension behavior locally:

-   Run the extension in VS Code's Extension Development Host (recommended for real testing).
-   Use the provided simulator script to exercise the same network behavior the extension uses
    (handshake + fallback POST) without launching VS Code.

Running in VS Code (dev host)

1. Open this repository root in VS Code.
2. Open the `extension` folder as the workspace root or ensure `extension` is present.
3. Press `F5` to Launch Extension (this opens an Extension Development Host window).
4. In the dev host, start a debug session; the extension will attempt to open an MCP SSE stream
   if your configuration points to `/sse`, and will send debug data via POST to `/debug-data`.

## Simulator (no VS Code required)

There is a small simulator script at `scripts/extension_simulator.sh`. It:

-   Probes the configured SSE URL to obtain an `mcp-session-id` (if the server issues one).
-   Attempts a lightweight streaming probe (using `curl` for a few seconds).
-   Sends a couple of test debug events to `/debug-data`.

Usage, from project root:

```
bash scripts/extension_simulator.sh
```

This simulates the network behavior of the extension and is useful when you can't run
the Extension Development Host in this environment.
