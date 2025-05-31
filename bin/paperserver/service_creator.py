import subprocess
from pathlib import Path
from bin.paperserver.download import download_latest_paper
from configparser import ConfigParser

def load_ram_config():
    config_path = Path(__file__).resolve().parents[1] / "config" / "global.conf"
    config = ConfigParser()
    config.read(config_path)
    default = config["DEFAULT"]
    return default.get("DEFAULT_MIN_RAM", "512M"), default.get("DEFAULT_MAX_RAM", "2G")

def create_systemd_service(server_name: str, server_dir: Path):
    print("➡️ Erstelle systemd-Service für Paper-Server...")

    min_ram, max_ram = load_ram_config()
    service_name = f"paper-{server_name}.service"
    service_path = Path("/etc/systemd/system") / service_name
    updater_path = server_dir / "autostart.py"

    # Autostart-Python-Skript (lädt Updates, startet Server)
    autostart_script = f"""#!/usr/bin/env python3
import os
from pathlib import Path
from paperserver.download import download_latest_paper
import subprocess

server_dir = Path("{server_dir}")
os.chdir(server_dir)

print("🔍 Suche nach Paper-Update...")
download_latest_paper(server_dir)

print("🚀 Starte Paper-Server...")
subprocess.run(["java", "-Xms{min_ram}", "-Xmx{max_ram}", "-jar", "paper.jar", "nogui"])
"""
    with open(updater_path, "w") as f:
        f.write(autostart_script)
    updater_path.chmod(0o755)

    # systemd-Service-Datei
    service_content = f"""[Unit]
Description=PaperMC Server: {server_name}
After=network.target

[Service]
Type=simple
WorkingDirectory={server_dir}
ExecStart=/usr/bin/python3 {updater_path}
Restart=on-failure
User=root

[Install]
WantedBy=multi-user.target
"""

    with open(service_path, "w") as f:
        f.write(service_content)

    subprocess.run(["systemctl", "daemon-reload"], check=True)
    subprocess.run(["systemctl", "enable", service_name], check=True)
    subprocess.run(["systemctl", "start", service_name], check=True)

    print(f"✅ systemd-Service {service_name} wurde eingerichtet und gestartet.")
