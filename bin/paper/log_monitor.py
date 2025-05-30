# paper/log_monitor.py

from pathlib import Path

def monitor_log_for_warnings(server_dir: Path):
    print("➡️  Überwache Logs auf Fehler oder Warnungen...")
    log_file = server_dir / "logs" / "latest.log"
    if log_file.exists():
        with open(log_file, "r") as f:
            for line in f:
                if any(w in line for w in ["[ERROR]", "[WARN]"]):
                    print(line.strip())

def wait_for_log_message(log_path: Path, message: str, timeout: int = 30):
    import time
    print(f"➡️ Warte auf Log-Meldung: {message}")
    start = time.time()
    while time.time() - start < timeout:
        if not log_path.exists():
            time.sleep(1)
            continue
        with open(log_path) as f:
            if any(message in line for line in f):
                print("✅ Meldung gefunden.")
                return
        time.sleep(1)
    raise TimeoutError(f"❌ Meldung '{message}' wurde nicht gefunden.")
