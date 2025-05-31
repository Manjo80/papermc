# service_creator.py

import subprocess
from pathlib import Path

def create_systemd_service(server_name: str, server_dir: Path):
    print("➡️ Erstelle systemd-Service für Paper-Server...")

    service_name = f"paper-{server_name}.service"
    service_path = Path("/etc/systemd/system") / service_name
    updater_script_path = server_dir / "start_with_update.sh"

    # Bash-Skript zum Updaten und Starten des Servers
    updater_script_content = f"""#!/bin/bash
cd "{server_dir}"

echo "🔍 Prüfe auf Updates..."
LATEST=$(curl -s https://api.papermc.io/v2/projects/paper | jq -r '.versions[-1]')
BUILD=$(curl -s https://api.papermc.io/v2/projects/paper/versions/$LATEST | jq -r '.builds[-1]')
JAR_NAME="paper-$LATEST-$BUILD.jar"

if [ ! -f "$JAR_NAME" ]; then
    echo "⬇️  Lade $JAR_NAME herunter..."
    curl -o "$JAR_NAME" -L "https://api.papermc.io/v2/projects/paper/versions/$LATEST/builds/$BUILD/downloads/$JAR_NAME"
    ln -sf "$JAR_NAME" paper.jar
else
    echo "✅ Bereits aktuell: $JAR_NAME"
    ln -sf "$JAR_NAME" paper.jar
fi

echo "🚀 Starte Paper-Server..."
exec java -Xms512M -Xmx512M -jar paper.jar nogui
"""

    with updater_script_path.open("w") as f:
        f.write(updater_script_content)
    updater_script_path.chmod(0o755)

    # systemd-Service-Datei
    service_content = f"""[Unit]
Description=PaperMC Server: {server_name}
After=network.target

[Service]
Type=simple
WorkingDirectory={server_dir}
ExecStart={updater_script_path}
Restart=on-failure
User=root

[Install]
WantedBy=multi-user.target
"""

    with open(service_path, "w") as f:
        f.write(service_content)

    # Systemd neu laden und Dienst aktivieren
    subprocess.run(["systemctl", "daemon-reload"])
    subprocess.run(["systemctl", "enable", service_name])
    subprocess.run(["systemctl", "start", service_name])

    print(f"✅ Systemd-Service {service_name} wurde erstellt und gestartet.")
