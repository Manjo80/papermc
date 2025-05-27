#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BASE_DIR="/opt/minecraft"
source "$SCRIPT_DIR/../config/global.conf"

# Abhängigkeiten installieren
apt update && apt install -y openjdk-21-jre-headless curl jq unzip yq

# Einstellungen abfragen
read -p "Server name (e.g. lobby): " NAME
NAME=$(echo "$NAME" | tr '[:upper:]' '[:lower:]')
TARGET_DIR="$BASE_DIR/paper-$NAME"

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

# Zielverzeichnis
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

# Startskript
cat << EOF > start_$NAME.sh
#!/bin/bash
java -Xms$DEFAULT_MIN_RAM -Xmx$DEFAULT_MAX_RAM -jar paper.jar nogui
EOF
chmod +x start_$NAME.sh

# Update-Skript
cat << EOF > update_$NAME.sh
#!/bin/bash
cd "\$(dirname "\$0")"
VERSION=\$(curl -s https://api.papermc.io/v2/projects/paper | jq -r '.versions[-1]')
BUILD=\$(curl -s "https://api.papermc.io/v2/projects/paper/versions/\$VERSION" | jq -r '.builds[-1]')
JAR="paper-\${VERSION}-\${BUILD}.jar"
curl -Lo paper.jar "https://api.papermc.io/v2/projects/paper/versions/\$VERSION/builds/\$BUILD/downloads/\$JAR"
EOF
chmod +x update_$NAME.sh

# ➤ Initialstart: nur für Generierung von Konfigs
echo "➡️  Running Paper once to generate config files..."
java -jar paper.jar nogui &
PAPER_PID=$!
sleep 5
kill "$PAPER_PID"
sleep 2

# EULA akzeptieren
echo "eula=true" > eula.txt

# Warte auf Konfigdateien
for i in {1..10}; do
  [[ -f server.properties && -f spigot.yml && -f config/paper-global.yml ]] && break
  sleep 1
done

# server.properties überschreiben
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

# Velocity-Integration konfigurieren
if [[ "$IS_VELOCITY" == "true" ]]; then
  echo "➡️  Activating Velocity support..."
  yq eval '.settings.bungeecord = true' -i spigot.yml
  yq eval ".proxies.velocity.enabled = true | .proxies.velocity.online-mode = true | .proxies.velocity.secret = \"REPLACE_WITH_SECRET\"" -i config/paper-global.yml
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

# Server über systemd starten
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
  echo "address = \"<IP-OF-THIS-SERVER>:$SERVER_PORT\""
  echo "try = [ \"$NAME\" ]"
  echo ""
  echo "Remember to insert the Velocity secret into this server's config/paper-global.yml"
fi

read -p "Press ENTER to return to menu..."
