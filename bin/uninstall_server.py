from uninstall.service_remover import remove_service
from uninstall.directory_cleaner import remove_server_directory
from uninstall.velocity_cleaner import remove_velocity_entry
from uninstall.file_cleaner import remove_server_files

def main():
    name = input("➡️  Name des Servers zum Entfernen: ").strip().lower()
    
    print("🛑 Stoppe und entferne systemd-Dienst...")
    remove_service(name)

    print("🧹 Lösche Serververzeichnis und paper.jar...")
    remove_server_files(name)
    remove_server_directory(name)

    print("🧽 Entferne Servereintrag aus velocity.toml (falls vorhanden)...")
    remove_velocity_entry(name)

    print("✅ Server erfolgreich entfernt.")

if __name__ == "__main__":
    main()
