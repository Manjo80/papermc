from configparser import ConfigParser
from pathlib import Path

def load_config(section: str = "DEFAULT") -> dict:
    config_path = Path(__file__).resolve().parents[2] / "config" / "global.conf"
    parser = ConfigParser()
    parser.read(config_path)

    if section not in parser:
        raise ValueError(f"Sektion [{section}] nicht gefunden in {config_path}")

    result = {}
    for key, value in parser[section].items():
        # Konvertiere true/false in bool
        if value.lower() == "true":
            result[key] = True
        elif value.lower() == "false":
            result[key] = False
        # Konvertiere ints (wenn möglich)
        elif value.isdigit():
            result[key] = int(value)
        # Versuche Floats
        else:
            try:
                result[key] = float(value)
            except ValueError:
                result[key] = value  # als String behalten

    return result
