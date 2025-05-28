import os
import subprocess
import time
import shutil
import json
from pathlib import Path

BASE_DIR = Path("/opt/minecraft")
VELOCITY_DIR = Path("/opt/velocity-temp")

VELOCITY_JAR_URL = "https://api.papermc.io/v2/projects/velocity/versions"

def ask_velocity_settings():
    name = input("Servername: ").strip().lower()
    port = input("Port [25577]: ") or "25577"
    if not port.isdigit() or not (1024 <= int(port) <= 65535):
        print("❌ Ungültiger Port. Verwende 25577.")
        port = "25577"
    return name, port

def download_velocity(target_dir):
    print("➡️  Lade Velocity 3.4.0-SNAPSHOT Build 509 herunter...")
    jar_name = "velocity-3.4.0-SNAPSHOT-509.jar"
    jar_url = f"https://api.papermc.io/v2/projects/velocity/versions/3.4.0-SNAPSHOT/builds/509/downloads/{jar_name}"
    jar_path = target_dir / "velocity.jar"
    r = requests.get(jar_url)
    if r.status_code != 200:
        print(f"❌ Fehler beim Herunterladen: Status {r.status_code}")
        return None
    with open(jar_path, 'wb') as f:
        f.write(r.content)
    return jar_path
    
def start_velocity_once(server_dir):
    print("➡️  Starte Velocity Server zur Initialisierung...")
    process = subprocess.Popen(["java", "-jar", "velocity.jar"], cwd=server_dir,
                               stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in process.stdout:
        decoded = line.decode(errors="ignore").strip()
        print(decoded)
        if "Done" in decoded or "Shutting down" in decoded:
            break
    time.sleep(5)
    process.terminate()
    process.wait()

def prepare_velocity_config(server_dir, name, port):
    print("➡️  Passe velocity.toml an...")
    toml_path = server_dir / "velocity.toml"
    if not toml_path.exists():
        print("❌ velocity.toml nicht gefunden. Stelle sicher, dass der Server korrekt gestartet wurde.")
        return

    with open(toml_path, "r") as f:
        lines = f.readlines()

    new_lines = []
    inside_servers = False
    inside_forced = False
    for line in lines:
        if line.strip().startswith("[servers]"):
            new_lines.append("[servers]\n")
            new_lines.append("# Platzhalter - konfiguriere manuell\n")
            inside_servers = True
            continue
        if line.strip().startswith("[forced-hosts]"):
            new_lines.append("[forced-hosts]\n")
            new_lines.append("# Platzhalter - konfiguriere manuell\n")
            inside_forced = True
            continue
        if line.strip().startswith("["):
            inside_servers = False
            inside_forced = False
        if not inside_servers and not inside_forced:
            new_lines.append(line)

    with open(toml_path, "w") as f:
        f.writelines(new_lines)

    print("➡️  Kopiere forwarding.secret nach /opt/minecraft...")
    forwarding_secret = server_dir / "forwarding.secret"
    if forwarding_secret.exists():
        shutil.copy(forwarding_secret, BASE_DIR / f"forwarding_{name}.secret")

def create_systemd_service(name, server_dir, port):
    print("➡️  Erstelle systemd Service...")
    service_file = f"/etc/systemd/system/velocity-{name}.service"
    content = f"""
[Unit]
Description=Velocity Server: {name}
After=network.target

[Service]
WorkingDirectory={server_dir}
ExecStart=/usr/bin/java -jar velocity.jar
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

def monitor_log(server_dir):
    print("➡️  Überwache Logs auf Fehler oder Warnungen...")
    log_path = server_dir / "logs" / "latest.log"
    if not log_path.exists():
        print("❌ Logdatei nicht gefunden.")
        return
    with open(log_path, "r") as f:
        for line in f:
            if any(w in line for w in ["[ERROR]", "[WARN]"]):
                print(line.strip())

def main():
    name, port = ask_velocity_settings()
    server_dir = BASE_DIR / f"velocity-{name}"
    server_dir.mkdir(parents=True, exist_ok=True)

    download_velocity(server_dir)
    start_velocity_once(server_dir)
    prepare_velocity_config(server_dir, name, port)
    start_velocity_once(server_dir)
    create_systemd_service(name, server_dir, port)
    time.sleep(30)
    monitor_log(server_dir)

if __name__ == "__main__":
    main()
