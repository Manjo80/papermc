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
