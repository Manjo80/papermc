from pathlib import Path
import shutil
import yaml

def copy_velocity_secret(velocity_dir: Path, paper_server_dir: Path):
    secret_file = velocity_dir / "forwarding.secret"
    if secret_file.exists():
        shutil.copy(secret_file, paper_server_dir / "forwarding.secret")
        print("✅ forwarding.secret wurde kopiert.")
    else:
        print("❌ forwarding.secret nicht gefunden.")

def update_spigot_yml(server_dir: Path):
    spigot_path = server_dir / "spigot.yml"
    if not spigot_path.exists():
        print("❌ spigot.yml nicht gefunden.")
        return

    with spigot_path.open("r") as f:
        config = yaml.safe_load(f)

    config['settings']['bungeecord'] = True

    with spigot_path.open("w") as f:
        yaml.dump(config, f)

    print("✅ spigot.yml angepasst.")

def update_paper_global_yml(server_dir: Path):
    paper_global_path = server_dir / "config" / "paper-global.yml"
    if not paper_global_path.exists():
        print("❌ paper-global.yml nicht gefunden.")
        return

    with paper_global_path.open("r") as f:
        config = yaml.safe_load(f)

    config['proxies'] = config.get('proxies', {})
    config['proxies']['velocity'] = {
        'enabled': True,
        'online-mode': True,
        'secret': str(server_dir / "forwarding.secret")
    }

    with paper_global_path.open("w") as f:
        yaml.dump(config, f)

    print("✅ paper-global.yml angepasst.")

def find_velocity_server(base_dir: Path) -> Path | None:
    for subdir in base_dir.iterdir():
        if subdir.is_dir() and subdir.name.startswith("velocity-"):
            if (subdir / "velocity.toml").exists():
                return subdir
    return None

def update_velocity_toml(
    velocity_dir: Path,
    server_name: str,
    server_ip: str,
    server_port: int,
    set_forced_host: bool,
    set_try: bool
):
    velocity_config_path = velocity_dir / "velocity.toml"
    if not velocity_config_path.exists():
        print("❌ velocity.toml nicht gefunden.")
        return

    # Lese Datei als Text
    with velocity_config_path.open("r", encoding="utf-8") as f:
        lines = f.readlines()

    # Blocks vorbereiten
    servers_block = f"{server_name} = \"{server_ip}:{server_port}\"\n"
    forced_hosts_block = (
        f"\"{server_name}.example.com\" = [ \"{server_name}\",]\n" if set_forced_host else ""
    )
    try_block = f"try = [ \"{server_name}\",]\n" if set_try else ""

    # Flags und Hilfsvariablen
    in_servers, in_forced_hosts, in_try = False, False, False
    new_lines = []
    servers_written = False
    forced_hosts_written = False
    try_written = False

    for line in lines:
        # [servers] block
        if line.strip().startswith("[servers]"):
            in_servers = True
            new_lines.append(line)
            new_lines.append(servers_block)
            servers_written = True
            continue
        if in_servers and (line.strip().startswith("[") and not line.strip().startswith("[servers]")):
            in_servers = False

        if not in_servers or line.strip().startswith("[servers]"):
            # [forced-hosts] block
            if line.strip().startswith("[forced-hosts]"):
                in_forced_hosts = True
                new_lines.append(line)
                if set_forced_host:
                    new_lines.append(forced_hosts_block)
                    forced_hosts_written = True
                continue
            if in_forced_hosts and (line.strip().startswith("[") and not line.strip().startswith("[forced-hosts]")):
                in_forced_hosts = False

            # try block
            if line.strip().startswith("try"):
                if set_try:
                    new_lines.append(try_block)
                    try_written = True
                continue

            # Normale Zeile, kein Block
            if not in_servers and not in_forced_hosts:
                new_lines.append(line)

    # Falls [servers] noch nicht geschrieben (z.B. nicht vorhanden)
    if not servers_written:
        new_lines.append("\n[servers]\n")
        new_lines.append(servers_block)
    if set_forced_host and not forced_hosts_written:
        new_lines.append("\n[forced-hosts]\n")
        new_lines.append(forced_hosts_block)
    if set_try and not try_written:
        new_lines.append(try_block)

    with velocity_config_path.open("w", encoding="utf-8") as f:
        f.writelines(new_lines)

    print("✅ velocity.toml wurde sicher angepasst (ohne komplette Überschreibung).")
