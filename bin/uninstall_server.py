import os
import subprocess
from pathlib import Path

BASE_DIR = Path("/opt/minecraft")

def list_installed_servers():
    servers = []
    for entry in BASE_DIR.iterdir():
        if entry.is_dir() and (entry.name.startswith("paper-") or entry.name.startswith("velocity-")):
            servers.append(entry.name)
    return servers

def delete_server(server_name):
    server_path = BASE_DIR / server_name
    service_name = f"paper-{server_name[6:]}" if server_name.startswith("paper-") else f"velocity-{server_name[9:]}"
    
    print(f"➡️  Stoppe systemd Service {service_name}...")
    subprocess.run(["systemctl", "stop", service_name], check=False)
    subprocess.run(["systemctl", "disable", service_name], check=False)

    print(f"🗑️  Lösche systemd Service-Datei...")
    service_file = f"/etc/systemd/system/{service_name}.service"
    if os.path.exists(service_file):
        os.remove(service_file)
        subprocess.run(["systemctl", "daemon-reload"])

    print(f"🧹  Entferne Server-Verzeichnis {server_path}...")
    subprocess.run(["rm", "-rf", str(server_path)])

    print(f"✅ Server '{server_name}' wurde entfernt.")

def main():
    servers = list_installed_servers()
    if not servers:
        print("❌ Keine Server gefunden.")
        return

    print("🧾 Verfügbare Server:")
    for i, s in enumerate(servers, 1):
        print(f"{i}. {s}")

    choice = input("Wähle Server zum Löschen (Zahl): ")
    if not choice.isdigit() or int(choice) < 1 or int(choice) > len(servers):
        print("❌ Ungültige Auswahl.")
        return

    selected = servers[int(choice) - 1]
    confirm = input(f"❗ Bist du sicher, dass du '{selected}' löschen willst? (y/n): ")
    if confirm.lower() == 'y':
        delete_server(selected)
    else:
        print("🚫 Abgebrochen.")

if __name__ == "__main__":
    main()
