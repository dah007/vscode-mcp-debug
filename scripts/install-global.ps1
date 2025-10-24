# Global installation script for MCP Debug Server (PowerShell)
# This installs the server so it can be run from anywhere

Write-Host "🚀 Installing MCP Debug Server Globally..." -ForegroundColor Green

# Get the absolute path to the server directory
$ServerDir = Join-Path $PSScriptRoot "server"
Write-Host "📁 Server directory: $ServerDir" -ForegroundColor Yellow

# Create virtual environment if it doesn't exist
if (-not (Test-Path "$ServerDir\venv")) {
    Write-Host "-- Creating virtual environment..." -ForegroundColor Yellow
    Set-Location $ServerDir
    python -m venv venv
}

# Install dependencies
Write-Host "-- Installing dependencies..." -ForegroundColor Yellow
Set-Location $ServerDir
& .\venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Create a global launcher script
$LauncherDir = "$env:USERPROFILE\.local\bin"
$LauncherPath = Join-Path $LauncherDir "mcp-debug-server.ps1"
Write-Host "-- Creating global launcher at $LauncherPath" -ForegroundColor Yellow

New-Item -ItemType Directory -Force -Path $LauncherDir | Out-Null

@"
# MCP Debug Server Launcher

# Kill any existing process on port 8001
Write-Host "🔍 Checking for existing server on port 8001..." -ForegroundColor Yellow
`$existingProcess = Get-NetTCPConnection -LocalPort 8001 -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess -Unique
if (`$existingProcess) {
    Write-Host "⚠️  Killing existing process (PID: `$existingProcess)" -ForegroundColor Yellow
    Stop-Process -Id `$existingProcess -Force -ErrorAction SilentlyContinue
    Start-Sleep -Seconds 1
}

Write-Host "🚀 Starting MCP Debug Server..." -ForegroundColor Green
Set-Location "$ServerDir"
& .\venv\Scripts\Activate.ps1
python -m uvicorn main:app --host 127.0.0.1 --port 8001 `$args
"@ | Set-Content -Path $LauncherPath

# Check if launcher dir is in PATH
$CurrentPath = [Environment]::GetEnvironmentVariable("Path", "User")
if ($CurrentPath -notlike "*$LauncherDir*") {
    Write-Host "⚠️  Adding $LauncherDir to PATH..." -ForegroundColor Yellow
    [Environment]::SetEnvironmentVariable(
        "Path",
        "$CurrentPath;$LauncherDir",
        "User"
    )
    Write-Host "   Restart PowerShell for PATH changes to take effect" -ForegroundColor Yellow
}

Write-Host "✅ Installation complete!" -ForegroundColor Green
Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "To start the server from anywhere, run:" -ForegroundColor Cyan
Write-Host "  powershell $LauncherPath" -ForegroundColor White
Write-Host ""
Write-Host "Or create an alias in your PowerShell profile:" -ForegroundColor Cyan
Write-Host "  Set-Alias mcp-debug-server '$LauncherPath'" -ForegroundColor White
Write-Host ""
Write-Host "With auto-reload:" -ForegroundColor Cyan
Write-Host "  powershell $LauncherPath --reload" -ForegroundColor White
Write-Host ""
Write-Host "To stop the server:" -ForegroundColor Cyan
Write-Host "  Stop-Process -Name 'python' -Force" -ForegroundColor White
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
