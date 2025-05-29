import yaml
from pathlib import Path

def update_spigot(server_dir):
    spigot_path = server_dir / "spigot.yml"
    if spigot_path.exists():
        with open(spigot_path, 'r') as f:
            data = yaml.safe_load(f)
        data['settings']['bungeecord'] = False
        with open(spigot_path, 'w') as f:
            yaml.dump(data, f)


def update_paper_global(server_dir, velocity_secret_path, velocity_online_mode):
    paper_config_path = server_dir / "config" / "paper-global.yml"
    if not paper_config_path.exists():
        print(f"❌ paper-global.yml nicht gefunden: {paper_config_path}")
        return

    try:
        with open(paper_config_path, 'r') as f:
            data = yaml.safe_load(f)

        if 'proxies' not in data:
            data['proxies'] = {}
        if 'velocity' not in data['proxies']:
            data['proxies']['velocity'] = {}

        data['proxies']['velocity']['enabled'] = True
        data['proxies']['velocity']['secret'] = Path(velocity_secret_path).read_text().strip()
        data['proxies']['velocity']['online-mode'] = velocity_online_mode

        with open(paper_config_path, 'w') as f:
            yaml.dump(data, f, sort_keys=False)

        print("✅ paper-global.yml wurde aktualisiert.")
    except Exception as e:
        print(f"❌ Fehler beim Aktualisieren von paper-global.yml: {e}")


def update_velocity_toml(toml_path, server_name, port):
    if toml_path.exists():
        lines = toml_path.read_text().splitlines()
        new_lines = []
        in_servers = False
        for line in lines:
            if line.strip() == "[servers]":
                in_servers = True
                new_lines.append(line)
                continue
            if in_servers and line.strip().startswith("["):
                in_servers = False
            if not in_servers:
                new_lines.append(line)
        new_lines.append(f"{server_name} = \"127.0.0.1:{port}\"")
        toml_path.write_text("\n".join(new_lines) + "\n")
