# config.py

from pathlib import Path

def accept_eula(server_dir: Path):
    """Setzt die EULA auf true."""
    eula_path = server_dir / "eula.txt"
    if not eula_path.exists():
        print("❌ eula.txt nicht gefunden.")
        return

    try:
        with open(eula_path, "w") as f:
            f.write("eula=true\n")
        print("✅ EULA akzeptiert.")
    except Exception as e:
        print(f"❌ Fehler beim Schreiben der eula.txt: {e}")
