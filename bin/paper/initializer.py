import subprocess
import time
from pathlib import Path

def start_server_once(server_dir: Path):
    print("➡️  Starte Server zum Erzeugen der Dateien...")
    process = subprocess.Popen(
        ["java", "-Xmx512M", "-Xms512M", "-jar", "paper.jar", "nogui"],
        cwd=server_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
    eula_seen = False
    for line in process.stdout:
        decoded = line.decode(errors="ignore").strip()
        print(decoded)
        if "eula" in decoded.lower():
            eula_seen = True
            break
    time.sleep(5)
    process.terminate()
    process.wait()
    if not eula_seen:
        raise RuntimeError("EULA-Meldung wurde nicht erkannt")

def apply_eula(server_dir: Path):
    print("➡️  Akzeptiere EULA...")
    with open(server_dir / "eula.txt", "w") as f:
        f.write("eula=true\n")

import subprocess
import time

def run_server_once(server_dir, seconds=30):
    print("➡️  Starte Server einmal vollständig zum Generieren aller Dateien...")
    process = subprocess.Popen(["java", "-Xmx512M", "-Xms512M", "-jar", "paper.jar", "nogui"],
                               cwd=server_dir, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    try:
        time.sleep(seconds)  # kurze Laufzeit reicht normalerweise, um alle Dateien zu erzeugen
    finally:
        process.terminate()
        process.wait()
        print("✅ Server wurde beendet.")

def run_server_until_generated(server_dir: Path, timeout: int = 60):
    print("➡️  Starte Server bis alle Konfigurationsdateien erstellt sind...")
    paper_global_path = server_dir / "config" / "paper-global.yml"

    process = subprocess.Popen(
        ["java", "-Xmx512M", "-Xms512M", "-jar", "paper.jar", "nogui"],
        cwd=server_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )

    start_time = time.time()
    try:
        while time.time() - start_time < timeout:
            if paper_global_path.exists():
                print("✅ paper-global.yml wurde erstellt.")
                break
            time.sleep(1)
        else:
            print("⚠️ Timeout erreicht – Datei wurde nicht gefunden, Server wird gestoppt.")
    finally:
        process.terminate()
        try:
            process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            process.kill()
            print("❌ Server musste hart beendet werden.")
        print("✅ Server gestoppt.")
