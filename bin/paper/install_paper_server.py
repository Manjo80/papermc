# bin/paper/install_paper_server.py

import os
import subprocess
from pathlib import Path

from paper.downloader import download_latest_paper
from paper.log_monitor import wait_for_log_message
from paper.property_writer import write_server_properties
from paper.config import apply_paper_configs
from paper.velocity_detection import find_velocity_servers, get_forwarding_secret
from paper.service_creator import create_systemd_service
from paper.input_collector import collect_user_inputs
from velocity.config_loader import load_config
from velocity.toml_editor import add_server_to_velocity_config


def main():
    base_dir = Path("/opt/minecraft")
    base_dir.mkdir(parents=True, exist_ok=True)

    server_name = input("➡️  Name des Paper-Servers: ").strip()
    if not server_name:
        print("❌ Kein Servername eingegeben.")
        return

    server_dir = base_dir / server_name
    if server_dir.exists():
        print("❌ Ein Server mit diesem Namen existiert bereits.")
        return
    server_dir.mkdir()

    # Benutzer fragen, ob Velocity verlinkt werden soll
    use_velocity = input("➡️  Mit Velocity verbinden? (j/n): ").strip().lower() == 'j'
    velocity_secret = None
    velocity_toml_path = None

    if use_velocity:
        velocity_servers = find_velocity_servers(base_dir)
        if not velocity_servers:
            print("❌ Keine Velocity-Server gefunden.")
            return

        print("➡️  Verfügbare Velocity-Server:")
        for i, v_path in enumerate(velocity_servers):
            print(f"[{i}] {v_path.name}")
        try:
            choice = int(input("➡️  Nummer des Velocity-Servers: ").strip())
            selected_velocity = velocity_servers[choice]
            velocity_secret = get_forwarding_secret(selected_velocity)
            velocity_toml_path = selected_velocity / "velocity.toml"
        except (ValueError, IndexError):
            print("❌ Ungültige Auswahl.")
            return

    # Lade Konfiguration
    config = load_config("PAPER")

    # Benutzerdefinierte Eingaben sammeln (inkl. Port, RCON, seed, etc.)
    user_inputs = collect_user_inputs(config, velocity_secret is not None)
    port = user_inputs['port']

    # PaperMC herunterladen
    jar_path = download_latest_paper(server_dir)

    # Erster Start: Dateien erzeugen
    print("➡️  Starte Server zum Initialisieren...")
    proc = subprocess.Popen([
        "java",
        f"-Xmx{config.get('default_max_ram', '2G')}",
        f"-Xms{config.get('default_min_ram', '512M')}",
        "-jar", jar_path.name
    ], cwd=server_dir)
    wait_for_log_message(server_dir / "logs" / "latest.log", "You have not accepted the EULA")
    proc.terminate()

    # EULA akzeptieren
    (server_dir / "eula.txt").write_text("eula=true\n")

    # `server.properties` schreiben
    update_server_properties(server_dir, config, user_inputs, velocity_secret)

    # Zweiter Start: paper-global.yml, spigot.yml erzeugen
    print("➡️  Starte Server zur Generierung weiterer Dateien...")
    proc = subprocess.Popen([
        "java",
        f"-Xmx{config.get('default_max_ram', '2G')}",
        f"-Xms{config.get('default_min_ram', '512M')}",
        "-jar", jar_path.name
    ], cwd=server_dir)
    wait_for_log_message(server_dir / "logs" / "latest.log", "Done")
    proc.terminate()

    # Konfigurationen anpassen
    apply_paper_configs(server_dir, velocity_secret, velocity_toml_path)

    # Server in Velocity-Konfiguration eintragen
    if use_velocity and velocity_toml_path:
        add_server_to_velocity_config(velocity_toml_path, server_name, port)

    # Systemd-Service anlegen
    create_systemd_service(server_name, server_dir, config.get("default_min_ram", "512M"), config.get("default_max_ram", "2G"))

    print("✅ Paper-Server wurde erfolgreich installiert.")
    print(f"➡️  Serververzeichnis: {server_dir}")
    print(f"➡️  Startbefehl: systemctl start paper@{server_name}")
