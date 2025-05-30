# paper/downloader.py

import requests
from pathlib import Path

def download_latest_paper(target_dir: Path) -> Path:
    print("➡️  Lade neueste PaperMC-Version herunter...")

    try:
        # Hole neueste Minecraft-Version
        versions_response = requests.get("https://api.papermc.io/v2/projects/paper")
        versions_response.raise_for_status()
        latest_version = versions_response.json()["versions"][-1]

        # Hole neuesten Build für diese Version
        builds_response = requests.get(f"https://api.papermc.io/v2/projects/paper/versions/{latest_version}")
        builds_response.raise_for_status()
        latest_build = builds_response.json()["builds"][-1]

        # Konstruiere Download-URL und Zielpfad
        jar_name = f"paper-{latest_version}-{latest_build}.jar"
        jar_url = f"https://api.papermc.io/v2/projects/paper/versions/{latest_version}/builds/{latest_build}/downloads/{jar_name}"
        jar_path = target_dir / "paper.jar"

        # Lade Datei herunter
        with requests.get(jar_url, stream=True) as r:
            r.raise_for_status()
            with open(jar_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

        print(f"✅ PaperMC heruntergeladen: {jar_path.name}")
        return jar_path

    except Exception as e:
        print(f"❌ Fehler beim Herunterladen von PaperMC: {e}")
        raise
