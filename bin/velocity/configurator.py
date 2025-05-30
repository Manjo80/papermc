# velocity/configurator.py

from pathlib import Path
from velocity.config_loader import load_config

def apply_velocity_toml(server_dir: Path):
    """
    Passt die velocity.toml an mit Werten aus global.conf, inklusive:
    - motd
    - bind
    - forwarding.secret-file
    - forwarding.method
    - online-mode
    - Beibehaltung von [servers] und [forced-hosts] als Platzhalter
    """
    config = load_config("VELOCITY")

    motd = config.get("default_motd", "Velocity Server")
    bind = config.get("default_bind", "0.0.0.0:25577")
    secret_file = config.get("default_secret_file", "forwarding.secret")
    forwarding_method = config.get("default_forwarding_method", "modern")
    online_mode = config.get("default_online_mode", "true")

    toml_path = server_dir / "velocity.toml"
    if not toml_path.exists():
        raise FileNotFoundError(f"{toml_path} nicht gefunden")

    with open(toml_path, 'r') as f:
        lines = f.readlines()

    new_lines = []
    in_servers = False
    in_forced_hosts = False

    for line in lines:
        stripped = line.strip()

        if stripped.startswith("motd"):
            new_lines.append(f'motd = "{motd}"\n')
        elif stripped.startswith("bind"):
            new_lines.append(f'bind = "{bind}"\n')
        elif stripped.startswith("forwarding.secret-file"):
            new_lines.append(f'forwarding.secret-file = "{secret_file}"\n')
        elif stripped.startswith("forwarding.method"):
            new_lines.append(f'forwarding.method = "{forwarding_method}"\n')
        elif stripped.startswith("online-mode"):
            new_lines.append(f'online-mode = {online_mode.lower()}\n')
        elif stripped.startswith("[servers]"):
            new_lines.append("[servers]\n")
            new_lines.append("# Platzhalter - konfiguriere manuell\n")
            in_servers = True
        elif stripped.startswith("[forced-hosts]"):
            new_lines.append("[forced-hosts]\n")
            new_lines.append("# Platzhalter - konfiguriere manuell\n")
            in_servers = False
            in_forced_hosts = True
        elif stripped.startswith("["):
            in_servers = False
            in_forced_hosts = False
            new_lines.append(line)
        elif not in_servers and not in_forced_hosts:
            new_lines.append(line)

    with open(toml_path, 'w') as f:
        f.writelines(new_lines)

    print("✅ velocity.toml wurde angepasst.")
