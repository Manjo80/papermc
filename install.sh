#!/bin/bash

# Root-Prüfung
if [[ $EUID -ne 0 ]]; then
   echo "❌ Dieses Skript muss als Root ausgeführt werden."
   exit 1
fi

echo "📦 Systempakete installieren..."
apt update && apt install -y python3 python3-pip python3-venv openjdk-21-jre-headless curl jq unzip git

echo "🧰 Verzeichnisse vorbereiten..."
mkdir -p /opt/papermc
mkdir -p /opt/minecraft

# Repository klonen, falls noch nicht vorhanden
if [ ! -d "/opt/papermc/.git" ]; then
    git clone https://github.com/manjo80/papermc.git /opt/papermc || {
        echo "❌ Fehler beim Klonen des Repositories"
        exit 1
    }
else
    echo "🔁 Repository scheint schon vorhanden zu sein."
fi

cd /opt/papermc || exit 1

# Virtuelle Umgebung einrichten
echo "🐍 Virtuelle Python-Umgebung einrichten..."
python3 -m venv .venv

# Aktivieren und Abhängigkeiten installieren
source .venv/bin/activate
echo "📦 Python-Abhängigkeiten installieren..."
pip install -r requirements.txt || {
    echo "❌ Fehler bei pip-Installation"
    exit 1
}

# Start des Managers über die virtuelle Umgebung
echo "🚀 Starte Manager..."
python manager.py
