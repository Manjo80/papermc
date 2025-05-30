# bin/velocity/install_velocity_server.py

from pathlib import Path
from velocity.downloader import download_latest_velocity
from velocity.initializer import start_velocity_once
from velocity.secret_handler import copy_forwarding_secret
from velocity.configurator import apply_velocity_toml
from velocity.config_loader import load_config
from velocity.service_creator import create_systemd_service
import os

def main():
    base_dir = Path("/opt/papermc/servers")
    base_dir.mkdir(parents=True, exist_ok=True)

    server_name = input("➡️  Name des Velocity-Proxys: ").strip()
    if not server_name:
        print("❌ Kein Servername eingegeben.")
        return

    server_dir = base_dir / server_name
    if server_dir.exists():
        print("❌ Ein Server mit diesem Namen existiert bereits.")
        return

    server_dir.mkdir()

    # Velocity herunterladen
    jar_path = download_latest_velocity(server_dir)

    # Server starten, damit Konfiguration erzeugt wird
    start_velocity_once(server_dir)

    # Secret erstellen
    secret_path = copy_forwarding_secret(server_dir)

    # Konfiguration vorbereiten
    apply_velocity_toml(server_dir, secret_path.read_text().strip(), server_name)

    # Systemd-Service einrichten
    create_systemd_service(server_name, server_dir)

    # Konfiguration anzeigen
    print("✅ Velocity-Proxy erfolgreich installiert.")
    print(f"➡️  Serververzeichnis: {server_dir}")
    print(f"➡️  Startbefehl: systemctl start velocity@{server_name}")
