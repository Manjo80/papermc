import os
import subprocess
import time
from pathlib import Path

def start_velocity_server(temp_dir):
    print("➡️  Starte Velocity-Server zur Initialisierung...")
    process = subprocess.Popen(["java", "-jar", "velocity.jar"], cwd=temp_dir, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    log_lines = []
    try:
        while True:
            line = process.stdout.readline()
            if not line:
                break
            decoded = line.decode(errors="ignore").strip()
            print(decoded)
            log_lines.append(decoded)
            if "Unable to read/load/save your velocity.toml" in decoded or "velocity.toml" in decoded:
                break
    finally:
        process.terminate()
        process.wait()
    return log_lines

def clean_velocity_toml_config(toml_path):
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
            inside_servers = False
            inside_forced = True
            continue
        if line.strip().startswith("[") and not line.strip().startswith("[servers]") and not line.strip().startswith("[forced-hosts]"):
            inside_servers = False
            inside_forced = False
            new_lines.append(line)
            continue
        if inside_servers or inside_forced:
            continue
        new_lines.append(line)

    with open(toml_path, "w") as f:
        f.writelines(new_lines)

def copy_forwarding_secret(temp_dir, target_dir):
    secret_path = temp_dir / "forwarding.secret"
    if secret_path.exists():
        target = target_dir / "forwarding.secret"
        with open(secret_path, "rb") as src, open(target, "wb") as dst:
            dst.write(src.read())

def validate_port(port_str):
    try:
        port = int(port_str)
        if 1024 <= port <= 65535:
            return str(port)
        else:
            raise ValueError
    except ValueError:
        print("❌ Ungültiger Port. Es wird ein zufälliger freier Port verwendet (25577).")
        return "25577"

def install_velocity_server():
    BASE_DIR = Path("/opt/minecraft")
    name = input("Servername: ").strip().lower()
    port_input = input("Port [25577]: ").strip()
    port = validate_port(port_input) if port_input else "25577"
    server_dir = BASE_DIR / f"velocity-{name}"
    server_dir.mkdir(parents=True, exist_ok=True)

    print("➡️  Lade neueste Velocity-Version herunter...")
    versions = subprocess.check_output(["curl", "-s", "https://api.papermc.io/v2/projects/velocity"]).decode("utf-8")
    import json
    latest_version = json.loads(versions)["versions"][-1]
    builds = subprocess.check_output(["curl", "-s", f"https://api.papermc.io/v2/projects/velocity/versions/{latest_version}"]).decode("utf-8")
    latest_build = json.loads(builds)["builds"][-1]
    jar_name = f"velocity-{latest_version}-{latest_build}.jar"
    jar_url = f"https://api.papermc.io/v2/projects/velocity/versions/{latest_version}/builds/{latest_build}/downloads/{jar_name}"

    jar_path = server_dir / "velocity.jar"
    subprocess.run(["curl", "-s", "-o", str(jar_path), jar_url], check=True)

    log = start_velocity_server(server_dir)

    velocity_toml = server_dir / "velocity.toml"
    if velocity_toml.exists():
        clean_velocity_toml_config(velocity_toml)

    copy_forwarding_secret(server_dir, BASE_DIR)

    print("➡️  Erstelle systemd Service...")
    service_name = f"velocity-{name}"
    service_file = f"/etc/systemd/system/{service_name}.service"
    with open(service_file, "w") as f:
        f.write(f"""
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
""")
    subprocess.run(["systemctl", "daemon-reload"])
    subprocess.run(["systemctl", "enable", service_name])
    subprocess.run(["systemctl", "start", service_name])

    print("➡️  Überwache vollständigen Start des Servers...")
    time.sleep(20)
    log_file = server_dir / "logs" / "latest.log"
    if log_file.exists():
        with open(log_file, "r") as f:
            for line in f:
                print(line.strip())

if __name__ == "__main__":
    install_velocity_server()
