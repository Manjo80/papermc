# paperserver/server_starter.py
import subprocess
import time
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

def start_until_configs_generated(server_path: Path, timeout: int = 60):
    print("➡️ Starte Server bis Konfigurationsdateien erzeugt wurden...")
    spigot_yml = server_path / "spigot.yml"
    paper_global_yml = server_path / "config" / "paper-global.yml"

    process = subprocess.Popen(
        ["java", "-Xmx512M", "-Xms512M", "-jar", "paper.jar", "nogui"],
        cwd=server_path,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )

    start_time = time.time()
    try:
        while time.time() - start_time < timeout:
            if spigot_yml.exists() and paper_global_yml.exists():
                print("✅ Konfigurationsdateien wurden erstellt.")
                break
            time.sleep(1)
        else:
            print("⚠️ Timeout: Dateien wurden nicht erstellt.")
    finally:
        process.terminate()
        try:
            process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            process.kill()
            print("❌ Server musste hart beendet werden.")
        print("🛑 Server gestoppt.")
