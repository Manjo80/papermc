from pathlib import Path
from velocity.config_loader import load_config

def apply_velocity_toml(server_dir: Path):
    config = load_config("VELOCITY")  # Gibt ein dict zurück
    toml_path = server_dir / "velocity.toml"

    with open(toml_path, 'r') as f:
        lines = f.readlines()

    new_lines = []
    in_section = None

    # Mapping vorbereiten: key umformatieren wie in der toml erwartet
    formatted_config = {}
    for key, value in config.items():
        clean_key = key.replace("default_", "").lower().replace("_", "-")
        if value.lower() not in ["true", "false"] and not value.replace('.', '', 1).isdigit():
            value = value.strip('"')  # Vorhandene " entfernen
            value = f'"{value}"'
        formatted_config[clean_key] = value

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("["):
            section = stripped.strip("[]")
            in_section = section
            new_lines.append(line)
            continue

        key_value = stripped.split("=", 1)
        if len(key_value) == 2:
            key = key_value[0].strip()
            if key in formatted_config:
                value = formatted_config[key]
                new_lines.append(f"{key} = {value}\n")
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)

    # Platzhalter für [servers] und [forced-hosts] erzwingen, falls nicht vorhanden
    if "[servers]" not in "".join(new_lines):
        new_lines.append("\n[servers]\n# Platzhalter\n")
    if "[forced-hosts]" not in "".join(new_lines):
        new_lines.append("\n[forced-hosts]\n# Platzhalter\n")

    with open(toml_path, 'w') as f:
        f.writelines(new_lines)
