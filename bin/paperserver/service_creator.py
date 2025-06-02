import subprocess
from pathlib import Path
from bin.paperserver.download_paper import download_latest_paper
from paperserver.config_loader import load_ram_config
from configparser import ConfigParser

def create_systemd_service(server_name: str, server_dir: Path):
    print("➡️ Erstelle systemd-Service für Paper-Server...")

    from paperserver.config_loader import load_ram_config
    min_ram, max_ram = load_ram_config()

    service_name = f"paper-{server_name}.service"
    service_path = Path("/etc/systemd/system") / service_name
    start_script_path = server_dir / "autostart.sh"
    update_script_path = "/opt/papermc/bin/paperserver/update_check.py"

    # Autostart-Shell-Skript
    autostart_script = f"""#!/bin/bash
cd "{server_dir}" || exit 1
/usr/bin/python3 "{update_script_path}"
exec java -Xms{min_ram} -Xmx{max_ram} -jar paper.jar nogui
"""

    # Schreibe Autostart-Skript
    with start_script_path.open("w") as f:
        f.write(autostart_script)
    start_script_path.chmod(0o755)

    # systemd-Service-Datei
    service_content = f"""[Unit]
Description=PaperMC Server: {server_name}
After=network.target

[Service]
Type=simple
WorkingDirectory={server_dir}
ExecStart={start_script_path}
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
