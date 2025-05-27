#!/bin/bash
source "$(dirname "$0")/../config/global.conf"

# Abhängigkeiten installieren
apt update && apt install -y openjdk-21-jre-headless curl jq unzip yq

# Einstellungen abfragen
read -p "Server name (e.g. lobby): " NAME
NAME=$(echo "$NAME" | tr '[:upper:]' '[:lower:]')
TARGET_DIR="/opt/minecraft/paper-$NAME"

read -p "Server port [$DEFAULT_PAPER_PORT]: " SERVER_PORT
SERVER_PORT=${SERVER_PORT:-$DEFAULT_PAPER_PORT}

read -p "RCON port [$DEFAULT_RCON_PORT]: " RCON_PORT
RCON_PORT=${RCON_PORT:-$DEFAULT_RCON_PORT}

read -p "RCON password (required): " RCON_PASS
read -p "Level name (world folder) [world]: " LEVEL_NAME
LEVEL_NAME=${LEVEL_NAME:-world}

read -p "Seed (leave empty for random): " LEVEL_SEED
read -p "View distance [$DEFAULT_VIEW_DISTANCE]: " VIEW_DISTANCE
VIEW_DISTANCE=${VIEW_DISTANCE:-$DEFAULT_VIEW_DISTANCE}

read -p "Is this server behind a Velocity proxy? (y/n): " IS_PROXY
IS_VELOCITY=false
if [[ "$IS_PROXY" =~ ^[Yy]$ ]]; then
  IS_VELOCITY=true
fi

# Verzeichnis vorbereiten
mkdir -p "$TARGET_DIR"
cd "$TARGET_DIR"

# PaperMC herunterladen
VERSION=$(curl -s https://api.papermc.io/v2/projects/paper | jq -r '.versions[-1]')
BUILD=$(curl -s "https://api.papermc.io/v2/projects/paper/versions/$VERSION" | jq -r '.builds[-1]')
JAR="paper-${VERSION}-${BUILD}.jar"
URL="https://api.papermc.io/v2/projects/paper/versions/${VERSION}/builds/${BUILD}/downloads/$JAR"
curl -Lo paper.jar "$URL"

if [[ ! -f paper.jar ]]; then
  echo "[ERROR] PaperMC download failed!"
  exit 1
fi

# Start- und Update-Skripte erstellen
cat << EOF > start_$NAME.sh
#!/bin/bash
java -Xms$DEFAULT_MIN_RAM -Xmx$DEFAULT_MAX_RAM -jar paper.jar nogui
EOF
chmod +x start_$NAME.sh

cat << EOF > update_$NAME.sh
#!/bin/bash
cd "\$(dirname "\$0")"
VERSION=\$(curl -s https://api.papermc.io/v2/projects/paper | jq -r '.versions[-1]')
BUILD=\$(curl -s "https://api.papermc.io/v2/projects/paper/versions/\$VERSION" | jq -r '.builds[-1]')
JAR="paper-\${VERSION}-\${BUILD}.jar"
curl -Lo paper.jar "https://api.papermc.io/v2/projects/paper/versions/\$VERSION/builds/\$BUILD/downloads/\$JAR"
EOF
chmod +x update_$NAME.sh

# Server initial starten (damit eula.txt + config generiert wird)
java -jar paper.jar nogui &> /dev/null &
PID=$!
sleep 10
kill "$PID" 2>/dev/null

# EULA akzeptieren
echo "eula=true" > eula.txt

# server.properties schreiben
cat << EOF > server.properties
server-port=$SERVER_PORT
motd=$DEFAULT_MOTD
gamemode=$DEFAULT_GAMEMODE
level-type=$DEFAULT_LEVEL_TYPE
level-name=$LEVEL_NAME
level-seed=$LEVEL_SEED
spawn-npcs=$DEFAULT_NPCS
spawn-animals=$DEFAULT_ANIMALS
spawn-monsters=$DEFAULT_MONSTERS
pvp=$DEFAULT_PVP
difficulty=$DEFAULT_DIFFICULTY
allow-nether=$DEFAULT_ALLOW_NETHER
allow-flight=$DEFAULT_ALLOW_FLIGHT
view-distance=$VIEW_DISTANCE
spawn-protection=$DEFAULT_SPAWN_PROTECTION
enable-command-block=true
online-mode=false
enable-rcon=true
rcon.port=$RCON_PORT
rcon.password=$RCON_PASS
EOF

# Auf Konfigdateien warten
for i in {1..10}; do
  [[ -f spigot.yml && -f config/paper-global.yml ]] && break
  sleep 1
done

# Velocity-Integration konfigurieren
if [[ "$IS_VELOCITY" == "true" ]]; then
  echo -e "\n➡️  Activating Velocity support..."

  SECRET_FILE="/opt/minecraft/velocity/forwarding.secret"
  if [[ -f "$SECRET_FILE" ]]; then
    SECRET=$(cat "$SECRET_FILE")
    yq e -i '.settings.bungeecord = true' spigot.yml
    yq e -i ".proxies.velocity.enabled = true | .proxies.velocity.online-mode = true | .proxies.velocity.secret = \"$SECRET\"" config/paper-global.yml
  else
    echo "[WARNING] Could not find Velocity secret file: $SECRET_FILE"
  fi
fi

# systemd-Dienst anlegen
cat << EOF > "/etc/systemd/system/paper-$NAME.service"
[Unit]
Description=PaperMC Server: $NAME
After=network.target

[Service]
WorkingDirectory=$TARGET_DIR
ExecStartPre=$TARGET_DIR/update_$NAME.sh
ExecStart=$TARGET_DIR/start_$NAME.sh
Restart=always
User=root

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable "paper-$NAME"
systemctl start "paper-$NAME"

# Zusammenfassung
echo ""
echo "✅ PaperMC server '$NAME' created and running."

if [[ "$IS_VELOCITY" == "true" ]]; then
  echo ""
  echo "➡️  Add the following to your Velocity's velocity.toml:"
  echo "[$NAME]"
  echo "address = \"$(hostname -I | awk '{print $1}'):$SERVER_PORT\""
  echo "try = [ \"$NAME\" ]"
fi

echo ""
read -p "Drücke [Enter] um zum Menü zurückzukehren..."
