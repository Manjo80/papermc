# install_velocity_server.py

from pathlib import Path
from velocity.config_loader import load_config
from velocity.downloader import download_latest_velocity
from velocity.initializer import start_velocity_once
from velocity.configurator import apply_velocity_toml
from velocity.service_creator import create_systemd_service
from velocity.secret_handler import copy_forwarding_secret

BASE_DIR = Path("/opt/minecraft")

def main():
    config = load_config()

    name = input("Velocity-Servername: ").strip().lower()
    port = input(f"Port [{config['DEFAULT_VELOCITY_PORT']}]: ") or config['DEFAULT_VELOCITY_PORT']
    server_dir = BASE_DIR / f"velocity-{name}"
    server_dir.mkdir(parents=True, exist_ok=True)

    # Installation
    download_latest_velocity(server_dir)
    start_velocity_once(server_dir)
    apply_velocity_toml(server_dir)
    copy_forwarding_secret(server_dir)
    create_systemd_service(name, server_dir, config['DEFAULT_MIN_RAM'], config['DEFAULT_MAX_RAM'])

    print("✅ Velocity Server erfolgreich installiert.")

if __name__ == "__main__":
    main()
