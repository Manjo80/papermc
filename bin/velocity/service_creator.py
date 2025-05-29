# velocity/service_creator.py

import subprocess
from pathlib import Path

def create_systemd_service(name: str, server_dir: Path, min_ram: str, max_ram: str):
    """
    Erstellt eine systemd-Service-Datei für den Velocity-Server.
    """
    print("➡️  Erstelle systemd Service...")

    service_file_path = Path(f"/etc/systemd/system/velocity-{name}.service")
    service_content = f"""[Unit]
Description=Velocity Server: {name}
After=network.target

[Service]
WorkingDirectory={server_dir}
ExecStart=/usr/bin/java -Xms{min_ram} -Xmx{max_ram} -jar velocity.jar
Restart=always
User=root

[Install]
WantedBy=multi-user.target
"""

    with open(service_file_path, "w") as f:
        f.write(service_content)

    subprocess.run(["systemctl", "daemon-reload"], check=True)
    subprocess.run(["systemctl", "enable", f"velocity-{name}"], check=True)
    subprocess.run(["systemctl", "start", f"velocity-{name}"], check=True)
