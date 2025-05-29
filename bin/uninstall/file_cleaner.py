import shutil
from pathlib import Path

BASE_DIR = Path("/opt/minecraft")

def delete_server_directory(server_type: str, name: str):
    path = BASE_DIR / f"{server_type}-{name}"
    if path.exists() and path.is_dir():
        print(f"🗑️  Lösche Serververzeichnis: {path}")
        shutil.rmtree(path)
    else:
        print(f"⚠️  Verzeichnis nicht gefunden: {path}")
