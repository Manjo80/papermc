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


def find_velocity_servers(base_dir: Path) -> list[Path]:
    """Findet installierte Velocity-Server im BASE_DIR."""
    servers = []
    for path in base_dir.iterdir():
        if path.is_dir() and (path / "velocity.toml").exists():
            servers.append(path)
    return servers


def get_forwarding_secret(velocity_dir: Path) -> str:
    """Liest die forwarding.secret-Datei eines Velocity-Servers."""
    secret_path = velocity_dir.parent / "forwarding.secret"
    if not secret_path.exists():
        raise FileNotFoundError(f"forwarding.secret nicht gefunden: {secret_path}")
    return secret_path.read_text().strip()
