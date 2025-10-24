# Remove common FastAPI build and cache folders
Get-ChildItem -Recurse -Directory | Where-Object {
    $_.Name -in @('__pycache__', '.venv', 'venv', '.env', 'env', 'build', 'dist', '.pytest_cache')
} | Remove-Item -Recurse -Force

# Remove unwanted files
Get-ChildItem -Recurse -File | Where-Object {
    $_.Name -match '\.pyc$|\.pyo$|\.log$|\.coverage$'
} | Remove-Item -Force
