import fetch from "node-fetch";
import * as vscode from "vscode";

// Helper function to get server URL from configuration
function getServerUrl(): string {
  const config = vscode.workspace.getConfiguration("debugDataForwarder");
  return config.get("serverUrl", "http://localhost:8001/debug-data");
}

// Helper function to check if forwarding is enabled
function isForwardingEnabled(): boolean {
  const config = vscode.workspace.getConfiguration("debugDataForwarder");
  return config.get("enabled", true);
}

// Helper function to send data to MCP server
async function sendToMCPServer(data: any) {
  if (!isForwardingEnabled()) {
    return;
  }

  try {
    const serverUrl = getServerUrl();
    const response = await fetch(serverUrl, {
      method: "POST",
      body: JSON.stringify(data),
      headers: { "Content-Type": "application/json" },
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    console.log("Debug data sent successfully:", Object.keys(data));
  } catch (error: any) {
    console.error("Failed to send debug data:", error);
    vscode.window.showWarningMessage(
      `Failed to send debug data: ${error.message}`
    );
  }
}

export function activate(context: vscode.ExtensionContext) {
  console.log("VS Code Debug MCP Extension activated");

  // Monitor debug sessions starting
  vscode.debug.onDidStartDebugSession(async (session: vscode.DebugSession) => {
    console.log("Debug session started:", session.name);

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
      const variables = await session.customRequest("variables");
      sendToMCPServer({ variables });
    } catch (error: any) {
      console.error("Failed to get variables:", error);
    }
  });

  // Monitor debug console output
  vscode.debug.onDidReceiveDebugSessionCustomEvent(
    (event: vscode.DebugSessionCustomEvent) => {
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
    console.log("Debug session terminated:", session.name);
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
          const stack = await vscode.debug.activeDebugSession.customRequest(
            "stackTrace"
          );
          sendToMCPServer({ stack });
        } catch (error: any) {
          console.error("Failed to get stack trace:", error);
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
  console.log("VS Code Debug MCP Extension deactivated");
}
