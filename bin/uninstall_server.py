from bin.uninstall.config_loader import load_config
from bin.uninstall.server_finder import list_paper_servers
from bin.uninstall.service_remover import remove_systemd_service
from bin.uninstall.file_cleaner import delete_server_directory
from bin.uninstall.velocity_cleanup import remove_from_velocity_toml
from pathlib import Path

def main():
    config = load_config()
    servers = list_paper_servers()

    if not servers:
        print("❌ Keine Paper-Server gefunden.")
        return

    print("📋 Verfügbare Server:")
    for i, srv in enumerate(servers):
        print(f"{i + 1}. {srv}")

    try:
        choice = int(input("❓ Welchen Server möchtest du löschen (Nummer): ")) - 1
        if choice < 0 or choice >= len(servers):
            print("❌ Ungültige Auswahl.")
            return
    except ValueError:
        print("❌ Ungültige Eingabe.")
        return

    server_name = servers[choice]

    # Velocity cleanup vorbereiten
    velocity_name = None
    velocity_toml = None
    velocity_path = Path(config["BASE_DIR"])
    for sub in velocity_path.iterdir():
        if sub.is_dir() and sub.name.startswith("velocity-"):
            candidate = sub / "velocity.toml"
            if candidate.exists():
                velocity_name = sub.name.replace("velocity-", "")
                velocity_toml = candidate
                break

    # Entferne systemd-Service und Serverdateien
    remove_systemd_service("paper", server_name)
    delete_server_directory("paper", server_name)

    # Entferne aus velocity.toml falls vorhanden
    if velocity_toml:
        remove_from_velocity_toml(velocity_toml, server_name)

    print(f"✅ Server '{server_name}' wurde erfolgreich entfernt.")

if __name__ == "__main__":
    main()
