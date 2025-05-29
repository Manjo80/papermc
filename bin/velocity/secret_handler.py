# velocity/secret_handler.py

from pathlib import Path
import shutil

BASE_DIR = Path("/opt/minecraft")

def copy_forwarding_secret(server_dir: Path):
    """
    Kopiert die forwarding.secret vom Velocity-Server ins zentrale BASE_DIR.
    """
    source = server_dir / "forwarding.secret"
    destination = BASE_DIR / "forwarding.secret"

    if source.exists():
        shutil.copy2(source, destination)
        print("➡️  forwarding.secret wurde kopiert.")
    else:
        print("❌ forwarding.secret nicht gefunden in", source)
