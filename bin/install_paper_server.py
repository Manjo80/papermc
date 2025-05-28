import os
import subprocess
import time
import requests
import json
from pathlib import Path
from configparser import ConfigParser

BASE_DIR = Path("/opt/minecraft")
CONFIG_PATH = Path(__file__).resolve().parent.parent / "config" / "global.conf"


def load_config():
    config = ConfigParser()
    config.read(CONFIG_PATH)
    return config['DEFAULT']


def download_latest_paper(target_dir):
    print("➡️  Lade neueste PaperMC-Version herunter...")
    versions = requests.get("https://api.papermc.io/v2/projects/paper").json()
    latest_version = versions["versions"][-1]
    builds = requests.get(f"https://api.papermc.io/v2/projects/paper/versions/{latest_version}").json()
    latest_build = builds["builds"][-1]
    jar_name = f"paper-{latest_version}-{latest_build}.jar"
    jar_url = f"https://api.papermc.io/v2/projects/paper/versions/{latest_version}/builds/{latest_build}/downloads/{jar_name}"
    jar_path = target_dir / "paper.jar"
    r = requests.get(jar_url)
    with open(jar_path, 'wb') as f:
        f.write(r.content)
    return jar_path


def start_server_once(server_dir):
    print("➡️  Starte Server zum Erzeugen der Dateien...")
    process = subprocess.Popen(["java", "-Xmx512M", "-Xms512M", "-jar", "paper.jar", "nogui"], cwd=server_dir, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    eula_seen = False
    for line in process.stdout:
        decoded = line.decode(errors="ignore").strip()
        print(decoded)
        if "eula" in decoded.lower():
            eula_seen = True
            break
    if eula_seen:
        time.sleep(5)
        process.terminate()
        process.wait()
    else:
        process.terminate()
        process.wait()
        raise RuntimeError("EULA-Meldung wurde nicht erkannt")


def apply_eula(server_dir):
    print("➡️  Akzeptiere EULA...")
    with open(server_dir / "eula.txt", "w") as f:
        f.write("eula=true\n")


def ask_server_properties(defaults):
    name = input("Servername: ").strip().lower()
    port = input(f"Port [{defaults['DEFAULT_PAPER_PORT']}]: ") or defaults['DEFAULT_PAPER_PORT']
    rcon_port = input(f"RCON Port [{defaults['DEFAULT_RCON_PORT']}]: ") or defaults['DEFAULT_RCON_PORT']
    rcon_pass = input("RCON Passwort: ")
    view_distance = input(f"View Distance [{defaults['DEFAULT_VIEW_DISTANCE']}]: ") or defaults['DEFAULT_VIEW_DISTANCE']
    level_name = input("Level Name [world]: ") or "world"
    seed = input("Seed (leer für zufällig): ")
    mode = input("Standalone oder Velocity? (s/v): ").strip().lower()
    proxy_secret = ""
    if mode == "v":
        proxy_secret = input("Velocity Forwarding Secret: ")
    return name, port, rcon_port, rcon_pass, view_distance, level_name, seed, mode, proxy_secret


def write_server_properties(server_dir, defaults, port, rcon_port, rcon_pass, view_distance, level_name, seed):
    print("➡️  Schreibe server.properties...")
    props = f"""
server-port={port}
motd={defaults['DEFAULT_MOTD']}
gamemode={defaults['DEFAULT_GAMEMODE']}
level-type={defaults['DEFAULT_LEVEL_TYPE']}
level-name={level_name}
level-seed={seed}
spawn-npcs={defaults['DEFAULT_NPCS']}
spawn-animals={defaults['DEFAULT_ANIMALS']}
spawn-monsters={defaults['DEFAULT_MONSTERS']}
pvp={defaults['DEFAULT_PVP']}
difficulty={defaults['DEFAULT_DIFFICULTY']}
allow-nether={defaults['DEFAULT_ALLOW_NETHER']}
allow-flight={defaults['DEFAULT_ALLOW_FLIGHT']}
view-distance={view_distance}
spawn-protection={defaults['DEFAULT_SPAWN_PROTECTION']}
enable-command-block=true
online-mode=false
enable-rcon=true
rcon.port={rcon_port}
rcon.password={rcon_pass}"""
    with open(server_dir / "server.properties", "w") as f:
        f.write(props.strip() + "\n")


def create_systemd_service(name, server_dir):
    print("➡️  Erstelle systemd Service...")
    service_file = f"/etc/systemd/system/paper-{name}.service"
    content = f"""
[Unit]
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


def monitor_log_for_warnings(server_dir):
    print("➡️  Überwache Logs auf Fehler oder Warnungen...")
    log_file = server_dir / "logs" / "latest.log"
    if log_file.exists():
        with open(log_file, "r") as f:
            for line in f:
                if any(w in line for w in ["[ERROR]", "[WARN]"]):
                    print(line.strip())


def main():
    defaults = load_config()
    name, port, rcon_port, rcon_pass, view_distance, level_name, seed, mode, proxy_secret = ask_server_properties(defaults)
    server_dir = BASE_DIR / f"paper-{name}"
    server_dir.mkdir(parents=True, exist_ok=True)

    download_latest_paper(server_dir)
    start_server_once(server_dir)
    apply_eula(server_dir)
    write_server_properties(server_dir, defaults, port, rcon_port, rcon_pass, view_distance, level_name, seed)
    create_systemd_service(name, server_dir)

    print("➡️  Starte Server erneut, um vollständige Konfiguration zu erzeugen...")
    subprocess.run(["systemctl", "restart", f"paper-{name}"])
    time.sleep(30)
    monitor_log_for_warnings(server_dir)


if __name__ == "__main__":
    main()
