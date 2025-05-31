import os
import subprocess
from pathlib import Path
import requests

# Konfigurationswerte aus global.conf laden
def load_config():
    from configparser import ConfigParser
    config_path = Path(__file__).resolve().parent.parent / "config" / "global.conf"
    config = ConfigParser()
    config.read(config_path)
    return config['DEFAULT']

# Lade neueste PaperMC-Version herunter
def download_latest_paper(target_dir: Path) -> Path:
    print("➡️  Lade neueste PaperMC-Version herunter...")
    versions = requests.get("https://api.papermc.io/v2/projects/paper").json()
    latest_version = versions["versions"][-1]

    builds = requests.get(f"https://api.papermc.io/v2/projects/paper/versions/{latest_version}").json()
    latest_build = builds["builds"][-1]

    jar_name = f"paper-{latest_version}-{latest_build}.jar"
    jar_url = f"https://api.papermc.io/v2/projects/paper/versions/{latest_version}/builds/{latest_build}/downloads/{jar_name}"
    jar_path = target_dir / "paper.jar"

    r = requests.get(jar_url, stream=True)
    r.raise_for_status()

    with open(jar_path, 'wb') as f:
        for chunk in r.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)

    print(f"✅ PaperMC heruntergeladen: {jar_path}")
    return jar_path

# Starte Server einmal, um EULA zu erzeugen
def start_server_until_eula(server_dir: Path):
    print("➡️  Starte Server zum Generieren der EULA...")
    process = subprocess.Popen(
        ["java", "-Xmx512M", "-Xms512M", "-jar", "paper.jar"],
        cwd=server_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )

    try:
        for line in process.stdout:
            decoded = line.decode(errors="ignore").strip()
            print(decoded)
            if "eula" in decoded.lower():
                break
    finally:
        process.terminate()
        process.wait()
        print("
