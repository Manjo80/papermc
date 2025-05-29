# velocity/downloader.py

import requests
from pathlib import Path

def download_latest_velocity(target_dir: Path) -> Path:
    print("➡️  Lade neueste Velocity-Version herunter...")
    jar_url = (
        "https://api.papermc.io/v2/projects/velocity/versions/3.4.0-SNAPSHOT/"
        "builds/509/downloads/velocity-3.4.0-SNAPSHOT-509.jar"
    )
    jar_path = target_dir / "velocity.jar"
    
    response = requests.get(jar_url, stream=True)
    response.raise_for_status()

    with open(jar_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    
    return jar_path
