from configparser import ConfigParser
from pathlib import Path

def format_value(value: str) -> str:
    """
    Formatiert Werte so, dass Strings in doppelte Anführungszeichen gesetzt werden,
    aber booleans und Zahlen unverändert bleiben.
    """
    if value.lower() in ["true", "false"]:
        return value.lower()
    if value.replace('.', '', 1).isdigit():
        return value
    if value.startswith('"') and value.endswith('"'):
        value = value[1:-1]
    return f'"{value}"'

def load_config(section: str = "DEFAULT") -> dict:
    config_path = Path(__file__).resolve().parents[2] / "config" / "global.conf"
    parser = ConfigParser()
    parser.read(config_path)

    if section in parser:
        raw_config = dict(parser[section])
        cleaned_config = {}

        for key, value in raw_config.items():
            if not key.startswith("default_"):
                continue
            clean_key = key.replace("default_", "").lower().replace("_", "-")
            cleaned_config[clean_key] = format_value(value)

        return cleaned_config
    else:
        raise ValueError(f"Sektion [{section}] nicht gefunden in {config_path}")
