#!/bin/bash
SCRIPT_DIR="$(dirname "$0")"
BASE_DIR="/opt/minecraft"
CONFIG_FILE="$SCRIPT_DIR/../config/global.conf"
BIN_DIR="$SCRIPT_DIR/bin"

# === Konfiguration laden oder Defaults setzen ===
if [[ -f "$CONFIG_FILE" ]]; then
  source "$CONFIG_FILE"
fi
DEFAULT_MIN_RAM="${DEFAULT_MIN_RAM:-512M}"
DEFAULT_MAX_RAM="${DEFAULT_MAX_RAM:-1G}"

# === Systempakete installieren ===
apt update && apt install -y openjdk-21-jre-headless curl jq unzip yq git build-essential

# === mcrcon installieren ===
if ! command -v mcrcon &> /dev/null; then
  echo "➡️  Installing mcrcon from source..."
  TMP_DIR=$(mktemp -d)
  git clone https://github.com/Tiiffi/mcrcon.git "$TMP_DIR/mcrcon"
  cd "$TMP_DIR/mcrcon" || exit 1
  make
  cp mcrcon /usr/local/bin/
  cd - >/dev/null
  rm -rf "$TMP_DIR"
else
  echo "✅ mcrcon is already installed."
fi

# === Instanznamen abfragen ===
read -p "Instance name (e.g. velocity-hub): " NAME
TARGET_DIR="$BASE_DIR/$NAME"
mkdir -p "$TARGET_DIR"
cd "$TARGET_DIR" || exit 1

# === Velocity herunterladen ===
VERSION=$(curl -s https://api.papermc.io/v2/projects/velocity | jq -r '.versions[-1]')
BUILD=$(curl -s "https://api.papermc.io/v2/projects/velocity/versions/$VERSION" | jq -r '.builds[-1]')
JAR="velocity-${VERSION}-${BUILD}.jar"
URL="https://api.papermc.io/v2/projects/velocity/versions/${VERSION}/builds/${BUILD}/downloads/$JAR"
curl -Lo velocity.jar "$URL"

if [[ ! -f velocity.jar ]]; then
  echo "[ERROR] Velocity download failed."
  exit 1
fi

# === Start- und Update-Skripte ===
cat << EOF > start_$NAME.sh
#!/bin/bash
java -Xms$DEFAULT_MIN_RAM -Xmx$DEFAULT_MAX_RAM -jar velocity.jar
EOF
chmod +x start_$NAME.sh

cat << EOF > update_$NAME.sh
#!/bin/bash
cd "\$(dirname "\$0")"
VERSION=\$(curl -s https://api.papermc.io/v2/projects/velocity | jq -r '.versions[-1]')
BUILD=\$(curl -s "https://api.papermc.io/v2/projects/velocity/versions/\$VERSION" | jq -r '.builds[-1]')
JAR="velocity-\${VERSION}-\${BUILD}.jar"
curl -Lo velocity.jar "https://api.papermc.io/v2/projects/velocity/versions/\$VERSION/builds/\$BUILD/downloads/\$JAR"
EOF
chmod +x update_$NAME.sh

# === Initialstart für Konfiguration ===
echo "➡️  Running Velocity once to generate config files..."
java -jar velocity.jar &
VELOCITY_PID=$!
sleep 5
kill "$VELOCITY_PID"
sleep 2

# === velocity.toml anpassen ===
TOML_FILE="$TARGET_DIR/velocity.toml"
if [[ -f "$TOML_FILE" ]]; then
  echo "➡️  Modifying velocity.toml ..."

  # Werte setzen
  sed -i 's/^player-info-forwarding-mode = .*/player-info-forwarding-mode = "modern"/' "$TOML_FILE"
  sed -i 's/^online-mode = true/online-mode = false/' "$TOML_FILE"
  sed -i "s/^motd = .*/motd = \"$NAME\"/" "$TOML_FILE"

  # [servers] und [forced-hosts] leeren, aber erhalten
  awk '
    /^\[servers\]/ {
      print "[servers]"
      skip=1
      next
    }
    /^\[forced-hosts\]/ {
      print "[forced-hosts]"
      skip=1
      next
    }
    /^\[/ {
      skip=0
    }
    skip==0 { print }
  ' "$TOML_FILE" > "$TOML_FILE.tmp" && mv "$TOML_FILE.tmp" "$TOML_FILE"

  # forwarding.secret anzeigen
  SECRET_FILE=$(grep -E '^forwarding-secret-file *= *' "$TOML_FILE" | cut -d= -f2- | tr -d ' "')
  if [[ -f "$TARGET_DIR/$SECRET_FILE" ]]; then
    echo ""
    echo "➡️  Velocity forwarding-secret (copy this into your PaperMC configs):"
    cat "$TARGET_DIR/$SECRET_FILE"
    echo ""
  else
    echo "[WARNING] forwarding.secret not found"
  fi
else
  echo "[ERROR] velocity.toml not found after startup"
fi

# === RCON-Monitoring ===
touch "$BASE_DIR/rcon_targets.list"
if [[ -f "$BIN_DIR/rcon_monitor.sh" ]]; then
  cp "$BIN_DIR/rcon_monitor.sh" "$BASE_DIR/rcon_monitor.sh"
  chmod +x "$BASE_DIR/rcon_monitor.sh"
else
  echo "[WARNING] rcon_monitor.sh not found in $BIN_DIR. Skipped copying."
fi

# === systemd-Service ===
cat << EOF > "/etc/systemd/system/$NAME.service"
[Unit]
Description=Velocity Proxy Server ($NAME)
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

systemctl daemon-reexec
systemctl daemon-reload
systemctl enable "$NAME"

echo ""
echo "✅ Velocity proxy '$NAME' installiert unter: $TARGET_DIR"
echo "➡️  Starte ihn bei Bedarf mit: systemctl start $NAME"
echo "📡 RCON-Tool: $BASE_DIR/rcon_monitor.sh"
read -p "Drücke ENTER um zurück zum Menü zu kommen ..."
