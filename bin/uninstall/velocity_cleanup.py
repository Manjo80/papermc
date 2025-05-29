from pathlib import Path

def remove_from_velocity_toml(toml_path: Path, server_name: str):
    if not toml_path.exists():
        print(f"❌ velocity.toml nicht gefunden: {toml_path}")
        return

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
        if in_servers and server_name in line:
            print(f"➡️  Entferne Eintrag für '{server_name}' aus velocity.toml")
            continue
        new_lines.append(line)

    toml_path.write_text("\n".join(new_lines) + "\n")
