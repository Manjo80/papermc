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
