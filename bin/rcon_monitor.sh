#!/bin/bash
source "$(dirname "$0")/../config/global.conf"

CMD=${1:-"list"}
echo "=== RCON Monitor (Parallel): $CMD ==="

RCON_LIST="$BASE_DIR/rcon_targets.list"

if [[ ! -f "$RCON_LIST" || ! -s "$RCON_LIST" ]]; then
  echo "[INFO] No servers in list."
  exit 0
fi

# Funktion zur Abfrage pro Server
rcon_query() {
  local line="$1"
  [[ -z "$line" ]] && return

  NAME=$(echo "$line" | cut -d';' -f1)
  HOST=$(echo "$line" | cut -d';' -f2)
  PORT=$(echo "$line" | cut -d';' -f3)
  PASS=$(echo "$line" | cut -d';' -f4)

  echo "--- $NAME ($HOST:$PORT) ---"
  mcrcon -H "$HOST" -P "$PORT" -p "$PASS" "$CMD" 2>/dev/null || echo "[ERROR] $NAME failed"
  echo ""
}

# Starte alle Anfragen parallel
while IFS= read -r line; do
  rcon_query "$line" &
done < "$RCON_LIST"

wait
