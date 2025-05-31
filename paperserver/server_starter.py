# paperserver/server_starter.py
import subprocess
from pathlib import Path

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
        print("✅ Server gestoppt nach EULA-Erkennung")
