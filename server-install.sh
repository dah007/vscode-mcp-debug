#!/bin/bash
cd server
# Setup script for MCP server
echo ""
echo -e "\033[0;32mSetting up MCP server...\033[0m"
echo ""
# Create virtual environment
echo -e "\033[0;33m-- Creating virtual environment...\033[0m"
python3 -m venv venv
source venv/bin/activate
# Install server dependencies
echo -e "\033[0;33m-- Installing server dependencies...\033[0m"
pip install -r requirements.txt
echo ""
echo -e "\033[0;32mSetup complete!\033[0m"
echo ""