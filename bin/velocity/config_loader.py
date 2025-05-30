from configparser import ConfigParser
from pathlib import Path

def format_value(value: str) -> str:
    # Belasse true/false und Zahlen wie sie sind
    if value.lower() in ["true", "false"] or value.isdigit():
        return value
    # Verhindere doppelte Anführungszeichen
    if value.startswith('"') and value.endswith('"'):
        return value
    return f'"{value}"'

def load_config(section: str = "DEFAULT") -> dict:
    config_path = Path(__file__).resolve().parents[2] / "config" / "global.conf"
    parser = ConfigParser()
    parser.read(config_path)

    if section not in parser:
        raise ValueError(f"Sektion [{section}] nicht gefunden in {config_path}")

    raw_config = parser[section]
    formatted_config = {}

    for key, value in raw_config.items():
        clean_key = key.replace("default_", "").lower().replace("_", "-")
        formatted_value = format_value(value)
        formatted_config[clean_key] = formatted_value

    return formatted_config
