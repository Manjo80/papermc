#!/bin/bash

# Sicherstellen, dass das Skript als Root läuft
if [[ $EUID -ne 0 ]]; then
   echo "Dieses Skript muss als Root ausgeführt werden." 
   exit 1
fi

echo "📦 Systempakete installieren..."
apt update && apt install -y python3 python3-pip openjdk-21-jre-headless curl jq unzip git

echo "🧰 Projekt vorbereiten..."
mkdir -p /opt/minecraft
cd /opt/minecraft || exit 1

# Optional: hier könntest du das Repo klonen oder prüfen
# git clone https://github.com/dein-repo/minecraft-manager.git .

echo "🚀 Starte Manager..."
python3 manager.py
