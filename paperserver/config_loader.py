# paperserver/config_loader.py
from configparser import ConfigParser
from pathlib import Path

def load_config():
    config_path = Path(__file__).resolve().parent.parent / "config" / "global.conf"
    config = ConfigParser()
    config.read(config_path)
    return config['DEFAULT']
