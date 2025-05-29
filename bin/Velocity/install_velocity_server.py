from velocity.config_loader import load_config
from velocity.downloader import download_velocity_jar
from velocity.initializer import initialize_velocity_config
from velocity.configurator import configure_velocity_toml
from velocity.service_creator import create_velocity_service
from velocity.secret_handler import create_forwarding_secret

from pathlib import Path

BASE_DIR = Path("/opt/minecraft")

def main():
    defaults = load_config()

    name = input("➡️  Name des Velocity-Servers: ").strip().lower()
    velocity_dir = BASE_DIR / f"velocity-{name}"
    velocity_dir.mkdir(parents=True, exist_ok=True)

    # Download + Initialisierung
    download_velocity_jar(velocity_dir)
    initialize_velocity_config(velocity_dir)

    # Konfiguration des TOML
    configure_velocity_toml(velocity_dir, name, defaults)

    # Secret erzeugen
    create_forwarding_secret(BASE_DIR)

    # Systemd-Service erstellen
    create_velocity_service(name, velocity_dir)

    print("✅ Velocity-Server erfolgreich eingerichtet.")

if __name__ == "__main__":
    main()
