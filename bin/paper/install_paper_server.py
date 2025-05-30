import os
import subprocess
from pathlib import Path
from paper.downloader import download_latest_paper
from paper.logwatcher import wait_for_log_message
from paper.server_properties_editor import update_server_properties
from paper.configurator import apply_paper_configs
from paper.velocity_linker import find_velocity_servers, get_forwarding_secret
from velocity.config_loader import load_config


def main():
    base_dir = Path("/opt/minecraft")
    base_dir.mkdir(parents=True, exist_ok=True)

    server_name = input("➡️  Name des Paper-Servers: ").strip()
    if not server_name:
        print("❌ Kein Servername eingegeben.")
        return

    server_dir = base_dir / server_name
    if server_dir.exists():
        print("❌ Ein Server mit diesem Namen existiert bereits.")
        return
    server_dir.mkdir()

    # Frage, ob mit Velocity verbunden werden soll
    use_velocity = input("➡️  Mit Velocity verbinden? (j/n): ").strip().lower() == 'j'
    velocity_secret = None
    if use_velocity:
        velocity_servers = find_velocity_servers(base_dir)
        if not velocity_servers:
            print("❌ Keine Velocity-Server gefunden.")
            return
        print("➡️  Verfügbare Velocity-Server:")
        for i, v_path in enumerate(velocity_servers):
            print(f"[{i}] {v_path.name}")
        choice = input("➡️  Nummer des Velocity-Servers: ").strip()
        try:
            choice_idx = int(choice)
            selected_velocity = velocity_servers[choice_idx]
            velocity_secret = get_forwarding_secret(selected_velocity)
        except (IndexError, ValueError):
            print("❌ Ungültige Auswahl.")
            return

    # Lade PaperMC
    jar_path = download_latest_paper(server_dir)

    # Starte Server einmal bis EULA erscheint
    print("➡️  Starte Server zum Initialisieren...")
    proc = subprocess.Popen(["java", "-jar", jar_path.name], cwd=server_dir)
    wait_for_log_message(server_dir / "logs" / "latest.log", "You have not accepted the EULA")
    proc.terminate()

    # EULA akzeptieren
    eula_path = server_dir / "eula.txt"
    with eula_path.open("w") as f:
        f.write("eula=true\n")

    # Lade Konfiguration
    config = load_config("PAPER")

    # Passe server.properties an
    update_server_properties(server_dir, config)

    # Starte erneut, um spigot.yml und paper-global zu generieren
    print("➡️  Starte Server zur Generierung weiterer Dateien...")
    proc = subprocess.Popen(["java", "-jar", jar_path.name], cwd=server_dir)
    wait_for_log_message(server_dir / "logs" / "latest.log", "Done")
    proc.terminate()

    # Passe spigot.yml und paper-global.yml an
    apply_paper_configs(server_dir, config)

    # Wenn Velocity genutzt wird, Server in velocity.toml eintragen
    if use_velocity and selected_velocity:
        from velocity.toml_editor import add_server_to_velocity_config
        add_server_to_velocity_config(selected_velocity, server_name, config.get("default_port", "25565"))

    print("✅ Paper-Server wurde erfolgreich installiert.")
    print(f"➡️  Serververzeichnis: {server_dir}")
    print(f"➡️  Startbefehl: java -Xmx{config.get('default_max_ram', '2G')} -Xms{config.get('default_min_ram', '512M')} -jar {jar_path.name}")
