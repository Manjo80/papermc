#!/bin/bash
source "$(dirname "$0")/../config/global.conf"

# Systempakete
apt update && apt install -y openjdk-21-jre-headless curl jq unzip yq git build-essential

# MCRCON manuell bauen
if ! command -v mcrcon &> /dev/null; then
  echo "➡️  Installing mcrcon from source..."
  TMP_DIR=$(mktemp -d)
  git clone https://github.com/Tiiffi/mcrcon.git "$TMP_DIR/mcrcon"
  cd "$TMP_DIR/mcrcon" || exit 1
  make
  cp mcrcon /usr/local/bin/
  cd -
  rm -rf "$TMP_DIR"
else
  echo "✅ mcrcon is already installed."
fi

read -p "Instance name (e.g. velocity-hub): " NAME
TARGET_DIR="$BASE_DIR/$NAME"
mkdir -p "$TARGET_DIR"
cd "$TARGET_DIR"

# Velocity herunterladen
VERSION=$(curl -s https://api.papermc.io/v2/projects/velocity | jq -r '.versions[-1]')
BUILD=$(curl -s "https://api.papermc.io/v2/projects/velocity/versions/$VERSION" | jq -r '.builds[-1]')
JAR="velocity-${VERSION}-${BUILD}.jar"
URL="https://api.papermc.io/v2/projects/velocity/versions/${VERSION}/builds/${BUILD}/downloads/$JAR"
curl -Lo velocity.jar "$URL"

if [[ ! -f velocity.jar ]]; then
  echo "[ERROR] Velocity download failed."
  exit 1
fi

# Start-Skript
cat << EOF > start_$NAME.sh
#!/bin/bash
java -Xms$DEFAULT_MIN_RAM -Xmx$DEFAULT_MAX_RAM -jar velocity.jar
EOF
chmod +x start_$NAME.sh

# Update-Skript
cat << EOF > update_$NAME.sh
#!/bin/bash
cd "\$(dirname "\$0")"
VERSION=\$(curl -s https://api.papermc.io/v2/projects/velocity | jq -r '.versions[-1]')
BUILD=\$(curl -s "https://api.papermc.io/v2/projects/velocity/versions/\$VERSION" | jq -r '.builds[-1]')
JAR="velocity-\${VERSION}-\${BUILD}.jar"
curl -Lo velocity.jar "https://api.papermc.io/v2/projects/velocity/versions/\$VERSION/builds/\$BUILD/downloads/\$JAR"
EOF
chmod +x update_$NAME.sh

# Initialstart für velocity.toml
java -jar velocity.jar || true

TOML_FILE="$TARGET_DIR/velocity.toml"
if [[ -f "$TOML_FILE" ]]; then
  echo "Modifying velocity.toml..."
  sed -i 's/^online-mode = true/online-mode = false/' "$TOML_FILE"
  sed -i 's/^player-info-forwarding-mode = .*/player-info-forwarding-mode = "modern"/' "$TOML_FILE"

  echo ""
  echo "➡️  Velocity forwarding-secret (copy this into your PaperMC configs):"
  SECRET=$(grep -E '^[# ]*forwarding-secret\s*=' "$TOML_FILE" | head -n 1 | cut -d= -f2- | tr -d ' "')
  if [[ -n "$SECRET" ]]; then
    echo "🔐 $SECRET"
  else
    echo "[WARNING] Could not find forwarding-secret in $TOML_FILE"
  fi
  echo ""
else
  echo "[ERROR] velocity.toml not found after startup"
fi

# RCON-Liste sicherstellen
touch "$BASE_DIR/rcon_targets.list"

# RCON-Skript bereitstellen
cp "$(dirname "$0")/rcon_monitor.sh" "$BASE_DIR/rcon_monitor.sh"
chmod +x "$BASE_DIR/rcon_monitor.sh"

# systemd-Service
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

systemctl daemon-reload
systemctl enable "$NAME"
systemctl start "$NAME"

echo "✅ Velocity proxy '$NAME' installed and running at $TARGET_DIR"
echo "ℹ️  Use $BASE_DIR/rcon_monitor.sh to send RCON commands to Paper servers."
