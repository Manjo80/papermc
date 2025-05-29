import requests
from pathlib import Path

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

    return jar_path
