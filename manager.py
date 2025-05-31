import os
import sys

# bin-Verzeichnis zur Modul-Suche hinzufügen
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "bin"))

# Imports aus den Unterpaketen
from paper.install_paper_server import main as install_paper_server
from velocity.install_velocity_server import main as install_velocity_server
from uninstall.uninstall_server import main as uninstall_server
from paperserver.install import main as install
# from bin.open_rcon_terminal import main as open_rcon_terminal  # optional

def show_menu():
    while True:
        os.system("clear")
        print("==== Minecraft Server Manager ====")
        print("1. Neuen PaperMC Server installieren")
        print("2. Velocity Proxy installieren")
        print("3. Bestehenden Server deinstallieren")
        print("4. RCON-Terminal öffnen")
        print("5. Beenden")
        choice = input("> ")

        if choice == "1":
            install()
        elif choice == "2":
            install_velocity_server()
        elif choice == "3":
            uninstall_server()
        elif choice == "4":
            print("❌ RCON-Terminal noch nicht implementiert.")
            input("Weiter mit Enter...")
        elif choice == "5":
            break
        else:
            print("❌ Ungültige Eingabe.")
            input("Weiter mit Enter...")

if __name__ == "__main__":
    show_menu()
