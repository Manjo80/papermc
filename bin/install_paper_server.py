# bin/install_paper_server.py

import time
import subprocess
from pathlib import Path

from paper import (
    load_config,
    download_latest_paper,
    start_server_once,
    apply_eula,
    detect_velocity,
    ask_server_properties,
    write_server_properties,
    update_spigot,
    update_paper_global,
    update_velocity_toml,
    create_systemd_service,
    monitor_log_for_warnings,
)

BASE_DIR = Path("/opt/minecraft")

def main():
    defaults = load_config()
    name, port, rcon_port, rcon_pass, view_distance, level_name, seed, mode, velocity_secret, velocity_toml, velocity_name = ask_server_properties(defaults)
    server_dir = BASE_DIR / f"paper-{name}"
    server_dir.mkdir(parents=True, exist_ok=True)

    download_latest_paper(server_dir)
    start_server_once(server_dir)
    apply_eula(server_dir)
    write_server_properties(server_dir, defaults, port, rcon_port, rcon_pass, view_distance, level_name, seed, velocity_secret)
    update_spigot(server_dir)
    if velocity_secret and velocity_toml:
        with open(velocity_toml) as f:
            online_mode = False
            for line in f:
                if "online-mode" in line and "=" in line:
                    online_mode = line.strip().split("=")[1].strip().lower() == "true"
                    break
        update_paper_global(server_dir, velocity_secret, online_mode)
        update_velocity_toml(velocity_toml, name, port)

    create_systemd_service(name, server_dir)

    print("➡️  Starte Server erneut, um vollständige Konfiguration zu erzeugen...")
    subprocess.run(["systemctl", "restart", f"paper-{name}"])
    time.sleep(30)
    monitor_log_for_warnings(server_dir)

if __name__ == "__main__":
    main()
