from pathlib import Path
import subprocess

def create_systemd_service(server_name: str, server_dir: Path):
    print("➞️ Erstelle systemd-Service für Paper-Server...")

    from paperserver.config_loader import load_ram_config
    min_ram, max_ram = load_ram_config()

    service_name = f"paper-{server_name}.service"
    service_path = Path("/etc/systemd/system") / service_name
    updater_path = server_dir / "autostart.py"
    update_check_path = Path("/opt/papermc/bin/paperserver/update_check.py")

    # Autostart-Python-Skript
    autostart_script = f"""#!/usr/bin/env python3
import os
import sys
from pathlib import Path

sys.path.append("/opt/papermc/bin")  # Wichtig für Import

from paperserver.download_paper import download_latest_paper
import subprocess

server_dir = Path("{server_dir}")
os.chdir(server_dir)

print("🔍 Suche nach Paper-Update...")
download_latest_paper(server_dir)

print("🚀 Starte Paper-Server...")
subprocess.run(["java", "-Xms{min_ram}", "-Xmx{max_ram}", "-jar", "paper.jar", "nogui"])
"""

    # Schreibe Autostart-Skript
    with updater_path.open("w") as f:
        f.write(autostart_script)
    updater_path.chmod(0o755)

    # update_check.py erzeugen (falls noch nicht vorhanden oder immer neu schreiben)
    with update_check_path.open("w") as f:
        f.write("""#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.append("/opt/papermc/bin")
from paperserver.download_paper import download_latest_paper

server_dir = Path.cwd()
print("🔍 Prüfe auf neues PaperMC-Update...")
try:
    download_latest_paper(server_dir)
    print("✅ PaperMC-Update abgeschlossen.")
except Exception as e:
    print(f"❌ Fehler beim Update: {e}")
""")
    update_check_path.chmod(0o755)

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

    with service_path.open("w") as f:
        f.write(service_content)

    subprocess.run(["systemctl", "daemon-reload"], check=True)
    subprocess.run(["systemctl", "enable", service_name], check=True)
    subprocess.run(["systemctl", "start", service_name], check=True)

    print(f"✅ systemd-Service {service_name} wurde eingerichtet und gestartet.")
