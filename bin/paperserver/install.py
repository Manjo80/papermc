 # install.py

import os
import shutil
from pathlib import Path
from paperserver.download_paper import download_latest_paper
from paperserver.config_loader import load_config
from paperserver.server_starter import start_server_until_eula, start_until_configs_generated
from paperserver.config import accept_eula, write_server_properties
from paperserver.service_creator import create_systemd_service
from paperserver.velocity_setup import copy_velocity_secret, update_spigot_yml, update_paper_global_yml, update_velocity_toml

def main():
    config = load_config()

    # Installationsverzeichnis aus global.conf
    base_dir = Path(config['DEFAULT']['BASE_DIR'])
    base_dir.mkdir(parents=True, exist_ok=True)

    # Servernamen abfragen
    name = input("➡️ Name des neuen Paper-Servers: ").strip()
    if not name:
        print("❌ Kein Name eingegeben.")
        return

    server_dir = base_dir / f"paper-{name}"
    if server_dir.exists():
        print("❌ Serververzeichnis existiert bereits.")
        return
    server_dir.mkdir()

    # Paper herunterladen
    jar_path = download_latest_paper(server_dir)
    print(f"✅ PaperMC wurde heruntergeladen: {jar_path}")

    # Server starten bis EULA erscheint
    start_server_until_eula(server_dir)

    # Accept EULA
    accept_eula(server_dir)

    # server.properties schreiben
    write_server_properties(server_dir, config)

    # Server stsrten bis spiot und paer-global erstellt sind
    start_until_configs_generated(server_dir)

    # Velocity-Einbindung abfragen
    use_velocity = input("➡️ Soll der Server in Velocity eingebunden werden? (y/n): ").lower() == 'y'
    if use_velocity:
        velocity_dir = Path("/opt/minecraft/velocity")
        copy_velocity_secret(velocity_dir, server_dir)
        update_spigot_yml(server_dir)
        update_paper_global_yml(server_dir)

       # IP und Port automatisch aus server.properties auslesen
        ip = "127.0.0.1"
        port = 25565
        props_file = server_dir / "server.properties"
        if props_file.exists():
            with open(props_file) as f:
                for line in f:
                    if line.startswith("server-port="):
                        port = int(line.split("=")[1].strip())
                    elif line.startswith("server-ip="):
                        ip = line.split("=")[1].strip()

        redirect = input("➡️ Soll Velocity bei Login direkt auf diesen Server weiterleiten? (y/n): ").lower() == 'y'
        update_velocity_toml(velocity_dir, name, ip, port, redirect)
     
    # Systemctl erstellen
    create_systemd_service(name, server_dir)

    # Konfiguration anzeigen
    print("✅ Paper-Server erfolgreich installiert.")
    print(f"➡️  Serververzeichnis: {server_dir}")
    print(f"➡️  Startbefehl: systemctl start paper@{name}")
    input("🔁 Drücke [Enter], um zurückzukehren ...")
