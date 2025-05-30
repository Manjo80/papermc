from configparser import ConfigParser
from pathlib import Path

def load_config(section: str = "DEFAULT") -> dict:
    """
    Lädt Konfigurationswerte aus global.conf, bereinigt Schlüssel und wandelt Werte
    ins korrekte TOML-Format:
    - Entfernt "default_"
    - ersetzt "_" durch "-"
    - alles klein geschrieben
    - Strings mit Anführungszeichen, außer reine Zahlen, true/false
    """
    config_path = Path(__file__).resolve().parents[2] / "config" / "global.conf"
    parser = ConfigParser()
    parser.optionxform = str  # Case beibehalten
    parser.read(config_path)

    if section not in parser:
        raise ValueError(f"Sektion [{section}] nicht gefunden in {config_path}")

    raw_config = parser[section]
    final_config = {}

    for key, value in raw_config.items():
        # Schlüssel bereinigen
        clean_key = key.lower().replace("default_", "").replace("_", "-")
        val = value.strip()

        # Werttyp prüfen und ggf. quoten
        if val.lower() in ["true", "false"]:
            final_val = val.lower()
        elif val.isdigit():
            final_val = val
        else:
            try:
                float(val)
                final_val = val  # Float bleibt unverändert
            except ValueError:
                final_val = f'"{val}"'  # String quoten

        final_config[clean_key] = final_val

    return final_config
