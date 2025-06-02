#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.append("/opt/papermc/bin")

from paperserver.download_paper import download_latest_paper

server_dir = Path.cwd()

print("🔍 Prüfe auf neues PaperMC-Update...")
try:
    download_latest_paper(server_dir)
    print("✅ PaperMC-Update abgeschlossen.")
except Exception as e:
    print(f"❌ Fehler beim Update: {e}")
