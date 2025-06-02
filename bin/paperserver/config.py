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
    paper_config = dict(config.items("PAPER", raw=True))  # Nur [PAPER]

    path = server_dir / "server.properties"
    props = {}

    # Bestehende Datei einlesen
    if path.exists():
        with path.open("r") as f:
            for line in f:
                if "=" in line:
                    k, v = line.strip().split("=", 1)
                    props[k.strip()] = v.strip()

    # Neue Werte anwenden (ersetzen oder ergänzen)
    for key, value in paper_config.items():
        if key.startswith("default_"):
            clean_key = key.replace("default_", "").replace("_", "-").lower()
            props[clean_key] = value.strip()

    # Alles zurückschreiben
    with path.open("w") as f:
        for k in sorted(props.keys()):
            f.write(f"{k}={props[k]}\n")

    print("✅ server.properties wurde aktualisiert.")
