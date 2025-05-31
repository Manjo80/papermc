# config.py

from pathlib import Path
from configparser import ConfigParser

def accept_eula(server_dir: Path):
    """Setzt die EULA auf true."""
    eula_path = server_dir / "eula.txt"
    if not eula_path.exists():
        print("❌ eula.txt nicht gefunden.")
        return

    try:
        with open(eula_path, "w") as f:
            f.write("eula=true\n")
        print("✅ EULA akzeptiert.")
    except Exception as e:
        print(f"❌ Fehler beim Schreiben der eula.txt: {e}")

def convert_value(value: str) -> str:
    value = value.strip()
    if value.lower() in ("true", "false"):
        return value.lower()
    try:
        int(value)
        return value
    except ValueError:
        pass
    return value.replace(" ", "\\ ").replace("§", "\\u00A7")


def write_server_properties(server_dir: Path, config: ConfigParser, server_name: str, velocity_secret: str = None):
    print("➡️  Schreibe server.properties...")

    # Pfad vorbereiten
    properties_path = server_dir / "server.properties"
    
    # Alle Werte aus [PAPER] laden
    paper_config = config["PAPER"]
    lines = []

    for key, value in paper_config.items():
        if key.startswith("default_"):
            prop_key = key.replace("default_", "").lower()
            lines.append(f"{prop_key}={value.strip()}")

    # Sonderwerte ergänzen
    lines.append("enable-command-block=true")
    lines.append("online-mode=false")
    lines.append("enable-rcon=true")

    if velocity_secret:
        lines.append("velocity-support-forwarding-secret-file=../forwarding.secret")
    else:
        # Einfaches (nicht sicheres) Default-Passwort setzen, kann bei Bedarf angepasst werden
        lines.append("rcon.password=changeme")

    # Schreiben
    with properties_path.open("w") as f:
        f.write("\n".join(lines) + "\n")

    print("✅ server.properties geschrieben.")
