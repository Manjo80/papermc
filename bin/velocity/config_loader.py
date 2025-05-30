from configparser import ConfigParser
from pathlib import Path

def format_value(value: str) -> str:
    """
    Formatiert den Wert korrekt für TOML:
    - Wahrheitswerte und reine Zahlen bleiben wie sie sind
    - Alles andere wird in Anführungszeichen gesetzt
    """
    value = value.strip()

    if value.lower() in ("true", "false"):
        return value.lower()
    try:
        float(value)  # Zahl erkannt
        return value
    except ValueError:
        pass

    if value.startswith('"') and value.endswith('"'):
        value = value[1:-1]

    return f'"{value}"'

def load_config(section: str = "DEFAULT") -> dict:
    """
    Lädt nur explizite Werte aus der angegebenen Sektion (z. B. VELOCITY),
    konvertiert `default_key_name` zu `key-name`, formatiert Werte wie für TOML nötig.
    """
    config_path = Path(__file__).resolve().parents[2] / "config" / "global.conf"
    parser = ConfigParser()
    parser.read(config_path)

    if section not in parser:
        raise ValueError(f"Sektion [{section}] nicht gefunden in {config_path}")

    raw_config = parser.items(section, raw=True)

    cleaned_config = {}
    for key, value in raw_config:
        if key.startswith("default_"):
            clean_key = key.replace("default_", "").lower().replace("_", "-")
            cleaned_config[clean_key] = format_value(value)

    return cleaned_config
