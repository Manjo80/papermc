def apply_velocity_toml(server_dir: Path):
    config = load_config("VELOCITY")  # Gibt ein dict zurück
    toml_path = server_dir / "velocity.toml"

    with open(toml_path, 'r') as f:
        lines = f.readlines()

    new_lines = []
    in_section = None

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
            if key in config:
                value = config[key]
                # Automatisch Strings quoten
                if not value.lower() in ["true", "false"] and not value.isdigit():
                    value = f'"{value}"'
                new_lines.append(f"{key} = {value}\n")
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)

    # Platzhalter für [servers] und [forced-hosts] erzwingen
    if "[servers]" not in "".join(new_lines):
        new_lines.append("\n[servers]\n# Platzhalter\n")
    if "[forced-hosts]" not in "".join(new_lines):
        new_lines.append("\n[forced-hosts]\n# Platzhalter\n")

    with open(toml_path, 'w') as f:
        f.writelines(new_lines)
