# install_paper_server.py

import os
import subprocess
from pathlib import Path

from paper.downloader import download_latest_paper
from paper.log_monitor import monitor_log_for_warnings
from paper.property_writer import write_server_properties
from paper.config import update_spigot, update_paper_global, update_velocity_toml
from paper.velocity_detection import detect_velocity
from paper.input_collector import ask_server_properties
from paper.service_creator import create_systemd_service
from velocity.config_loader import load_config

def main():
    base_dir = Path("/opt/minecraft")
    base_dir.mkdir(parents=True, exist_ok=True)

    print("➡️ PaperMC Server Installer gestartet.")

    # Konfiguration laden
    defaults = load_config()

    # Eingaben vom Benutzer
    name, port, rcon_port, rcon_pass, view_distance, level_name, seed, mode, velocity_secret, velocity_toml, velocity_name = ask_server_properties(defaults)

    server_dir = base_dir / f"paper-{name}"
    if server_dir.exists():
        print(f"❌ Serververzeichnis {server_dir} existiert bereits.")
        return
    server_dir.mkdir(parents=True)

    # Paper herunterladen
    jar_path = download_latest_paper(server_dir)

    # Server einmal starten zum Erzeugen der Dateien
    print("➡️ Starte Server zum Erzeugen der EULA...")
    proc = subprocess.Popen(["java", "-jar", "paper.jar", "nogui"], cwd=server_dir)
    proc.wait(timeout=15)
    eula_path = server_dir / "eula.txt"
    if eula_path.exists():
        eula_path.write_text("eula=true\n")
        print("✅ EULA akzeptiert.")
    else:
        print("❌ EULA nicht gefunden.")
        return

    # server.properties schreiben
    write_server_properties(server_dir, defaults, port, rcon_port, rcon_pass, view_distance, level_name, seed, velocity_secret)

    # Server starten zum Erzeugen von spigot.yml und paper-global.yml
    print("➡️ Starte Server zur Erzeugung weiterer Konfigurationsdateien...")
    proc = subprocess.Popen(["java", "-jar", "paper.jar", "nogui"], cwd=server_dir)
    proc.wait(timeout=30)

    # spigot.yml anpassen
    update_spigot(server_dir)

    # paper-global.yml anpassen (nur wenn Velocity genutzt wird)
    if velocity_secret:
        update_paper_global(server_dir, velocity_secret, velocity_online_mode=True)

    # velocity.toml eintragen, wenn vorhanden
    if velocity_toml:
        update_velocity_toml(velocity_toml, name, port)

    # systemd Service anlegen
    create_systemd_service(name, server_dir)

    print(f"✅ PaperMC Server '{name}' erfolgreich installiert unter {server_dir}")
