# MCP Debug Server - Global Setup Guide

This guide explains how to install and run the MCP Debug Server globally so it works with all your Python projects across different workspaces.

## 🚀 Quick Setup

From the scripts directory:

### Linux/macOS/WSL

```bash
# 1. Make the installer executable
chmod +x install-global.sh

# 2. Run the installer
./install-global.sh

# 3. Reload your shell (or restart terminal)
source ~/.bashrc

# 4. Start the server from anywhere
mcp-debug-server
```

### Windows PowerShell

```powershell
# 1. Allow script execution (if needed)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# 2. Run the installer
.\install-global.ps1

# 3. Restart PowerShell

# 4. Start the server from anywhere
powershell "$env:USERPROFILE\.local\bin\mcp-debug-server.ps1"
```

## 🎯 How It Works

The installer:

1. ✅ Creates a virtual environment in the `server/` directory
2. ✅ Installs all Python dependencies
3. ✅ Creates a global launcher script in `~/.local/bin/`
4. ✅ Adds the launcher to your PATH

After installation, you can start the server from **any directory** by running:

```bash
mcp-debug-server
```

## 🔧 Usage

### Start the server

```bash
mcp-debug-server
```

### Start with auto-reload (development mode)

```bash
mcp-debug-server --reload
```

### Stop the server

**Linux/macOS:**

```bash
pkill -f 'uvicorn main:app'
```

**Windows:**

```powershell
Stop-Process -Name python -Force
```

Or just press `Ctrl+C` in the terminal running the server.

## 🌍 Using with Multiple Workspaces

Once installed globally, the server works with **all your Python projects**:

1. **Start the server once** (in any terminal):

    ```bash
    mcp-debug-server
    ```

2. **Open any Python workspace** in VS Code

3. **Start debugging** (F5) - the extension automatically sends data to `localhost:8001`

4. **View collected data** at http://localhost:8001/debug-data

### No workspace-specific configuration needed!

The extension is already configured to connect to `http://localhost:8001/debug-data` by default.

## 📝 VS Code Configuration (Optional)

If you want to **remove the auto-start task** from your workspace (since the server runs globally), update `.vscode/launch.json`:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Debug Test Script",
            "type": "debugpy",
            "request": "launch",
            "program": "${workspaceFolder}/test_debug.py",
            "console": "integratedTerminal",
            "justMyCode": true
        }
    ]
}
```

## 🔄 Running as a Background Service (Advanced)

### Using systemd (Linux)

Create `~/.config/systemd/user/mcp-debug-server.service`:

```ini
[Unit]
Description=MCP Debug Server
After=network.target

[Service]
Type=simple
ExecStart=/home/YOUR_USERNAME/.local/bin/mcp-debug-server
Restart=on-failure

[Install]
WantedBy=default.target
```

Enable and start:

```bash
systemctl --user enable mcp-debug-server
systemctl --user start mcp-debug-server
```

### Using Task Scheduler (Windows)

1. Open Task Scheduler
2. Create Basic Task
3. Trigger: At log on
4. Action: Start a program
5. Program: `powershell`
6. Arguments: `-File "C:\Users\YourName\.local\bin\mcp-debug-server.ps1"`

## 🧪 Testing

After installation:

```bash
# Start the server
mcp-debug-server

# In another terminal, test the health endpoint
curl http://localhost:8001/health

# Expected response: {"status":"healthy"}
```

## 🔍 Troubleshooting

### "Command not found: mcp-debug-server"

**Linux/macOS:**

-   Ensure `~/.local/bin` is in your PATH
-   Run: `source ~/.bashrc` or restart terminal

**Windows:**

-   Restart PowerShell after installation
-   Or run with full path: `powershell "$env:USERPROFILE\.local\bin\mcp-debug-server.ps1"`

### Port already in use

```bash
# Find and kill the process using port 8001
lsof -ti:8001 | xargs kill -9  # Linux/macOS
netstat -ano | findstr :8001    # Windows (then use Task Manager)
```

### Virtual environment issues

```bash
# Re-run the installer
./install-global.sh  # or install-global.ps1
```

## 📊 Monitoring

Check server status:

```bash
# Linux/macOS
ps aux | grep uvicorn

# Windows
Get-Process | Where-Object {$_.ProcessName -eq "python"}
```

View logs in the terminal where the server is running.

## 🎉 Benefits of Global Installation

✅ **One server for all projects** - No need to start/stop per workspace  
✅ **Centralized debug data** - All sessions in one place  
✅ **Easy to manage** - Single command to control  
✅ **Resource efficient** - Only one server instance needed  
✅ **Works anywhere** - Debug any Python file in any directory
