# Debug Data Forwarder — Extension README

This README explains how to build and run the `debug-data-forwarder` VS Code extension locally for development and testing.

## Build

From the `extension` folder:

```bash
cd extension
npm install
npm run compile
```

This compiles TypeScript into `dist/extension.js` (the extension entry point).

## Running in Extension Development Host (recommended)

1. Open this repo in VS Code.
2. Open the `extension` folder or ensure it's part of the workspace.
3. Press `F5` to start the Extension Development Host.
4. In the new Dev Host window, start a Python debug session (for example run `test_debug.py` using a Python debug configuration).

The extension will try to open an MCP streaming connection if the configured server URL points to `/sse`. If streaming cannot be opened, it will fallback to POSTing debug data to `http://localhost:8001/debug-data`.

### Config

The extension settings are contributed under `Debug Data Forwarder`:

-   `debugDataForwarder.serverUrl` (default: `http://localhost:8001/debug-data`) — change to `http://localhost:8001/sse/` to attempt streaming.
-   `debugDataForwarder.enabled` — enable/disable forwarding.

## Simulator (no VS Code)

There is a small simulator script at `scripts/extension_simulator.sh` which emulates the extension's network behavior (probe for session id, short streaming probe, and POSTs to `/debug-data`). To run it:

```bash
bash scripts/extension_simulator.sh
```

This is useful when you want to test the server without launching VS Code.

## Notes

-   For real MCP streaming usage, prefer a full MCP client implementation or use the `example_mcp_client.py` under `scripts/` which demonstrates a minimal handshake and stream subscription.
-   The extension's streaming implementation is minimal and aimed at development/debugging; production clients should implement the full MCP protocol or reuse an official client library.

## Run extension dev host (quick snippet)

From the repository root, open VS Code and then either:

-   Press F5 to launch the Extension Development Host (recommended), or
-   Use the following `.vscode/launch.json` in the repository to run and attach quickly:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Run Extension",
            "type": "extensionHost",
            "request": "launch",
            "runtimeExecutable": "${execPath}",
            "args": ["--extensionDevelopmentPath=${workspaceFolder}/extension"]
        }
    ]
}
```

Place that file at `.vscode/launch.json` (or merge into workspace launch settings). Then:

1. Open the project in VS Code.
2. Select the `Run Extension` configuration and start debugging (F5).

The Extension Development Host window will open and load the extension.
