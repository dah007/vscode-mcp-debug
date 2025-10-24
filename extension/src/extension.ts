import fetch from 'node-fetch';
import * as vscode from 'vscode';

// Helper function to get server URL from configuration
function getServerUrl(): string {
    const config = vscode.workspace.getConfiguration('debugDataForwarder');
    return config.get('serverUrl', 'http://localhost:8001/debug-data'); // TODO: make this defaulted from a vs code setting
}

// Helper function to check if forwarding is enabled
function isForwardingEnabled(): boolean {
    const config = vscode.workspace.getConfiguration('debugDataForwarder');
    return config.get('enabled', true);
}

// Helper function to send data to MCP server
async function sendToMCPServer(data: any) {
    if (!isForwardingEnabled()) {
        return;
    }

    try {
        const serverUrl = getServerUrl();
        const response = await fetch(serverUrl, {
            method: 'POST',
            body: JSON.stringify(data),
            headers: { 'Content-Type': 'application/json' },
        });

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }

        console.log('Debug data sent successfully:', Object.keys(data));
    } catch (error: any) {
        // Detailed logging to help diagnose network/fetch issues.
        console.error('Failed to send debug data to MCP server:', error);

        // Try a pragmatic fallback: if the configured URL is an SSE/streamable
        // endpoint (for example ends with /sse or /sse/), attempt to POST to the
        // legacy `/debug-data` endpoint on the same host. This helps when the
        // extension environment cannot open an SSE/streamable connection but the
        // server still accepts POSTs for debug forwarding.
        try {
            const serverUrl = getServerUrl();
            const fallback = serverUrl.replace(/\/sse\/?$/i, '/debug-data');
            if (fallback !== serverUrl) {
                console.warn(`Attempting fallback POST to ${fallback}`);
                const fbResp = await fetch(fallback, {
                    method: 'POST',
                    body: JSON.stringify(data),
                    headers: { 'Content-Type': 'application/json' },
                });
                if (fbResp.ok) {
                    console.log(
                        'Fallback debug data POST succeeded',
                        Object.keys(data)
                    );
                    return;
                } else {
                    console.error(
                        `Fallback POST failed: HTTP ${fbResp.status}: ${fbResp.statusText}`
                    );
                }
            }
        } catch (fbErr: any) {
            console.error('Fallback POST attempt also failed:', fbErr);
        }

        // Show a user-facing warning with the original error message.
        vscode.window.showWarningMessage(
            `Failed to send debug data: ${error?.message || error}`
        );
    }
}

// TODO: understand this better
// Minimal MCP streaming client helper. If the configured server URL points to
// an SSE/streamable endpoint (for example ends with /sse or contains /sse),
// attempt a lightweight handshake: probe to obtain an `mcp-session-id` then
// open a streaming GET including that header. Incoming chunks are logged for
// debugging and can be parsed/forwarded as needed.
let _mcpStreamAbort: (() => void) | null = null;

async function startMCPStreamIfConfigured() {
    const serverUrl = getServerUrl();
    if (!/\/sse\/?($|\?)/i.test(serverUrl)) {
        console.error('MCP SSE not configured, serverUrl:', serverUrl);
        return;
    }

    try {
        console.log('Probing MCP SSE endpoint:', serverUrl);
        // Initial probe to get an mcp-session-id header if server issues one
        const probe = await fetch(serverUrl, {
            method: 'GET',
            headers: { Accept: 'text/event-stream' },
            redirect: 'manual' as any,
        });
        const sid =
            probe.headers && (probe.headers as any).get
                ? (probe.headers as any).get('mcp-session-id')
                : undefined;

        if (sid) console.log('MCP probe returned session id:', sid);

        // Now open a streaming connection including the session id (if any)
        const streamHeaders: any = { Accept: 'text/event-stream' };
        if (sid) streamHeaders['mcp-session-id'] = sid;

        const res = await fetch(serverUrl, {
            method: 'GET',
            headers: streamHeaders,
        });
        if (!res.ok) {
            console.warn(`MCP stream handshake failed: HTTP ${res.status} ${res.statusText}`);
            return;
        }

        // Node fetch exposes a readable stream on `res.body`.
        const nodeStream: any = (res as any).body;
        if (!nodeStream || typeof nodeStream.on !== 'function') {
            console.warn('MCP stream: response body is not a readable stream');
            return;
        }

        let buffer = '';

        const onData = (chunk: Buffer) => {
            try {
                buffer += chunk.toString('utf8');
                // Split into lines to make output readable. MCP/Server-Sent-Events use
                // line-oriented framing (e.g., `data:` lines). We'll simply log non-empty lines.
                const parts = buffer.split(/\r?\n/);
                // keep last partial line in buffer
                buffer = parts.pop() || '';

                for (const line of parts) {
                    if (!line) continue;
                    // Strip leading `data:` if present
                    const trimmed = line.replace(/^data:\s*/i, '');
                    console.info('MCP EVENT:', trimmed);
                }
            } catch (e) {
                console.error('Error processing MCP stream chunk:', e);
            }
        };

        const onError = (err: any) => {
            console.error('MCP stream error:', err);
            stopMCPStream();
        };

        const onEnd = () => {
            console.log('MCP stream ended');
            stopMCPStream();
        };

        nodeStream.on('data', onData);
        nodeStream.on('error', onError);
        nodeStream.on('end', onEnd);

        _mcpStreamAbort = () => {
            try {
                nodeStream.off && nodeStream.off('data', onData);
                nodeStream.off && nodeStream.off('error', onError);
                nodeStream.off && nodeStream.off('end', onEnd);
                // There is no standard abort on the node stream; close the underlying socket if available
                if (typeof nodeStream.destroy === 'function')
                    nodeStream.destroy();
            } catch (e) {
                console.error('Error aborting MCP stream:', e);
            }
            _mcpStreamAbort = null;
        };

        console.log('MCP stream opened successfully');
    } catch (err: any) {
        console.error('Failed to open MCP stream:', err);
        // leave existing fallback behavior in sendToMCPServer to POST to /debug-data
    }
}

