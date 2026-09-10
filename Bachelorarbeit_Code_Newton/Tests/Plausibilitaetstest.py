# Erster Test, um die Plausibilitaet des semiglatten Newtonverfahrens zu ueberpruefen.
# Vergleicht die Ergebnisse des semiglatten Newtonverfahrens mit den Ergebnissen des Simplexverfahrens für verschiedene Dimensionen und Parameterwerte.
# ---------- Imports - Pakete, Algorithmen und Hilfsfunktionen ---------- 

# Pakete für Pfad- und Dateiverwaltung
from Tests.pfadTestEinstellung import CSV_ORDNER, DIAGRAMM_ORDNER

# Algorithmen und Hilfsfunktionen
from Algorithmen_Funktionen.semiglattesNewtonVerfahren import semiglattesNewton
from Algorithmen_Funktionen.DatenGenerieren import datenGenerierenEinfach
from Algorithmen_Funktionen.simplexVerfahren import simplexLoeser

from Algorithmen_Funktionen.Hilfsfunktionen import dfZuLatex

# Pakete für die Datenanalyse
import csv
import pandas as pd
from scipy import stats
import numpy as np

# Darstellung der Plots
from Algorithmen_Funktionen.plotStilEinstellung import plt, COLORS, COLORS_LIGHT

# Plausibilitaetstest
def plausibilitaetsTest(dimWerte = [(10, 10)], paramWerte = [(1, 1)], dateiname = "Plausibilitaetstest", tol=1e-10, maxit=10000, alpha0 = None, beta0 =None):
    """Fuehrt den Plausibilitaetstest für das semiglatte Newtonverfahren durch und speichert die Ergebnisse in einer CSV-Datei."""

    # Evtl. alte CSV-Datei loeschen
    dateipfad = CSV_ORDNER / f"{dateiname}.csv"
    if dateipfad.is_file():
        dateipfad.unlink()

    for (n, m), (eps, gamma) in zip(dimWerte, paramWerte):

        mu, nu, c = datenGenerierenEinfach(n,m)

        ergebnisNewton = semiglattesNewton(mu,nu,c,eps, gamma, tol = tol, maxit = maxit, alpha0 = alpha0, beta0 = beta0)
        ergebnisSimplex = simplexLoeser(mu,nu,c)

        sicherungPlausibilitaetsTest(dateiname, ergebnisNewton, ergebnisSimplex)

        # Zeige bei Matrixausgaben alle Nachkommastellen an
        np.set_printoptions(
            suppress=False,
            precision=15,
            formatter={'float_kind': lambda x: f"{x:.15f}"}
        )

        print("Newton für " + f"{n}, {m}" + ":" + "\n")
        print(ergebnisNewton["transportPlan"])

        print("Simplex für " + f"{n}, {m}" + ":" + "\n")
        print(ergebnisSimplex["transportPlan"])


    latexPlausibilitaetstest(dateiname)

def sicherungPlausibilitaetsTest(dateiname, ergebnisNewton, ergebnisSimplex):
    """Speichert die Ergebnisse des Plausibilitaetstests in einer CSV-Datei."""

    dateipfad = CSV_ORDNER / f"{dateiname}.csv"
    dateiExistiert = dateipfad.is_file()

    with open(dateipfad, "a", newline="") as f:

        writer = csv.writer(f)

        if not dateiExistiert:
            writer.writerow([
                "eps",
                "gamma",
                "n",
                "m",
                "Kostendifferenz",
                "Marginalfehler"
            ])

        writer.writerow([
            ergebnisNewton["param"]["eps"],
            ergebnisNewton["param"]["gamma"],
            ergebnisNewton["param"]["n"],
            ergebnisNewton["param"]["m"],
            abs(ergebnisNewton["kosten"] - ergebnisSimplex["kosten"]),
            ergebnisNewton["finalerMarginalfehler"]
        ])

def latexPlausibilitaetstest(dateiname):
    """Erstellt eine LaTeX-Tabelle für den Plausibilitaetstest und speichert sie als .tex-Datei."""

    # ---- CSV-Datei ----
    df_latex = pd.read_csv(CSV_ORDNER / f"{dateiname}.csv", sep=',', header=0)

    # ---- Sicherung der Tabelle als .tex Datei ----
    
    # Darstellung in Zehnerpotenzen
    df_latex["eps"] = df_latex["eps"].apply(lambda x: np.format_float_scientific(x))
    df_latex["gamma"] = df_latex["gamma"].apply(lambda x: np.format_float_scientific(x))

    # Nachkommastellen bearbeiten
    df_latex["Kostendifferenz"] = df_latex["Kostendifferenz"].map(lambda x: f"{x:.4e}" if pd.notnull(x) else "nan")
    df_latex["Marginalfehler"] = df_latex["Marginalfehler"].map(lambda x: f"{x:.4e}" if pd.notnull(x) else "nan")

    # Spaltennamen anpassen
    df_latex = df_latex.rename(columns={"eps": r"$\varepsilon$"})
    df_latex = df_latex.rename(columns={"gamma": r"$\gamma$"})

    caption="Ergebnis des Plausibilitätstests"

    dfZuLatex(df_latex, dateiname, caption)
