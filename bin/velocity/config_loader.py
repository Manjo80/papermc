from configparser import ConfigParser
from pathlib import Path

def load_config(section: str = "DEFAULT") -> dict:
    config_path = Path(__file__).resolve().parents[2] / "config" / "global.conf"
    parser = ConfigParser()
    parser.read(config_path)

    if section in parser:
        return dict(parser[section])
    else:
        raise ValueError(f"Sektion [{section}] nicht gefunden in {config_path}")
