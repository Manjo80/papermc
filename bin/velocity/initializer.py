# velocity/initializer.py

import subprocess
import time
from pathlib import Path

def start_velocity_once(server_dir: Path):
    """
    Startet den Velocity-Server einmalig, um Konfigurationsdateien wie velocity.toml zu erzeugen.
    """
    print("➡️  Starte Velocity Server zum Erzeugen der Dateien...")
    process = subprocess.Popen(
        ["java", "-Xmx512M", "-Xms512M", "-jar", "velocity.jar"],
        cwd=server_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )

    try:
        for line in process.stdout:
            decoded = line.decode(errors="ignore").strip()
            print(decoded)
            if "Unable to read/load/save your velocity.toml" in decoded:
                break
    finally:
        time.sleep(10)  # Warten auf Dateierzeugung
        process.terminate()
        process.wait()
