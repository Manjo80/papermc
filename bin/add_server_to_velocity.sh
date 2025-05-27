#!/bin/bash
source "$(dirname "$0")/../config/global.conf"

VELOCITY_DIR="$BASE_DIR/velocity"
TOML_FILE="$VELOCITY_DIR/velocity.toml"
RCON_LIST="$BASE_DIR/rcon_targets.list"

read -p "Server name (e.g. lobby): " NAME
read -p "Server IP (e.g. 127.0.0.1): " IP
read -p "Server Port (e.g. 25565): " PORT
read -p "RCON Port (e.g. 25575): " RCON_PORT
read -p "RCON Password: " RCON_PASS

# Prüfe Existenz der Dateien
if [[ ! -f "$TOML_FILE" ]]; then
  echo "[ERROR] velocity.toml not found in $VELOCITY_DIR"
  exit 1
fi

if [[ ! -w "$TOML_FILE" ]]; then
  echo "[ERROR] Cannot write to $TOML_FILE – check permissions."
  exit 1
fi

# Backup der velocity.toml
cp "$TOML_FILE" "${TOML_FILE}.bak"

# Prüfen, ob Servereintrag bereits existiert
if grep -q "^\[$NAME\]" "$TOML_FILE"; then
  echo "[INFO] Server '$NAME' already exists in velocity.toml. Skipping insert."
else
  {
    echo ""
    echo "[$NAME]"
    echo "address = \"$IP:$PORT\""
    echo "try = [ \"$NAME\" ]"
  } >> "$TOML_FILE"
  echo "✅ Added $NAME to velocity.toml"
fi

# Prüfen, ob RCON-Eintrag bereits existiert
if [[ ! -f "$RCON_LIST" ]]; then
  touch "$RCON_LIST"
fi

if grep -q "^$NAME;$IP;$RCON_PORT;$RCON_PASS" "$RCON_LIST"; then
  echo "[INFO] RCON entry for '$NAME' already exists in rcon_targets.list. Skipping."
else
  echo "$NAME;$IP;$RCON_PORT;$RCON_PASS" >> "$RCON_LIST"
  echo "✅ RCON entry added to $RCON_LIST"
fi

echo ""
echo "➡️  You can now connect to $NAME via RCON and through Velocity."
