# paper/server_properties_editor.py

from pathlib import Path

def write_server_properties(server_dir, defaults, port, rcon_port, rcon_pass, view_distance, level_name, seed, velocity_secret):
    print("➡️  Schreibe server.properties...")

    props = f"""
server-port={port}
motd={defaults['DEFAULT_MOTD']}
gamemode={defaults['DEFAULT_GAMEMODE']}
level-type={defaults['DEFAULT_LEVEL_TYPE']}
level-name={level_name}
level-seed={seed}
spawn-npcs={defaults['DEFAULT_NPCS']}
spawn-animals={defaults['DEFAULT_ANIMALS']}
spawn-monsters={defaults['DEFAULT_MONSTERS']}
pvp={defaults['DEFAULT_PVP']}
difficulty={defaults['DEFAULT_DIFFICULTY']}
allow-nether={defaults['DEFAULT_ALLOW_NETHER']}
allow-flight={defaults['DEFAULT_ALLOW_FLIGHT']}
view-distance={view_distance}
spawn-protection={defaults['DEFAULT_SPAWN_PROTECTION']}
enable-command-block=true
online-mode=false
enable-rcon=true
rcon.port={rcon_port}
"""

    if velocity_secret:
        props += "velocity-support-forwarding-secret-file=../forwarding.secret\n"
    else:
        props += f"rcon.password={rcon_pass}\n"

    with open(server_dir / "server.properties", "w") as f:
        f.write(props.strip() + "\n")
