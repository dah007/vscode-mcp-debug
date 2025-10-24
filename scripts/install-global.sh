#!/bin/bash
# Global installation script for MCP Debug Server
# This installs the server so it can be run from anywhere

echo -e "\033[0;32m🚀 Installing MCP Debug Server Globally...\033[0m"

# Get the absolute path to the server directory
SERVER_DIR="$(cd ."$(dirname "${BASH_SOURCE[0]}")/server" && pwd)"
echo -e "\033[0;33m📁 Server directory: $SERVER_DIR\033[0m"

# Create virtual environment if it doesn't exist
if [ ! -d "$SERVER_DIR/venv" ]; then
    echo -e "\033[0;33m-- Creating virtual environment...\033[0m"
    cd "$SERVER_DIR"
    python3 -m venv venv
fi

# Install dependencies
echo -e "\033[0;33m-- Installing dependencies...\033[0m"
cd "$SERVER_DIR"
source venv/bin/activate
pip install -r requirements.txt

# Create a global launcher script
LAUNCHER_PATH="$HOME/.local/bin/mcp-debug-server"
echo -e "\033[0;33m-- Creating global launcher at $LAUNCHER_PATH\033[0m"

mkdir -p "$HOME/.local/bin"

cat > "$LAUNCHER_PATH" << EOF
#!/bin/bash
# MCP Debug Server Launcher

# Kill any existing process on port 8001
echo -e "\033[0;33m🔍 Checking for existing server on port 8001...\033[0m"
PID=\$(lsof -ti:8001)
if [ -n "\$PID" ]; then
    echo -e "\033[0;33m⚠️  Killing existing process (PID: \$PID)\033[0m"
    kill -9 \$PID 2>/dev/null
    sleep 1
fi

echo -e "\033[0;32m🚀 Starting MCP Debug Server...\033[0m"
cd "$SERVER_DIR"
source venv/bin/activate
python3 -m uvicorn main:app --host 127.0.0.1 --port 8001 "\$@"
EOF

chmod +x "$LAUNCHER_PATH"

# Check if ~/.local/bin is in PATH
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    echo -e "\033[0;33m⚠️  Adding $HOME/.local/bin to PATH...\033[0m"
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
    echo -e "\033[0;33m   Run: source ~/.bashrc  (or restart terminal)\033[0m"
fi

echo -e "\033[0;32m✅ Installation complete!\033[0m"
echo -e "\033[0;36m"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "To start the server from anywhere, run:"
echo "  mcp-debug-server"
echo ""
echo "With auto-reload:"
echo "  mcp-debug-server --reload"
echo ""
echo "To stop the server:"
echo "  pkill -f 'uvicorn main:app'"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "\033[0m"
