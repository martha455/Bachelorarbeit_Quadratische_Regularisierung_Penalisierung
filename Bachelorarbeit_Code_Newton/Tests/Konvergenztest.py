# Testet die Konvergenz des semiglattes Newton-Verfahrens für verschiedene Dimensionen und Parameter.
# ---------- Imports - Pakete, Algorithmen und Hilfsfunktionen ---------- 

# Pakete für Pfad- und Dateiverwaltung
from Tests.pfadTestEinstellung import CSV_ORDNER, TEX_ORDNER, DIAGRAMM_ORDNER

# Algorithmen und Hilfsfunktionen
from Algorithmen_Funktionen.semiglattesNewtonVerfahren import semiglattesNewton
from Algorithmen_Funktionen.DatenGenerieren import datenGenerierenZufall

from Algorithmen_Funktionen.Hilfsfunktionen import dfZuLatex

# Pakete für die Datenanalyse
import csv
import pandas as pd
from scipy import stats
import numpy as np

# Darstellung der Plots
from Algorithmen_Funktionen.plotStilEinstellung import plt, COLORS, COLORS_LIGHT

# Konvergenztest

def konvergenzTest(dimensionen, parameter, dateiname = "Konvergenztest", alpha0 = None, beta0 =None, numSeeds=10, tol=1e-10, maxit=10000, reduktionsfaktor=0.5, min_schritt=1e-12):
    """Fuehrt den Konvergenztest für das semiglatte Newtonverfahren durch und speichert die Ergebnisse in einer CSV-Datei."""

    # Evtl. alte CSV-Datei löschen
    dateipfad = CSV_ORDNER / f"{dateiname}.csv"
    if dateipfad.is_file():
        dateipfad.unlink()

    for (n,m), (eps, gamma) in zip(dimensionen, parameter):
        for seed in range(numSeeds):
            mu, nu, c = datenGenerierenZufall(n,m,seed)
            ergebnisNewton = semiglattesNewton(mu,nu,c,eps,gamma, alpha0 = alpha0, beta0 = beta0, tol = tol, maxit = maxit, reduktionsfaktor = reduktionsfaktor, min_schritt = min_schritt)
            sicherungKonvergenzTest(dateiname, seed, ergebnisNewton)
    diagrammKonvergenzTestEinzel(dateiname)


#  ---------- Hilfsfunktionen ---------- 

def sicherungKonvergenzTest(dateiname, seed, ergebnisNewton):
    """Speichert die Ergebnisse des Konvergenztests in einer CSV-Datei."""
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
                "Iteration",
                "Residuum",
                "Schrittweite",
                "Quotient"
            ])

        historie = ergebnisNewton["historie"]
        residuuen = historie["FNorm"]
        n_iter = len(residuuen)

        # Zeilenweise Speicherung für jede Iteration k
        for k in range(n_iter):
            # Für die letzte Iteration gibt es keine Schrittweite, daher setzen wir sie auf NaN
            schritt = historie["Schrittweite"][k] if k < len(historie["Schrittweite"]) else np.nan

            if k == 0 or residuuen[k-1] == 0:
                quotient = np.nan
            else:
                quotient = residuuen[k] / residuuen[k-1]

            writer.writerow([
                seed,
                ergebnisNewton["param"]["n"],
                ergebnisNewton["param"]["m"],
                ergebnisNewton["param"]["eps"],
                ergebnisNewton["param"]["gamma"],
                k,
                residuuen[k],
                schritt,
                quotient
            ])

def diagrammKonvergenzTestEinzel(dateiname):
    """Erstellt Diagramme für den Konvergenztest und speichert sie als PDF-Dateien."""

    # CSV-Datei einlesen
    df = pd.read_csv(CSV_ORDNER / f"{dateiname}.csv", sep=',', header=0)

    seed_laufzeiten = (
        df.groupby(["n", "m", "eps", "gamma", "Seed"])["Iteration"]
        .max()
        .reset_index()
        .rename(columns={"Iteration": "max_k"})
    )

    # Die 5 schnellsten Seeds behalten
    schnellste_seeds_liste = []

    for (n, m, eps, gamma), df_gruppe in seed_laufzeiten.groupby(["n", "m", "eps", "gamma"]):
        df_gruppe_sortiert = df_gruppe.sort_values("max_k")
        schnelle_seeds = df_gruppe_sortiert.head(5)
        schnellste_seeds_liste.append(schnelle_seeds)

    df_gueltige_seeds = pd.concat(schnellste_seeds_liste, ignore_index=True)

    df_gefiltert = pd.merge(
        df, 
        df_gueltige_seeds[["n", "m", "eps", "gamma", "Seed"]], 
        on=["n", "m", "eps", "gamma", "Seed"], 
        how="inner"
    )

    farben_liste = list(COLORS.values())

    for (n, m), df_dim in df_gefiltert.groupby(["n", "m"]):
        
        fig, axes = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

        einzellaeufe = df_dim[["eps", "gamma", "Seed"]].drop_duplicates().reset_index(drop=True)

        ax_res = axes[0]
        ax_schritt = axes[1]

        # Einzelne Laeufe plotten
        for idx, row in einzellaeufe.iterrows():
            eps, gamma, seed = row["eps"], row["gamma"], row["Seed"]
            
            df_lauf = df_dim[
                (df_dim["eps"] == eps) & 
                (df_dim["gamma"] == gamma) & 
                (df_dim["Seed"] == seed)
            ].sort_values("Iteration")

            farbe = farben_liste[idx % len(farben_liste)]
            label_text = fr"Seed {int(seed)} ($\varepsilon={eps}, \gamma={gamma}$)"

            # 1. Subplot: Residuum
            ax_res.plot(
                df_lauf["Iteration"],
                df_lauf["Residuum"],
                marker='o',
                markersize=3,
                label=label_text,
                linewidth=1.2,
                color=farbe
            )

            # 2. Subplot: Schrittweite
            df_schritt = df_lauf.dropna(subset=["Schrittweite"])
            ax_schritt.plot(
                df_schritt["Iteration"],
                df_schritt["Schrittweite"],
                marker='s',
                markersize=3,
                label=label_text,
                linewidth=1.2,
                color=farbe
            )

        # Layout Subplot 1
        ax_res.set_yscale("log")
        ax_res.set_ylabel(r"Residuum $\|F(\alpha_k, \beta_k)\|_\infty$", fontsize=15)
        ax_res.set_title(fr"Konvergenzverlauf ($n={int(n)}, m={int(m)}$)", fontsize=15)
        ax_res.grid(True, which="both", alpha=0.35)

        # Layout Subplot 2
        ax_schritt.set_xlabel("Iteration $k$", fontsize=15)
        ax_schritt.set_ylabel(r"Schrittweite $\sigma_k$", fontsize=15)
        ax_schritt.set_title(fr"Schrittweitenverlauf ($n={int(n)}, m={int(m)}$)", fontsize=15)
        ax_schritt.grid(True, which="both", alpha=0.35)

        fig.tight_layout()
        
        # PDF pro Dimensionenpaar speichern
        pdf_dateiname = DIAGRAMM_ORDNER / f"{dateiname}_n{int(n)}_m{int(m)}.pdf"
        fig.savefig(pdf_dateiname, bbox_inches="tight")
        plt.close(fig)
