# velocity/configurator.py

from pathlib import Path

def apply_velocity_toml(server_dir: Path):
    """
    Passt die velocity.toml so an, dass die [servers] und [forced-hosts] Sektionen
    als Platzhalter erhalten bleiben, aber nicht leer sind.
    """
    print("➡️  Passe velocity.toml an...")
    toml_path = server_dir / "velocity.toml"
    if not toml_path.exists():
        raise FileNotFoundError("velocity.toml nicht gefunden")

    with open(toml_path, 'r') as f:
        lines = f.readlines()

    new_lines = []
    in_servers = False
    in_forced_hosts = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("[servers]"):
            new_lines.append("[servers]\n")
            new_lines.append("# Platzhalter - konfiguriere manuell\n")
            in_servers = True
            continue
        elif stripped.startswith("[forced-hosts]"):
            new_lines.append("[forced-hosts]\n")
            new_lines.append("# Platzhalter - konfiguriere manuell\n")
            in_forced_hosts = True
            in_servers = False
            continue
        elif stripped.startswith("["):
            in_servers = False
            in_forced_hosts = False
            new_lines.append(line)
            continue

        if not in_servers and not in_forced_hosts:
            new_lines.append(line)

    with open(toml_path, 'w') as f:
        f.writelines(new_lines)
