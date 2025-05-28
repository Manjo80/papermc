import os
import subprocess
import time
from pathlib import Path
import requests

BASE_DIR = Path("/opt/minecraft")
CONFIG_DIR = Path("/opt/papermc/config")
VELOCITY_PORT_DEFAULT = 25577


def get_valid_port(prompt, default):
    while True:
        port_input = input(f"{prompt} [{default}]: ") or str(default)
        if port_input.isdigit() and 1024 < int(port_input) < 65535:
            return port_input
        print("❌ Ungültiger Port. Bitte gib eine Zahl zwischen 1025 und 65534 ein.")


def download_velocity(target_dir):
    print("➡️  Lade neueste Velocity-Version herunter...")
    versions = requests.get("https://api.papermc.io/v2/projects/velocity").json()
    latest_version = versions["versions"][-1]
    builds = requests.get(f"https://api.papermc.io/v2/projects/velocity/versions/{latest_version}").json()
    latest_build = builds["builds"][-1]
    jar_name = f"velocity-{latest_version}-{latest_build}.jar"
    jar_url = f"https://api.papermc.io/v2/projects/velocity/versions/{latest_version}/builds/{latest_build}/downloads/{jar_name}"
    jar_path = target_dir / "velocity.jar"
    r = requests.get(jar_url)
    with open(jar_path, 'wb') as f:
        f.write(r.content)
    return latest_version, jar_path


def generate_velocity_config(target_dir, port):
    print("➡️  Erzeuge velocity.toml...")
    velocity_toml = target_dir / "velocity.toml"
    content = f"""
config-version = 2
bind = ":{port}"
motd = "A Velocity Server"
show-max-players = 500
announce-forge = false
forwarding-secret-file = "forwarding.secret"
servers = {{}}
forced-hosts = {{}}
"""
    with open(velocity_toml, "w") as f:
        f.write(content.strip())


def copy_forwarding_secret(server_dir):
    print("➡️  Kopiere forwarding.secret nach /opt/minecraft...")
    src = server_dir / "forwarding.secret"
    dest = BASE_DIR / "forwarding.secret"
    if src.exists():
        subprocess.run(["cp", str(src), str(dest)])
    else:
        print("⚠️  forwarding.secret wurde nicht gefunden. Wird wahrscheinlich erst nach dem ersten Start erstellt.")


def create_systemd_service(name, server_dir):
    print("➡️  Erstelle systemd Service...")
    service_file = f"/etc/systemd/system/velocity-{name}.service"
    content = f"""
[Unit]
Description=Velocity Server: {name}
After=network.target

[Service]
WorkingDirectory={server_dir}
ExecStart=/usr/bin/java -Xmx512M -Xms512M -jar velocity.jar
Restart=always
User=root

[Install]
WantedBy=multi-user.target
"""
    with open(service_file, "w") as f:
        f.write(content)
    subprocess.run(["systemctl", "daemon-reload"])
    subprocess.run(["systemctl", "enable", f"velocity-{name}"])
    subprocess.run(["systemctl", "start", f"velocity-{name}"])


def main():
    name = input("Velocity-Servername: ").strip().lower()
    port = get_valid_port("Port für Velocity", VELOCITY_PORT_DEFAULT)
    server_dir = BASE_DIR / f"velocity-{name}"
    server_dir.mkdir(parents=True, exist_ok=True)

    version, jar_path = download_velocity(server_dir)

    generate_velocity_config(server_dir, port)
    create_systemd_service(name, server_dir)

    print("➡️  Starte Server für Initialisierung...")
    subprocess.run(["systemctl", "restart", f"velocity-{name}"])
    time.sleep(10)

    copy_forwarding_secret(server_dir)

    print("✅ Velocity-Server '{name}' installiert und gestartet.")
    print("➡️  Ergänze velocity.toml manuell mit deinen Servereinträgen.")


if __name__ == "__main__":
    main()
