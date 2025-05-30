# velocity/configurator.py

from pathlib import Path
from velocity.config_loader import load_config

def apply_velocity_toml(server_dir: Path):
    config = load_config("VELOCITY")  # Gibt ein dict zurück
    toml_path = server_dir / "velocity.toml"

    if not toml_path.exists():
        raise FileNotFoundError(f"{toml_path} nicht gefunden")

    with open(toml_path, 'r') as f:
        lines = f.readlines()

    new_lines = []
    current_section = None
    seen_keys = set()

    for line in lines:
        stripped = line.strip()

        if stripped.startswith("["):
            section = stripped.strip("[]").lower()
            current_section = section

            # Platzhalter für [servers] und [forced-hosts]
            if section == "servers":
                new_lines.append("[servers]\n")
                new_lines.append("# Platzhalter - konfiguriere manuell\n")
                continue
            elif section == "forced-hosts":
                new_lines.append("[forced-hosts]\n")
                new_lines.append("# Platzhalter - konfiguriere manuell\n")
                continue
            else:
                new_lines.append(line)
                continue

        if current_section == "servers" or current_section == "forced-hosts":
            continue  # überspringe existierende Inhalte dieser Abschnitte

        if "=" in line and current_section != "servers" and current_section != "forced-hosts":
            key, _ = line.split("=", 1)
            key = key.strip()
            if key in config and key not in seen_keys:
                new_lines.append(f"{key} = {config[key]}\n")
                seen_keys.add(key)
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)

    # Absicherung: Falls Sektionen fehlen
    if not any("[servers]" in l for l in new_lines):
        new_lines.append("\n[servers]\n# Platzhalter - konfiguriere manuell\n")
    if not any("[forced-hosts]" in l for l in new_lines):
        new_lines.append("\n[forced-hosts]\n# Platzhalter - konfiguriere manuell\n")

    with open(toml_path, 'w') as f:
        f.writelines(new_lines)
