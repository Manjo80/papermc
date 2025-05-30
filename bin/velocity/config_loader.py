from configparser import ConfigParser
from pathlib import Path

def normalize_key(key: str) -> str:
    key = key.lower()
    if key.startswith("default_"):
        key = key.replace("default_", "")
    return key.replace("_", "-")

def load_config(section: str = "DEFAULT") -> dict:
    config_path = Path(__file__).resolve().parents[2] / "config" / "global.conf"
    parser = ConfigParser()
    parser.read(config_path)

    if section not in parser:
        raise ValueError(f"Sektion [{section}] nicht gefunden in {config_path}")

    return {
        normalize_key(k): v
        for k, v in parser[section].items()
    }
