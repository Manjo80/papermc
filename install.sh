#!/bin/bash
# Root-Pr  fung
if [[ $EUID -ne 0 ]]; then
   echo " ^}^l Dieses Skript muss als Root ausgef  hrt werden."
   exit 1
fi

# Pakete installieren
apt update && apt install -y python3 python3-pip openjdk-21-jre-headless curl jq unzip git

# Verzeichnisse vorbereiten
mkdir -p /opt/papermc
mkdir -p /opt/minecraft

# Repository klonen, falls noch nicht vorhanden
if [ ! -d "/opt/papermc/.git" ]; then
    git clone https://github.com/manjo80/papermc.git /opt/papermc || {
        echo " ^}^l Fehler beim Klonen des Repositories"
        exit 1
    }
else
    echo " ^=^t^a Repository scheint schon vorhanden zu sein."
fi

# In das Repo wechseln und manager starten
cd /opt/papermc || exit 1
python3 manager.py
