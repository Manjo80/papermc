from uninstall.service_remover import remove_service
from uninstall.folder_cleaner import remove_server_folder
from uninstall.velocity_toml_editor import remove_from_velocity_toml
from config.config_loader import load_config
from pathlib import Path
import sys

BASE_DIR = Path("/opt/minecraft")

def uninstall_server():
    config = load_config()
    name = input("Name des zu entfernenden Servers: ").strip().lower()

    paper_dir = BASE_DIR / f"paper-{name}"
    velocity_dirs = list(BASE_DIR.glob("velocity-*/velocity.toml"))

    if not paper_dir.exists():
        print(f"❌ Serververzeichnis nicht gefunden: {paper_dir}")
        sys.exit(1)

    remove_service(name, "paper")
    remove_server_folder(paper_dir)

    for toml_path in velocity_dirs:
        remove_from_velocity_toml(toml_path, name)

    print(f"✅ Server {name} erfolgreich entfernt.")

if __name__ == "__main__":
    uninstall_server()
