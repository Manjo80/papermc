# bin/uninstall_server.py

from uninstall.config_loader import load_config
from uninstall.server_finder import list_paper_servers
from uninstall.service_remover import remove_systemd_service
from uninstall.file_cleaner import delete_server_directory
from uninstall.velocity_cleanup import remove_from_velocity_toml

def main():
    config = load_config()
    base_dir = config['BASE_DIR']

    print("🔍 Suche nach installierten PaperMC-Servern...")
    servers = list_paper_servers(base_dir)

    if not servers:
        print("❌ Keine Server gefunden.")
        return

    print("\n📋 Verfügbare Server:")
    for i, name in enumerate(servers, start=1):
        print(f"{i}. {name}")

    try:
        choice = int(input("\n🗑 Welchen Server möchtest du entfernen? (Nummer): "))
        if not (1 <= choice <= len(servers)):
            raise ValueError()
    except ValueError:
        print("❌ Ungültige Auswahl.")
        return

    selected_server = servers[choice - 1]
    print(f"\n⚠️  Der Server '{selected_server}' wird jetzt entfernt...")

    remove_systemd_service(selected_server)
    delete_server_directory(base_dir, selected_server)
    remove_from_velocity_toml(base_dir, selected_server)

    print(f"\n✅ Server '{selected_server}' wurde vollständig entfernt.")

if __name__ == "__main__":
    main()
