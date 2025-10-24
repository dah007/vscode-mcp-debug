#!/bin/bash
# A script to clean up Python project directories by removing unnecessary files and folders.
find . -type d \( -name '__pycache__' -o -name '*.egg-info' -o -name 'build' -o -name 'dist' -o -name '.pytest_cache' -o -name '.venv' -o -name 'venv' -o -name '.env' -o -name 'env' \) -exec rm -rf {} + && find . -type f \( -name '*.pyc' -o -name '*.pyo' -o -name '*.log' -o -name '.coverage' \) -delete
echo "Cleanup completed."