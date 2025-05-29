import os
from pathlib import Path

BASE_DIR = Path("/opt/minecraft")

def detect_velocity():
    for svc in os.listdir("/etc/systemd/system"):
        if svc.startswith("velocity-") and svc.endswith(".service"):
            name = svc.replace("velocity-", "").replace(".service", "")
            dir_path = BASE_DIR / f"velocity-{name}"
            toml = dir_path / "velocity.toml"
            secret = BASE_DIR / "forwarding.secret"
            if toml.exists() and secret.exists():
                return name, dir_path, toml, secret
    return None, None, None, None
