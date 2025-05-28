#!/bin/bash
# Sicherstellen, dass das Skript als Root läuft
if [[ $EUID -ne 0 ]]; then
   echo "❌ Dieses Skript muss als Root ausgeführt werden." 
   exit 1
fi

echo "📦 Systempakete installieren..."
apt update && apt install -y python3 python3-pip openjdk-21-jre-headless curl jq unzip git

echo "🧰 Projekt vorbereiten..."
mkdir -p /opt/minecraft
cd /opt/minecraft || exit 1

# Optional: Repository klonen, wenn es noch nicht da ist
if [ ! -d ".git" ]; then
  echo "📥 Klone Repository..."
  git clone https://github.com/manjo80/papermc.git .
else
  echo "🔁 Repository scheint schon vorhanden zu sein."
fi

echo "🚀 Starte Manager..."
python3 manager.py
