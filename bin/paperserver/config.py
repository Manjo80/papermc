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
    print("➡️  Aktualisiere server.properties...")

    paper_config = config["PAPER"]
    properties_path = server_dir / "server.properties"
    existing = {}

    # Vorhandene Datei einlesen
    if properties_path.exists():
        with properties_path.open("r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    existing[k.strip().lower()] = v.strip()

    # Neue Werte aus der Config einfügen oder überschreiben
    for key, value in paper_config.items():
        if key.startswith("default_"):
            prop_key = key.replace("default_", "").lower()
            existing[prop_key] = value.strip()

    # Zurückschreiben
    with properties_path.open("w") as f:
        for k, v in sorted(existing.items()):
            f.write(f"{k}={v}\n")

    print("✅ server.properties aktualisiert.")
