import os
import subprocess
import time
import requests
from pathlib import Path
from configparser import ConfigParser
import yaml

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

def detect_velocity():
    for svc in os.listdir("/etc/systemd/system"):
        if svc.startswith("velocity-") and svc.endswith(".service"):
            name = svc.replace("velocity-", "").replace(".service", "")
            dir_path = BASE_DIR / f"velocity-{name}"
            toml = dir_path / "velocity.toml"
            secret = BASE_DIR / "forwarding.secret"
            if toml.exists() and secret.exists():
                return name, dir_path, toml, secret
    return None, None, None, None

def ask_server_properties(defaults):
    name = input("Servername: ").strip().lower()
    velocity_name, velocity_dir, velocity_toml, velocity_secret = detect_velocity()
    if velocity_toml:
        with open(velocity_toml) as f:
            for line in f:
                if line.strip().startswith("port"):
                    port = int(line.strip().split("=")[1]) + 1
                    rcon_port = port + 1
                    break
    else:
        port = int(defaults['DEFAULT_PAPER_PORT'])
        rcon_port = int(defaults['DEFAULT_RCON_PORT'])

    rcon_pass = input("RCON Passwort: ") if not velocity_secret else None
    view_distance = input(f"View Distance [{defaults['DEFAULT_VIEW_DISTANCE']}]: ") or defaults['DEFAULT_VIEW_DISTANCE']
    level_name = input("Level Name [world]: ") or "world"
    seed = input("Seed (leer für zufällig): ")
    mode = "v" if velocity_secret else "s"

    velocity_online_mode = False
    if velocity_toml and velocity_toml.exists():
        with open(velocity_toml) as f:
            for line in f:
                if line.strip().startswith("online-mode"):
                    velocity_online_mode = line.strip().split("=")[1].strip().lower() == "true"
                    break

    return name, str(port), str(rcon_port), rcon_pass, view_distance, level_name, seed, mode, velocity_secret, velocity_toml, velocity_name, velocity_online_mode

def write_server_properties(server_dir, defaults, port, rcon_port, rcon_pass, view_distance, level_name, seed, velocity_secret):
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
"""
    if velocity_secret:
        props += f"velocity-support-forwarding-secret-file=../forwarding.secret\n"
    else:
        props += f"rcon.password={rcon_pass}\n"
    with open(server_dir / "server.properties", "w") as f:
        f.write(props.strip() + "\n")

def update_spigot(server_dir):
    spigot_path = server_dir / "spigot.yml"
    if spigot_path.exists():
        with open(spigot_path, 'r') as f:
            data = yaml.safe_load(f)
        data['settings']['bungeecord'] = False
        with open(spigot_path, 'w') as f:
            yaml.dump(data, f)

def update_paper_global(server_dir, velocity_secret_path, velocity_online_mode):
    paper_config_path = server_dir / "config" / "paper-global.yml"
    if not paper_config_path.exists():
        print(f"❌ paper-global.yml nicht gefunden: {paper_config_path}")
        return

    try:
        with open(paper_config_path, 'r') as f:
            data = yaml.safe_load(f)

        if 'proxies' not in data:
            data['proxies'] = {}
        if 'velocity' not in data['proxies']:
            data['proxies']['velocity'] = {}

        data['proxies']['velocity']['enabled'] = True
        data['proxies']['velocity']['secret'] = Path(velocity_secret_path).read_text().strip()
        data['proxies']['velocity']['online-mode'] = velocity_online_mode

        with open(paper_config_path, 'w') as f:
            yaml.dump(data, f, sort_keys=False)

        print("✅ paper-global.yml wurde aktualisiert.")
    except Exception as e:
        print(f"❌ Fehler beim Aktualisieren von paper-global.yml: {e}")

def update_velocity_toml(toml_path, server_name, port):
    if toml_path.exists():
        lines = toml_path.read_text().splitlines()
        new_lines = []
        in_servers = False
        for line in lines:
            if line.strip() == "[servers]":
                in_servers = True
                new_lines.append(line)
                continue
            if in_servers and line.strip().startswith("["):
                in_servers = False
            if not in_servers:
                new_lines.append(line)
        new_lines.append(f"{server_name} = \"127.0.0.1:{port}\"")
        toml_path.write_text("\n".join(new_lines) + "\n")

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
    name, port, rcon_port, rcon_pass, view_distance, level_name, seed, mode, velocity_secret, velocity_toml, velocity_name, velocity_online_mode = ask_server_properties(defaults)
    server_dir = BASE_DIR / f"paper-{name}"
    server_dir.mkdir(parents=True, exist_ok=True)

    download_latest_paper(server_dir)
    start_server_once(server_dir)
    apply_eula(server_dir)
    write_server_properties(server_dir, defaults, port, rcon_port, rcon_pass, view_distance, level_name, seed, velocity_secret)
    update_spigot(server_dir)
    update_paper_global(server_dir, velocity_secret, velocity_online_mode)
    if velocity_toml:
        update_velocity_toml(velocity_toml, name, port)

    create_systemd_service(name, server_dir)

    print("➡️  Starte Server erneut, um vollständige Konfiguration zu erzeugen...")
    subprocess.run(["systemctl", "restart", f"paper-{name}"])
    time.sleep(30)
    monitor_log_for_warnings(server_dir)

if __name__ == "__main__":
    main()
