# paper/service_creator.py

import subprocess

def create_systemd_service(name, server_dir):
    print("➡️  Erstelle systemd Service...")

    service_file = f"/etc/systemd/system/paper-{name}.service"
    content = f"""[Unit]
Description=PaperMC Server: {name}
After=network.target

[Service]
WorkingDirectory={server_dir}
ExecStart=/usr/bin/java -Xms512M -Xmx512M -jar paper.jar nogui
Restart=always
User=root

[Install]
WantedBy=multi-user.target
"""

    with open(service_file, "w") as f:
        f.write(content)

    subprocess.run(["systemctl", "daemon-reload"])
    subprocess.run(["systemctl", "enable", f"paper-{name}"])
    subprocess.run(["systemctl", "start", f"paper-{name}"])
