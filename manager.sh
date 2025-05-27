#!/bin/bash
BASE_DIR="$(dirname "$0")"
BIN="$BASE_DIR/bin"

while true; do
    clear
    echo "=== Minecraft Server Manager ==="
    echo "1. Create new Paper server"
    echo "2. Install Velocity proxy"
    echo "3. Send RCON command to all servers"
    echo "4. Add server to Velocity proxy and RCON list"
    echo "5. List Velocity proxy servers"
    echo "6. Remove server from Velocity and RCON list"
    echo "7. Exit"
    echo ""
    read -p "Select an option [1–7]: " CHOICE

    case $CHOICE in
        1) bash "$BIN/create_paper.sh" ;;
        2) bash "$BIN/create_velocity.sh" ;;
        3) bash "$BIN/rcon_monitor.sh" ;;
        4) bash "$BIN/add_server_to_velocity.sh" ;;
        5) bash "$BIN/list_velocity_servers.sh" ;;
        6) bash "$BIN/remove_server_from_velocity.sh" ;;
        7) exit 0 ;;
        *) echo "Invalid option."; sleep 1 ;;
    esac
done
