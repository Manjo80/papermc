# config.py

from pathlib import Path

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


def write_server_properties(server_dir: Path, config: dict):
    props_path = server_dir / "server.properties"
    with props_path.open("w") as f:
        f.write("# Automatisch generiert\n")
        for key, value in config.items():
            if key.startswith("DEFAULT_"):
                prop_key = key.replace("DEFAULT_", "").lower().replace("_", "-")
                f.write(f"{prop_key}={convert_value(value)}\n")
        # Ergänzung: wichtige zusätzliche Optionen
        f.write("enable-command-block=true\n")
        f.write("online-mode=false\n")
        f.write("enable-rcon=true\n")
