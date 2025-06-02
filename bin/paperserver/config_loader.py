# paperserver/config_loader.py
from configparser import ConfigParser
from pathlib import Path

def load_config():
    config_path = Path(__file__).resolve().parents[2] / "config" / "global.conf"
    parser = ConfigParser()
    parser.read(config_path)
    return parser
