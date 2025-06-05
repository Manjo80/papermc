# bin/remote_inst/logger.py

from pathlib import Path
from datetime import datetime

def write_info_file(server_name, data):
    info_dir = Path("/opt/minecraft")
    info_dir.mkdir(parents=True, exist_ok=True)
    info_file = info_dir / f"remote_{server_name}.info"
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(info_file, "w") as f:
        f.write(f"Installationsdatum: {now}\n")
        for k, v in data.items():
            f.write(f"{k}: {v}\n")
    print(f"ℹ️ Info-Datei geschrieben: {info_file}")
