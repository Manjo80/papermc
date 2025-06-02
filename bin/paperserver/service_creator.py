import subprocess
from pathlib import Path

def create_systemd_service(server_name: str, server_dir: Path):
    print("➡️ Erstelle systemd-Service für Paper-Server (ohne Update)...")

    service_name = f"paper-{server_name}.service"
    service_path = Path("/etc/systemd/system") / service_name
    updater_path = server_dir / "autostart.py"

    # Autostart-Python-Skript (ohne Update)
    autostart_script = f"""#!/usr/bin/env python3
import os
import subprocess
from pathlib import Path

server_dir = Path("{server_dir}")
os.chdir(server_dir)

print("🚀 Starte Paper-Server...")
subprocess.run(["java", "-Xms512M", "-Xmx2G", "-jar", "paper.jar", "nogui"])
"""

    # Schreibe das Autostart-Skript
    with updater_path.open("w") as f:
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

    with service_path.open("w") as f:
        f.write(service_content)

    subprocess.run(["systemctl", "daemon-reload"], check=True)
    subprocess.run(["systemctl", "enable", service_name], check=True)
    subprocess.run(["systemctl", "start", service_name], check=True)

    print(f"✅ systemd-Service {service_name} wurde eingerichtet und gestartet.")
