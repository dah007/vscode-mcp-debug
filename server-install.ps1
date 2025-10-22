cd server
# Setup script for MCP server
Write-Host ""
Write-Host "Setting up MCP server..." -ForegroundColor Green
Write-Host ""

# Create virtual environment
Write-Host "-- Creating virtual environment..." -ForegroundColor Yellow
python -m venv venv

# Activate virtual environment
Write-Host "-- Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

# Install server dependencies
Write-Host "-- Installing server dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

Write-Host ""
Write-Host "Setup complete!" -ForegroundColor Green
Write-Host ""