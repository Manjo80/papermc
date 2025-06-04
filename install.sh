#!/bin/bash

if [[ $EUID -ne 0 ]]; then
   echo "❌ Dieses Skript muss als Root ausgeführt werden."
   exit 1
fi

LOGFILE="/opt/papermc/install.log"
exec > >(tee -a "$LOGFILE") 2>&1

echo "📦 Systempakete installieren..."
apt update && apt install -y python3 python3-pip python3-venv openjdk-21-jre-headless curl jq unzip git

echo "🧰 Verzeichnisse vorbereiten..."
mkdir -p /opt/papermc
mkdir -p /opt/minecraft

cd /opt/papermc || exit 1

if [ -d .git ]; then
    echo "🔄 Repository aktualisieren..."
    git pull --rebase
else
    git clone https://github.com/manjo80/papermc.git . || {
        echo "❌ Fehler beim Klonen des Repositories"
        exit 1
    }
fi

echo "🐍 Virtuelle Python-Umgebung einrichten..."
python3 -m venv .venv
source .venv/bin/activate

echo "📦 Python-Abhängigkeiten installieren..."
pip install --upgrade pip
pip install -r requirements.txt || {
    echo "❌ Fehler bei pip-Installation"
    exit 1
}

echo "🚀 Starte Manager..."
python manager.py "$@"
