# velocity/initializer.py

import subprocess
import time
from pathlib import Path

def start_velocity_once(server_dir: Path, timeout: int = 60):
    """
    Startet den Velocity-Server und wartet, bis sowohl velocity.toml als auch forwarding.secret erstellt wurden.
    """
    print("➡️  Starte Velocity Server bis Konfigurationsdateien erstellt sind...")

    velocity_toml = server_dir / "velocity.toml"
    forwarding_secret = server_dir / "forwarding.secret"

    process = subprocess.Popen(
        ["java", "-Xmx512M", "-Xms512M", "-jar", "velocity.jar"],
        cwd=server_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )

    start_time = time.time()
    try:
        while time.time() - start_time < timeout:
            if velocity_toml.exists() and forwarding_secret.exists():
                print("✅ velocity.toml und forwarding.secret wurden erstellt.")
                break
            time.sleep(1)
        else:
            print("⚠️ Timeout erreicht – Dateien wurden nicht gefunden, Server wird gestoppt.")
    finally:
        process.terminate()
        try:
            process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            process.kill()
            print("❌ Server musste hart beendet werden.")
        print("✅ Server gestoppt.")
