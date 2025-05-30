# velocity/config_loader.py

from configparser import ConfigParser
from pathlib import Path

def load_config(section: str = "DEFAULT") -> dict:
    config_path = Path(__file__).resolve().parents[2] / "config" / "global.conf"
    parser = ConfigParser()
    parser.optionxform = str  # Groß-/Kleinschreibung beibehalten
    parser.read(config_path)

    if section not in parser:
        raise ValueError(f"Sektion [{section}] nicht gefunden in {config_path}")

    result = {}
    for key, value in parser[section].items():
        clean_key = key.replace("DEFAULT_", "").lower().replace("_", "-")
        value = value.strip()

        # Falls bereits gequotet: Quote entfernen, damit es nicht doppelt wird
        if value.startswith('"') and value.endswith('"'):
            value = value[1:-1]

        # Werte quoten, außer bei bools und reinen Zahlen (ohne Sonderzeichen)
        if not value.lower() in ["true", "false"] and not value.replace('.', '', 1).isdigit():
            value = f'"{value}"'

        result[clean_key] = value

    return result
