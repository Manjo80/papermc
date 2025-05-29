# velocity/config_loader.py

from pathlib import Path
from configparser import ConfigParser

CONFIG_PATH = Path(__file__).resolve().parent.parent.parent / "config" / "global.conf"

def load_config():
    config = ConfigParser()
    config.read(CONFIG_PATH)
    return config['DEFAULT']
