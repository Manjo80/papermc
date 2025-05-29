from configparser import ConfigParser
from pathlib import Path

CONFIG_PATH = Path(__file__).resolve().parent.parent / "config" / "global.conf"

def load_config():
    config = ConfigParser()
    config.read(CONFIG_PATH)
    return config['DEFAULT']
