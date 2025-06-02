from pathlib import Path
import shutil
import yaml
import toml

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
    """
    Sucht im base_dir nach einem Ordner, der mit 'velocity-' beginnt und eine 'velocity.toml' enthält.
    Gibt den Pfad zurück oder None, falls nichts gefunden wurde.
    """
    for subdir in base_dir.iterdir():
        if subdir.is_dir() and subdir.name.startswith("velocity-"):
            if (subdir / "velocity.toml").exists():
                return subdir
    return None

def update_velocity_toml(velocity_dir: Path, server_name: str, server_ip: str, server_port: int, set_forced_host: bool, set_try: bool):
    velocity_config_path = velocity_dir / "velocity.toml"
    if not velocity_config_path.exists():
        print("❌ velocity.toml nicht gefunden.")
        return

    with velocity_config_path.open("r") as f:
        config = toml.load(f)

    config.setdefault('servers', {})[server_name] = f"{server_ip}:{server_port}"

    if set_forced_host:
        config.setdefault('forced-hosts', {})[server_name + ".example.com"] = [server_name]
    else:
        config.pop('forced-hosts', None)

    if set_try:
        try_list = config.get("try", [])
        if server_name not in try_list:
            try_list.append(server_name)
        config["try"] = try_list

    with velocity_config_path.open("w") as f:
        toml.dump(config, f)

    print("✅ velocity.toml wurde angepasst.")
