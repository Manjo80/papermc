from pathlib import Path

BASE_DIR = Path("/opt/minecraft")

def list_paper_servers():
    return sorted([
        d.name.replace("paper-", "")
        for d in BASE_DIR.iterdir()
        if d.is_dir() and d.name.startswith("paper-")
    ])
