from invoke import task
import zipfile
import os

@task
def clean(c):
    print("🧹 Cleaning project...")
    folders = ['__pycache__', '.venv', 'venv', '.env', 'env', 'build', 'dist', '.pytest_cache']
    files = ['.coverage']
    extensions = ['.pyc', '.pyo', '.log']

    for root, dirs, file_names in os.walk('.'):
        for d in dirs:
            if d in folders:
                c.run(f'rm -rf "{os.path.join(root, d)}"')
        for f in file_names:
            if any(f.endswith(ext) for ext in extensions) or f in files:
                c.run(f'rm -f "{os.path.join(root, f)}"')

@task(pre=[clean])
def zip(c):
    print("📦 Creating zip archive...")
    zip_name = "fastapi_app.zip"
    with zipfile.ZipFile(zip_name, 'w') as zipf:
        for root, dirs, files in os.walk('.'):
            if any(x in root for x in ['.git', '__pycache__', 'build', 'dist', '.venv', 'venv', '.env', 'env', '.pytest_cache', '.vscode', '.idea']):
                continue
            for file in files:
                if any(file.endswith(ext) for ext in ['.pyc', '.pyo', '.log']) or file in ['.coverage']:
                    continue
                zipf.write(os.path.join(root, file))
