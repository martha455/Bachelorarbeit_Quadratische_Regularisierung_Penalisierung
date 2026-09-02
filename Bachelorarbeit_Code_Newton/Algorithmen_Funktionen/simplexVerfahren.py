# Simplex-Loeser fuer das Transportproblem 

# Pakete
import time
import numpy as np
import ot

def simplexLoeser(mu, nu, c):
    """Berechnet eine Loesung fuer das Transportproblem durch einen Simplex Loeser."""

    pi = None
    log = {}

    ergebnisCode = None
    warnungMeldung = ""
    fehlerMeldung = "Keine Fehler"

    startZeit = time.perf_counter()

    # Ausfuehrung & Exceptions abfangen
    try:
        pi, log = ot.emd(mu, nu, c, log=True)
        ergebnisCode = log.get("result_code", None)
        warnungMeldung = log.get("warning", "")
    except Exception as fehler:
        fehlerMeldung = f"Python Fehler: {fehler}"

    endeZeit = time.perf_counter()

    # Solver-Status pruefen (Code 1 = Optimal in POT)
    istGueltig = (ergebnisCode == 1) or (warnungMeldung == "Problem solved")

    if not istGueltig and fehlerMeldung == "Keine Fehler":
        fehlerMeldung = f"C++ Solver: '{warnungMeldung}' (Code {ergebnisCode})"

    # Nur bei istGueltig gueltig, sonst NaN / None
    if istGueltig and pi is not None:
        zeilenFehler = np.linalg.norm(np.abs(pi.sum(axis=1) - mu), np.inf)
        spaltenFehler = np.linalg.norm(np.abs(pi.sum(axis=0) - nu), np.inf)
        marginalFehler = max(zeilenFehler, spaltenFehler)
        kosten = np.sum(pi * c)
        zeit = endeZeit - startZeit
    else:
        pi = None
        kosten = np.nan
        zeit = np.nan
        marginalFehler = np.nan

    return {
        "param": {"n": len(mu), "m": len(nu)},

        "transportPlan": pi,
        "kosten": kosten,

        "zeit": zeit,
        "marginalFehler": marginalFehler,

        "istGueltig": istGueltig,
        "fehlerMeldung": fehlerMeldung,
    }
