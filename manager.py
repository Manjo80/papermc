import os
import sys

# Stelle sicher, dass das bin-Verzeichnis zum sys.path hinzugefügt wird
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BIN_DIR = os.path.join(BASE_DIR, "bin")
sys.path.insert(0, BIN_DIR)

# Imports der Hauptfunktionen aus den Unterordnern
from paper.install_paper_server import main as install_paper_server
from velocity.install_velocity_server import main as install_velocity_server
from uninstall.uninstall_server import main as uninstall_server
# Optional: Implementiere dies später
# from rcon.open_rcon_terminal import main as open_rcon_terminal  

def show_menu():
    while True:
        os.system("clear")
        print("==== Minecraft Server Manager ====")
        print("1. Neuen PaperMC Server installieren")
        print("2. Velocity Proxy installieren")
        print("3. Bestehenden Server deinstallieren")
        print("4. RCON-Terminal öffnen")
        print("5. Beenden")
        choice = input("> ").strip()

        if choice == "1":
            install_paper_server()
        elif choice == "2":
            install_velocity_server()
        elif choice == "3":
            uninstall_server()
        elif choice == "4":
            print("❌ RCON-Terminal noch nicht implementiert.")
            input("Weiter mit Enter...")
            # open_rcon_terminal()
        elif choice == "5":
            break
        else:
            print("❌ Ungültige Eingabe.")
            input("Weiter mit Enter...")

if __name__ == "__main__":
    print("🚀 Starte Manager...")
    show_menu()
