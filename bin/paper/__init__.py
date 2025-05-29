# paper/__init__.py

from .config_loader import load_config
from .downloader import download_latest_paper
from .initializer import start_server_once, apply_eula
from .velocity_detection import detect_velocity
from .input_collector import ask_server_properties
from .property_writer import write_server_properties
from .config import update_spigot, update_paper_global, update_velocity_toml
from .service_creator import create_systemd_service
from .log_monitor import monitor_log_for_warnings
