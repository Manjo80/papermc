from paper.config_loader import load_config
from paper.downloader import download_latest_paper
from paper.initializer import (
    apply_eula,
    run_server_once,
    run_server_until_generated,
    start_server_once,
    start_server_fully_and_stop
)
from paper.velocity_detection import detect_velocity
from paper.input_collector import ask_server_properties
from paper.property_writer import write_server_properties
from paper.config import (
    update_spigot,
    update_paper_global,
    update_velocity_toml
)
from paper.service_creator import create_systemd_service
from paper.log_monitor import monitor_log_for_warnings

from pathlib import Path
import subprocess
import time

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

    # Jetzt vollständiger Start und Stop
    start_server_fully_and_stop(server_dir)

    update_spigot(server_dir)
    velocity_online_mode = False
    if velocity_toml:
        with open(velocity_toml) as f:
            for line in f:
                if "online-mode" in line and "=" in line:
                    velocity_online_mode = line.split("=")[1].strip().lower() == "true"
                    break
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
