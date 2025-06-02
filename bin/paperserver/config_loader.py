from configparser import ConfigParser
from pathlib import Path

def load_config() -> ConfigParser:
    config_path = Path(__file__).resolve().parents[2] / "config" / "global.conf"
    parser = ConfigParser()
    parser.read(config_path)
    return parser

def load_ram_config():
    config = load_config()
    min_ram = config.get("DEFAULT", "MIN_RAM", fallback="512M")
    max_ram = config.get("DEFAULT", "MAX_RAM", fallback="2G")
    return min_ram, max_ram
