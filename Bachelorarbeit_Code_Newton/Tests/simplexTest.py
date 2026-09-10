# Testet den Simplex-Algorithmus für verschiedene Dimensionen 
# ---------- Imports - Pakete, Algorithmen und Hilfsfunktionen ---------- 

# Pakete für Pfad- und Dateiverwaltung
from Tests.pfadTestEinstellung import CSV_ORDNER, TEX_ORDNER, DIAGRAMM_ORDNER

# Algorithmen und Hilfsfunktionen
from Algorithmen_Funktionen.simplexVerfahren import simplexLoeser
from Algorithmen_Funktionen.DatenGenerieren import datenGenerierenZufall

from Algorithmen_Funktionen.Hilfsfunktionen import dfZuLatex

# Pakete für die Datenanalyse
import csv
import pandas as pd
from scipy import stats
import numpy as np
import math

# Darstellung der Plots
from Algorithmen_Funktionen.plotStilEinstellung import plt, COLORS, COLORS_LIGHT

# ---------- Simplex-Test ----------

def simplexTest(dimensionen, dateiname="Simplextest", numSeeds=10):
    """Fuehrt den Simplex-Test für verschiedene Dimensionen durch und speichert die Ergebnisse in einer CSV-Datei."""

    # Evtl. alte CSV-Datei loeschen
    dateipfad = CSV_ORDNER / f"{dateiname}.csv"
    if dateipfad.is_file():
        dateipfad.unlink()

    for n, m in dimensionen:
        for seed in range(numSeeds):

            mu, nu, c = datenGenerierenZufall(n,m,seed)

            ergebnisSimplex = simplexLoeser(mu, nu, c)

            sicherungSimplexTest(dateiname, seed, ergebnisSimplex)
    
    diagrammSimplexTest(dateiname)

#  ---------- Hilfsfunktionen ---------- 

def sicherungSimplexTest(dateiname, seed, ergebnisSimplex):
    """Speichert die Ergebnisse des Simplex-Tests in einer CSV-Datei."""

    dateipfad = CSV_ORDNER / f"{dateiname}.csv"
    dateiExistiert = dateipfad.is_file()

    with open(dateipfad, "a", newline="") as f:

        writer = csv.writer(f)

        if not dateiExistiert:
            writer.writerow([
                "Seed",
                "n",
                "m",
                "Zeit [s]",
                "Marginalfehler",
                "Kosten",
                "istGueltig",
            ])

        writer.writerow([
            seed,
            ergebnisSimplex["param"]["n"],
            ergebnisSimplex["param"]["m"],
            ergebnisSimplex["zeit"],
            ergebnisSimplex["marginalFehler"],
            ergebnisSimplex["kosten"],
            ergebnisSimplex["istGueltig"],
        ])

def diagrammSimplexTest(dateiname):
    """Erstellt Tabellen für den Simplex-Test und speichert sie als .tex-Dateien."""

    # ---- CSV-Datei einlesen ----
    df = pd.read_csv(CSV_ORDNER / f"{dateiname}.csv", sep=",", header=0)

    # Nur gueltige Zeilenberuecksichtigen
    df_gueltig = df[df["istGueltig"] == True]

    # Gruppierung nach n und m
    ergebnisse = []

    for (n, m), group in df.groupby(["n", "m"]):
        gueltige_gruppe = df_gueltig[(df_gueltig["n"] == n) & (df_gueltig["m"] == m)]
        
        # Anteil der gueltigen Durchlaeufe
        anteil_gueltig = len(gueltige_gruppe) / len(group) if len(group) > 0 else 0.0

        if len(gueltige_gruppe) > 0:
            zeit_val = stats.trim_mean(gueltige_gruppe["Zeit [s]"], 0.1)
            marg_val = stats.trim_mean(gueltige_gruppe["Marginalfehler"], 0.1)
            kost_val = stats.trim_mean(gueltige_gruppe["Kosten"], 0.1)
        else:
            # Falls keine gueltigen Daten vorhanden sind
            zeit_val = np.nan
            marg_val = np.nan
            kost_val = np.nan

        ergebnisse.append({
            "n": n,
            "m": m,
            "Gueltig_Anteil": anteil_gueltig,
            "Zeit [s]": zeit_val,
            "Marginalfehler": marg_val,
            "Kosten": kost_val
        })

    df_gruppiert = pd.DataFrame(ergebnisse).sort_values(["n", "m"]).reset_index(drop=True)

    df_latex = df_gruppiert.copy()

    df_latex["Gueltig_Anteil"] = df_latex["Gueltig_Anteil"].map(
        lambda x: f"{x * 100:.0f}\\%" if pd.notnull(x) else "0\\%"
    )

    # Nachkommastellen bearbeiten
    df_latex["Zeit [s]"] = df_latex["Zeit [s]"].map(
        lambda x: f"{x:.4e}" if pd.notnull(x) else ""
    )
    df_latex["Marginalfehler"] = df_latex["Marginalfehler"].map(
        lambda x: f"{x:.4e}" if pd.notnull(x) else ""
    )
    df_latex["Kosten"] = df_latex["Kosten"].map(
        lambda x: f"{x:.4e}" if pd.notnull(x) else ""
    )

    # Spaltennamen für LaTeX anpassen
    df_latex = df_latex.rename(columns={
        "Gueltig_Anteil": "Gültig",
        "Zeit [s]": "Laufzeit [s]",
        "Marginalfehler": "Marg.fehl."
    })

    caption = "Getrimmte Mittelwerte der Parameter des Simplex-Algorithmus gruppiert nach $n$ und $m$"

    dfZuLatex(df_latex, dateiname, caption)
