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

def write_server_properties(server_dir: Path, config: ConfigParser):
    print("➡️  Schreibe server.properties...")

    if "PAPER" not in config:
        print("❌ Sektion [PAPER] nicht gefunden.")
        return

    paper_config = config._sections["PAPER"]  # Nur explizit definierte Werte
    properties = {}

    for key, value in paper_config.items():
        if key.startswith("default_"):
            prop_key = key.replace("default_", "").lower()
            properties[prop_key] = value.strip()

    # Bestehende Datei lesen, um alte Einträge zu ersetzen
    properties_path = server_dir / "server.properties"
    if properties_path.exists():
        with properties_path.open("r") as f:
            for line in f:
                if "=" in line:
                    k, v = line.strip().split("=", 1)
                    if k not in properties:
                        properties[k] = v.strip()

    # Alles neu schreiben
    with properties_path.open("w") as f:
        for k, v in properties.items():
            f.write(f"{k}={v}\n")

    print("✅ server.properties geschrieben.")
