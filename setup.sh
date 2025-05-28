#!/bin/bash

# Sicherstellen, dass das Skript als Root läuft
if [[ $EUID -ne 0 ]]; then
   echo "❌ Dieses Skript muss als Root ausgeführt werden."
   exit 1
fi

echo "📦 Systempakete installieren..."
apt update && apt install -y python3 python3-pip openjdk-21-jre-headless curl jq unzip git || {
    echo "❌ Fehler bei der Paketinstallation"
    exit 1
}

echo "🧰 Projekt vorbereiten..."
mkdir -p /opt/minecraft
cd /opt/minecraft || exit 1

# Repository klonen oder updaten
if [ ! -d ".git" ]; then
    echo "📥 Klone Repository..."
    git clone https://github.com/manjo80/papermc.git . || {
        echo "❌ Fehler beim Klonen des Repositories"
        exit 1
    }
else
    echo "🔁 Repository scheint schon vorhanden zu sein, ziehe neueste Änderungen..."
    git pull || echo "⚠️ Fehler beim Aktualisieren des Repositories"
fi

# Prüfen ob Manager vorhanden ist
if [ ! -f "manager.py" ]; then
    echo "❌ manager.py nicht gefunden!"
    exit 1
fi

echo "🚀 Starte Manager..."
python3 manager.py
