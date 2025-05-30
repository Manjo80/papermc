# paper/config.py

import yaml
from pathlib import Path


def update_spigot(server_dir: Path):
    """Deaktiviert BungeeCord in der spigot.yml."""
    spigot_path = server_dir / "spigot.yml"
    if not spigot_path.exists():
        print(f"⚠️ spigot.yml nicht gefunden in {spigot_path}")
        return

    with spigot_path.open("r") as f:
        data = yaml.safe_load(f)

    if "settings" not in data:
        data["settings"] = {}
    data["settings"]["bungeecord"] = False

    with spigot_path.open("w") as f:
        yaml.dump(data, f, sort_keys=False)

    print("✅ spigot.yml angepasst (bungeecord = false).")


def update_paper_global(server_dir: Path, velocity_secret_path: Path, velocity_online_mode: bool):
    """Aktualisiert paper-global.yml mit Velocity-Informationen."""
    paper_config_path = server_dir / "config" / "paper-global.yml"
    if not paper_config_path.exists():
        print(f"❌ paper-global.yml nicht gefunden: {paper_config_path}")
        return

    try:
        with paper_config_path.open("r") as f:
            data = yaml.safe_load(f) or {}

        proxies = data.setdefault("proxies", {})
        velocity = proxies.setdefault("velocity", {})
        velocity["enabled"] = True
        velocity["secret"] = velocity_secret_path.read_text().strip()
        velocity["online-mode"] = velocity_online_mode

        with paper_config_path.open("w") as f:
            yaml.dump(data, f, sort_keys=False)

        print("✅ paper-global.yml wurde aktualisiert.")
    except Exception as e:
        print(f"❌ Fehler beim Aktualisieren von paper-global.yml: {e}")


def update_velocity_toml(toml_path: Path, server_name: str, port: str):
    """Trägt den Paper-Server in die velocity.toml unter [servers] ein."""
    if not toml_path.exists():
        print(f"❌ velocity.toml nicht gefunden: {toml_path}")
        return

    lines = toml_path.read_text().splitlines()
    new_lines = []
    in_servers = False
    servers_written = False

    for line in lines:
        stripped = line.strip()
        if stripped == "[servers]":
            in_servers = True
            new_lines.append(line)
            continue
        if in_servers and stripped.startswith("["):
            # Neue Section beginnt, also neuen Server einfügen
            new_lines.append(f'{server_name} = "127.0.0.1:{port}"')
            servers_written = True
            in_servers = False

        new_lines.append(line)

    # Wenn keine Section danach kam und nichts eingefügt wurde
    if in_servers and not servers_written:
        new_lines.append(f'{server_name} = "127.0.0.1:{port}"')

    toml_path.write_text("\n".join(new_lines) + "\n")
    print(f"✅ {server_name} in velocity.toml eingetragen.")


def apply_paper_configs(server_dir: Path, config: dict):
    """Wendet spigot.yml- und paper-global.yml-Konfiguration an."""
    velocity_secret_path = server_dir.parent / "forwarding.secret"
    velocity_online_mode = config.get("online-mode", "false") == "true"

    update_spigot(server_dir)
    update_paper_global(server_dir, velocity_secret_path, velocity_online_mode)
