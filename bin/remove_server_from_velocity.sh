### bin/remove_server_from_velocity.sh
#!/bin/bash
source "$(dirname "$0")/../config/global.conf"

TOML_FILE="$BASE_DIR/velocity/velocity.toml"
RCON_LIST="$BASE_DIR/rcon_targets.list"

read -p "Enter server name to remove: " NAME

# Remove from velocity.toml
if [[ -f "$TOML_FILE" ]]; then
  cp "$TOML_FILE" "$TOML_FILE.bak"
  sed -i "/^\[$NAME\]/,/^$/d" "$TOML_FILE"
  echo "✅ Removed $NAME from velocity.toml"
else
  echo "[ERROR] velocity.toml not found."
fi

# Remove from rcon_targets.list
if [[ -f "$RCON_LIST" ]]; then
  cp "$RCON_LIST" "$RCON_LIST.bak"
  grep -v "^$NAME;" "$RCON_LIST.bak" > "$RCON_LIST"
  echo "✅ Removed $NAME from rcon_targets.list"
fi