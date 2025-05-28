#!/usr/bin/env python3

import os
import sys
import subprocess

# Konstanten
BASE_DIR = "/opt/minecraft"
BIN_DIR = os.path.join(BASE_DIR, "bin")
SERVERS_DIR = os.path.join(BASE_DIR, "servers")

# Sicherstellen, dass alle Verzeichnisse existieren
os.makedirs(BIN_DIR, exist_ok=True)
os.makedirs(SERVERS_DIR, exist_ok=True)

def main_menu():
    while True:
        print("\n=== Minecraft Server Manager ===")
        print("1. Paper Server installieren")
        print("2. Velocity installieren")
        print("3. Server starten")
        print("4. Server stoppen")
        print("5. Server deinstallieren")
        print("6. RCON-Terminal öffnen")
        print("7. Beenden")
        choice = input("Auswahl: ")

        if choice == "1":
            install_paper()
        elif choice == "2":
            install_velocity()
        elif choice == "3":
            start_server()
        elif choice == "4":
            stop_server()
        elif choice == "5":
            uninstall_server()
        elif choice == "6":
            open_rcon()
        elif choice == "7":
            sys.exit(0)
        else:
            print("❌ Ungültige Eingabe!")

def install_paper():
    print("⚙️  Installiere Paper Server...")
    subprocess.run(["python3", os.path.join(BIN_DIR, "install_paper.py")])

def install_velocity():
    print("⚙️  Installiere Velocity Proxy...")
    subprocess.run(["python3", os.path.join(BIN_DIR, "install_velocity.py")])

def start_server():
    print("🚀 Starte Server...")
    subprocess.run(["python3", os.path.join(BIN_DIR, "start_server.py")])

def stop_server():
    print("🛑 Stoppe Server...")
    subprocess.run(["python3", os.path.join(BIN_DIR, "stop_server.py")])

def uninstall_server():
    print("🧹 Deinstalliere Server...")
    subprocess.run(["python3", os.path.join(BIN_DIR, "uninstall_server.py")])

def open_rcon():
    print("🔌 Starte RCON-Terminal...")
    subprocess.run(["python3", os.path.join(BIN_DIR, "rcon_terminal.py")])

if __name__ == "__main__":
    main_menu()