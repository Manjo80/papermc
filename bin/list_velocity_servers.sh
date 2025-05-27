### bin/list_velocity_servers.sh
#!/bin/bash
source "$(dirname "$0")/../config/global.conf"

TOML_FILE="$BASE_DIR/velocity/velocity.toml"

if [[ ! -f "$TOML_FILE" ]]; then
  echo "[ERROR] velocity.toml not found."
  exit 1
fi

echo "=== Registered Servers in Velocity ==="
grep -E "^\[.*\]" "$TOML_FILE" | tr -d "[]"