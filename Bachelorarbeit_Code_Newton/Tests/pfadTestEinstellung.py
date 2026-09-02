# Legt den Elternordner des Projekts fest und fuegt ihn dem Systempfad fuer Zugriff im Projekt hinzu

# Paket für Pfad- und Dateiverwaltung
from pathlib import Path
import sys

# ---------- Pfadeinstellungen ----------

PROJEKTORDNER = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJEKTORDNER))

# Ordner fuer die Ergebnisse
CSV_ORDNER = PROJEKTORDNER / "Ergebnisse" / "CSV"
TEX_ORDNER = PROJEKTORDNER / "Ergebnisse" / "Tex"
DIAGRAMM_ORDNER = PROJEKTORDNER / "Ergebnisse" / "Diagramme"