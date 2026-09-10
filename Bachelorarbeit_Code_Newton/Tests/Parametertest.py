# Ziel des Parametertests ist es, die Auswirkungen der Parameter epsilon und gamma auf die Konvergenzgeschwindigkeit und die Genauigkeit des semiglattes Newton-Verfahrens zu untersuchen

# ---------- Imports - Pakete, Algorithmen und Hilfsfunktionen ---------- 

# Pakete für Pfad- und Dateiverwaltung
from Tests.pfadTestEinstellung import CSV_ORDNER, DIAGRAMM_ORDNER

# Algorithmen und Hilfsfunktionen
from Algorithmen_Funktionen.semiglattesNewtonVerfahren import semiglattesNewton
from Algorithmen_Funktionen.DatenGenerieren import datenGenerierenZufall
from Algorithmen_Funktionen.simplexVerfahren import simplexLoeser

from Algorithmen_Funktionen.Hilfsfunktionen import dfZuLatex

# Pakete für die Datenanalyse
import csv
import pandas as pd
from scipy import stats
import numpy as np

# Darstellung der Plots
from Algorithmen_Funktionen.plotStilEinstellung import plt, COLORS, COLORS_LIGHT

# Parametertest

def parameterTest(n, m,  epsWerte, gammaWerte, dateiname="Parametertest",numSeeds=10, tol=1e-10, maxit=10000, reduktionsfaktor=0.5, min_schritt=1e-12,alpha0 = None, beta0 =None):
    """Fuehrt den Parametertest für das semiglatte Newtonverfahren durch und speichert die Ergebnisse in einer CSV-Datei."""

    # Evtl. alte CSV-Datei loeschen
    dateipfad = CSV_ORDNER / f"{dateiname}.csv"
    if dateipfad.is_file():
        dateipfad.unlink()

    for eps in epsWerte:
        for gamma in gammaWerte:
            for seed in range(numSeeds):

                mu, nu, c = datenGenerierenZufall(n,m,seed)
                ergebnisNewton = semiglattesNewton(mu,nu,c,eps,gamma, alpha0 = alpha0, beta0 = beta0, tol = tol, maxit = maxit, reduktionsfaktor = reduktionsfaktor, min_schritt = min_schritt)
                ergebnisSimplex = simplexLoeser(mu,nu,c)
                sicherungParameterTest(dateiname, seed, ergebnisNewton, ergebnisSimplex)
    
    diagrammParameterTest(dateiname)

#  ---------- Hilfsfunktionen ---------- 

def sicherungParameterTest(dateiname, seed, ergebnisNewton, ergebnisSimplex):
    """Speichert die Ergebnisse des Parametertests in einer CSV-Datei."""

    dateipfad = CSV_ORDNER / f"{dateiname}.csv"
    dateiExistiert = dateipfad.is_file()

    with open(dateipfad, "a", newline="") as f:

        writer = csv.writer(f)

        if not dateiExistiert:
            writer.writerow([
                "Seed",
                "n",
                "m",
                "eps",
                "gamma",
                "Iterationen",
                "Zeit [s]",
                "Marginalfehler",
                "Kostendifferenz",
                "Kosten Newton",
                "Kosten Simplex",
            ])

        if np.isclose(ergebnisSimplex["kosten"], 0):
            relativeKostendifferenz = np.nan
        else:
            relativeKostendifferenz = (
                            (abs(ergebnisNewton["kosten"] - ergebnisSimplex["kosten"]))/ abs(ergebnisSimplex["kosten"])
                        )
    

        writer.writerow([
            seed,
            ergebnisNewton["param"]["n"],
            ergebnisNewton["param"]["m"],
            ergebnisNewton["param"]["eps"],
            ergebnisNewton["param"]["gamma"],
            ergebnisNewton["iterationen"],
            ergebnisNewton["zeit"],
            ergebnisNewton["finalerMarginalfehler"],
            abs(ergebnisNewton["kosten"] - ergebnisSimplex["kosten"]),
            ergebnisNewton["kosten"],
            ergebnisSimplex["kosten"]
        ])

def diagrammParameterTest(dateiname):
    """Erstellt Tabellen für den Parametertest und speichert sie als .tex-Dateien."""

    # CSV-Datei
    df = pd.read_csv(CSV_ORDNER / f"{dateiname}.csv", sep=',', header=0)

    # Gruppierung der Daten nach eps und gamma, Berechnung des getrimmten Mittelwerts pro Spalte
    werte = df.columns[5:10].tolist()
    
    df_gruppiert = df.groupby(["eps", "gamma"], as_index=False)[werte].agg(lambda x: stats.trim_mean(x.dropna(), 0.1)).sort_values(["gamma", "eps"]).reset_index(drop=True)

    df_latex = df_gruppiert.copy()

    # Darstellung in Zehnerpotenzen
    df_latex["eps"] = df_latex["eps"].apply(lambda x: np.format_float_scientific(x))
    df_latex["gamma"] = df_latex["gamma"].apply(lambda x: np.format_float_scientific(x))

    # Nachkommastellen bearbeiten
    df_latex["Iterationen"] = df_latex["Iterationen"].map(lambda x: f"{x:.2f}" if pd.notnull(x) else "nan")

    # Nachkommastellen bearbeiten
    df_latex["Zeit [s]"] = df_latex["Zeit [s]"].map(lambda x: f"{x:.4e}" if pd.notnull(x) else "nan")
    df_latex["Marginalfehler"] = df_latex["Marginalfehler"].map(lambda x: f"{x:.4e}" if pd.notnull(x) else "nan")
    df_latex["Kostendifferenz"] = df_latex["Kostendifferenz"].map(lambda x: f"{x:.4e}" if pd.notnull(x) else "nan")
    df_latex["Kosten Newton"] = df_latex["Kosten Newton"].map(lambda x: f"{x:.4e}" if pd.notnull(x) else "nan")

    # Spaltennamen anpassen
    df_latex = df_latex.rename(
        columns={"eps": r"$\varepsilon$","gamma": r"$\gamma$",}
    )

    caption="Getrimmte Mittelwerte der Daten in Abhängigkeit von $\\varepsilon$ und $\\gamma$"
    
    dfZuLatex(df_latex, dateiname, caption)
