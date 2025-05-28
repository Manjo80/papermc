import os
from bin.install_paper_server import main as install_paper_server
from bin.install_velocity_server import main as install_velocity_server
from bin.uninstall_server import main as uninstall_server
from bin.open_rcon_terminal import main as open_rcon_terminal  # falls noch nicht vorhanden, musst du diese Datei erstellen

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
            install_paper_server()
        elif choice == "2":
            install_velocity_server()
        elif choice == "3":
            uninstall_server()
        elif choice == "4":
            open_rcon_terminal()
        elif choice == "5":
            break
        else:
            print("❌ Ungültige Eingabe.")
            input("Weiter mit Enter...")

if __name__ == "__main__":
    show_menu()
