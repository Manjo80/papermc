from paper.velocity_detection import detect_velocity

def ask_server_properties(defaults):
    name = input("Servername: ").strip().lower()
    velocity_name, velocity_dir, velocity_toml, velocity_secret = detect_velocity()

    if velocity_toml:
        with open(velocity_toml) as f:
            for line in f:
                if line.strip().startswith("port"):
                    port = int(line.strip().split("=")[1]) + 1
                    rcon_port = port + 1
                    break
    else:
        port = int(defaults['DEFAULT_PAPER_PORT'])
        rcon_port = int(defaults['DEFAULT_RCON_PORT'])

    rcon_pass = input("RCON Passwort: ") if not velocity_secret else None
    view_distance = input(f"View Distance [{defaults['DEFAULT_VIEW_DISTANCE']}]: ") or defaults['DEFAULT_VIEW_DISTANCE']
    level_name = input("Level Name [world]: ") or "world"
    seed = input("Seed (leer für zufällig): ")
    mode = "v" if velocity_secret else "s"

    return name, str(port), str(rcon_port), rcon_pass, view_distance, level_name, seed, mode, velocity_secret, velocity_toml, velocity_name
