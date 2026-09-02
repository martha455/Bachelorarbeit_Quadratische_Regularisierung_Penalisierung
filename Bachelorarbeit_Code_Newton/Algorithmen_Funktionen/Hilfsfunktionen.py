# ---------- Imports - Pakete, Algorithmen und Hilfsfunktionen ---------- 

# Pakete für Pfad- und Dateiverwaltung
from Tests.pfadTestEinstellung import TEX_ORDNER

# Pakete für die Datenanalyse
import numpy as np

# ---------- Hilfsfunktionen ----------

def dfZuLatex(df, dateiname, caption):

    # ---- LaTeX-Code erzeugen ----
    latex_code = df.to_latex(
        index=False,
        escape=False,
        column_format="r" * len(df.columns),
        caption=caption,
        label="tab:" + dateiname
    )

    # ---- Umformatieren ----
    latex_code = latex_code.replace(
        r"\begin{table}",
        r"\begin{table}[htbp]"
    )

    latex_code = latex_code.replace(
        r"\begin{tabular}",
        r"\small" + "\n" 
        r"\centering" + "\n" +
        r"\rowcolors{2}{gray!10}{white}" + "\n" +
        r"\begin{tabular}"
    )

    # ---- Datei speichern ----
    with open(
        TEX_ORDNER / f"{dateiname}.tex",
        "w",
        encoding="utf-8"
    ) as f:
        f.write(latex_code)