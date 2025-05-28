import os
import sys

# Funktion zum Löschen des Bildschirms
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Lokales Projektverzeichnis einfügen
sys.path.append(os.path.join(os.path.dirname(__file__), "bin"))

try:
    from install_paper_server import main as install_paper_server
except ImportError:
    print("[FEHLER] Kann 'install_paper_server' nicht importieren.")
    install_paper_server = None

try:
    from install_velocity_server import main as install_velocity_server
except ImportError:
    print("[FEHLER] Kann 'install_velocity_server' nicht importieren.")
    install_velocity_server = None

def show_menu():
    while True:
        clear_screen()
        print("==== Minecraft Server Manager ====")
        print("1. Neuen PaperMC Server installieren")
        print("2. Neuen Velocity Server installieren")
        print("3. Bestehenden Server deinstallieren")
        print("4. RCON-Terminal öffnen")
        print("5. Beenden")
        choice = input("> ").strip()

        if choice == "1":
            if install_paper_server:
                install_paper_server()
        elif choice == "2":
            if install_velocity_server:
                install_velocity_server()
        elif choice == "3":
            os.system("python3 bin/uninstall_server.py")
        elif choice == "4":
            os.system("python3 bin/rcon_terminal.py")
        elif choice == "5":
            print("Beende...")
            break
        else:
            print("❌ Ungültige Auswahl.")

if __name__ == "__main__":
    show_menu()
