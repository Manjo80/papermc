from pathlib import Path
from velocity.config_loader import load_config

def apply_velocity_toml(server_dir: Path):
    config = load_config("VELOCITY")
    toml_path = server_dir / "velocity.toml"

    with open(toml_path, 'r') as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        stripped = line.strip()
        if "=" in stripped and not stripped.startswith("#") and not stripped.startswith("["):
            key, _ = stripped.split("=", 1)
            key = key.strip()
            if key in config:
                new_lines.append(f"{key} = {config[key]}\n")
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)

    # Platzhalter für [servers] und [forced-hosts] erzwingen, falls sie fehlen
    full_text = "".join(new_lines)
    if "[servers]" not in full_text:
        new_lines.append("\n[servers]\n# Platzhalter\n")
    if "[forced-hosts]" not in full_text:
        new_lines.append("\n[forced-hosts]\n# Platzhalter\n")

    with open(toml_path, 'w') as f:
        f.writelines(new_lines)
