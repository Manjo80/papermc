# paper/config_loader.py

from configparser import ConfigParser
from pathlib import Path

CONFIG_PATH = Path(__file__).resolve().parents[2] / "config" / "global.conf"


def format_value(value: str) -> str:
    """
    Gibt den Wert zurück, geeignet für TOML/YAML:
    - true/false → bleibt wie ist
    - reine Zahlen → bleibt wie ist
    - sonst → in Anführungszeichen
    """
    value = value.strip()

    if value.lower() in ("true", "false"):
        return value.lower()

    try:
        float(value)
        return value
    except ValueError:
        pass

    if value.startswith('"') and value.endswith('"'):
        value = value[1:-1]

    return f'"{value}"'


def load_config(section: str = "DEFAULT") -> dict:
    """
    Lädt nur Werte aus der gewünschten Sektion (z. B. PAPER) und wandelt
    diese in ein für Konfigurationsdateien geeignetes Format um.
    """
    parser = ConfigParser()
    parser.read(CONFIG_PATH)

    if section not in parser:
        raise ValueError(f"Sektion [{section}] nicht gefunden in {CONFIG_PATH}")

    raw_items = parser.items(section, raw=True)

    result = {}
    for key, value in raw_items:
        if key.startswith("default_"):
            clean_key = key.replace("default_", "").lower().replace("_", "-")
            result[clean_key] = format_value(value)

    return result
