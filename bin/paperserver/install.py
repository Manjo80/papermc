 # install.py

import os
from pathlib import Path
from downloader import download_latest_paper
from config_loader import load_config
from server_starter import start_server_until_eula, start_until_configs_generated
from config import accept_eula, write_server_properties
from paperserver.service_creator import create_systemd_service

# Konfiguration laden
config = load_config()

# Installationsverzeichnis aus global.conf
base_dir = Path(config['BASE_DIR'])
base_dir.mkdir(parents=True, exist_ok=True)

# Servernamen abfragen
name = input("➡️ Name des neuen Paper-Servers: ").strip()
if not name:
    print("❌ Kein Name eingegeben.")
    exit(1)

server_dir = base_dir / f"paper-{name}"
if server_dir.exists():
    print("❌ Serververzeichnis existiert bereits.")
    exit(1)
server_dir.mkdir()

# Paper herunterladen
jar_path = download_latest_paper(server_dir)
print(f"✅ PaperMC wurde heruntergeladen: {jar_path}")

# Server starten bis EULA erscheint
start_server_until_eula(server_dir)

# Accept EULA
accept_eula(server_dir)

# server.properties schreiben
write_server_properties(server_path, config)

# Systemctl erstellen mit autoupdater
create_systemd_service(server_name, server_dir)
