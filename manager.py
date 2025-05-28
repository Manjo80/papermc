import sys
import os
import subprocess

# Pfad zum bin-Ordner hinzufügen
BIN_DIR = os.path.join(os.path.dirname(__file__), 'bin')
sys.path.append(BIN_DIR)

# Module aus bin laden
try:
    from install_paper_server import run as install_paper_server
except ImportError:
    print("[FEHLER] Kann install_paper_server nicht importieren. Stelle sicher, dass die Datei in 'bin/' liegt.")
    sys.exit(1)

def uninstall_server():
    name = input("Name des Servers zum Entfernen: ").strip().lower()
    target_dir = f"/opt/minecraft/paper-{name}"
    service_name = f"paper-{name}.service"
    try:
        subprocess.run(["systemctl", "stop", service_name], check=True)
        subprocess.run(["systemctl", "disable", service_name], check=True)
        os.remove(f"/etc/systemd/system/{service_name}")
        subprocess.run(["systemctl", "daemon-reexec"], check=True)
        subprocess.run(["rm", "-rf", target_dir])
        print(f"✅ Server '{name}' wurde entfernt.")
    except Exception as e:
        print(f"[FEHLER] Beim Entfernen ist ein Fehler aufgetreten: {e}")

def open_rcon_terminal():
    host = input("Server-Host (z. B. 127.0.0.1): ").strip()
    port = input("RCON-Port (z. B. 25575): ").strip()
    password = input("RCON-Passwort: ").strip()
    try:
        subprocess.run(["mcrcon", "-H", host, "-P", port, "-p", password])
    except FileNotFoundError:
        print("[FEHLER] mcrcon ist nicht installiert. Bitte installiere es zuerst.")
    except Exception as e:
        print(f"[FEHLER] {e}")

def show_menu():
    while True:
        os.system("clear")
        print("==== Minecraft Server Manager ====")
        print("1. Neuen PaperMC Server installieren")
        print("2. Bestehenden Server deinstallieren")
        print("3. RCON-Terminal öffnen")
        print("4. Beenden")
        choice = input("> ")

        if choice == "1":
            install_paper_server()
        elif choice == "2":
            uninstall_server()
        elif choice == "3":
            open_rcon_terminal()
        elif choice == "4":
            break
        else:
            print("Ungültige Auswahl.")
            input("Drücke ENTER zum Fortfahren...")

if __name__ == "__main__":
    show_menu()