function stopMCPStream() {
    if (_mcpStreamAbort) {
        try {
            _mcpStreamAbort();
        } finally {
            _mcpStreamAbort = null;
        }
    }
}

export function activate(context: vscode.ExtensionContext) {
    console.log('VS Code Debug MCP Extension activated');

    // Attempt to start streaming if the configured server URL points at /sse
    // This runs in the background and will log incoming MCP events to console.
    startMCPStreamIfConfigured().catch((e) =>
        console.error('startMCPStreamIfConfigured error:', e)
    );

    // Monitor debug sessions starting
    vscode.debug.onDidStartDebugSession(
        async (session: vscode.DebugSession) => {
            console.info('Debug session started:', session.name);

            // Send initial session info
            sendToMCPServer({
                sessionStarted: {
                    name: session.name,
                    type: session.type,
                    id: session.id,
                    timestamp: new Date().toISOString(),
                },
            });

            // Get initial variables
            try {
                const variables = await session.customRequest('variables');
                sendToMCPServer({ variables });
            } catch (error: any) {
                console.error('Failed to get variables:', error);
            }
        }
    );

    // Monitor debug console output
    vscode.debug.onDidReceiveDebugSessionCustomEvent(
        (event: vscode.DebugSessionCustomEvent) => {
            console.info('%cDebug session custom event received:', 'color: blue;background:white;font-weight:bold;font-size:14px', event);
            // Capture various debug events
            sendToMCPServer({
                debugEvent: {
                    event: event.event,
                    body: event.body,
                    timestamp: new Date().toISOString(),
                    sessionId: event.session.id,
                    sessionName: event.session.name,
                },
            });
        }
    );

    // Monitor debug session termination
    vscode.debug.onDidTerminateDebugSession((session: vscode.DebugSession) => {
        console.log('Debug session terminated:', session.name);
        sendToMCPServer({
            sessionTerminated: {
                name: session.name,
                id: session.id,
                timestamp: new Date().toISOString(),
            },
        });
    });

    // Also listen for stack trace and breakpoint changes
    vscode.debug.onDidChangeActiveStackItem(
        async (
            stackItem: vscode.DebugThread | vscode.DebugStackFrame | undefined
        ) => {
            if (stackItem && vscode.debug.activeDebugSession) {
                try {
                    const stack =
                        await vscode.debug.activeDebugSession.customRequest(
                            'stackTrace'
                        );
                    sendToMCPServer({ stack });
                } catch (error: any) {
                    console.error('Failed to get stack trace:', error);
                }
            }
        }
    );

    vscode.debug.onDidChangeBreakpoints(
        (event: vscode.BreakpointsChangeEvent) => {
            const breakpoints = vscode.debug.breakpoints.map(
                (bp: vscode.Breakpoint) => ({
                    id: bp.id,
                    enabled: bp.enabled,
                    condition: (bp as any).condition,
                    hitCondition: (bp as any).hitCondition,
                    logMessage: (bp as any).logMessage,
                })
            );

            sendToMCPServer({ breakpoints });
        }
    );
}

export function deactivate() {
    console.log('VS Code Debug MCP Extension deactivated');
}
