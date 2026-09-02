# Semiglattes Newton-Verfahren für das endliche Transportproblem mit quadratischer Regularisierung und Penalisierung

# Pakete
import numpy as np
import time
from scipy.sparse import block_array, csr_matrix, diags
from scipy.sparse.linalg import spsolve


# Aktive Menge bestimmen für die Berechnung von Phi
def aktiveMengen(alpha, beta, c):
    """Die Funktion bestimmt die aktiven Menge A_k der Funktion F."""

    Z = alpha[:, None] + beta[None, :] - c

    reihen, spalten = np.where(Z > 0)

    daten = np.ones(len(reihen))

    Phi = csr_matrix(
        (daten, (reihen, spalten)), shape=c.shape
    )  # Speicherung der aktiven Menge als sparse Matrix im csr-Format

    return Phi


# Berechnung der Funktion F(alpha, beta)
def F(alpha, beta, c, mu, nu, eps, gamma):
    """Berechnet fuer die gegebenen Parameter den Funktionswert von F"""

    g = np.maximum(alpha[:, None] + beta[None, :] - c, 0.0)

    F1 = g.sum(axis=1) / eps + gamma * alpha - mu
    F2 = g.sum(axis=0) / eps + gamma * beta - nu

    return np.concatenate(
        [F1, F2], axis=0
    )  # Aneinanderreihung der beiden Teile von F zu einem Vektor


# Berechnung der verallgemeinerten Jacobi-Matrix J(alpha, beta)
def allgemeineJacobi(alpha, beta, c, eps, gamma):
    """Berechnet die Newton Ableitung der Funktion F"""

    Phi = aktiveMengen(alpha, beta, c)

    reihenSumme = np.asarray(
        Phi.sum(axis=1)
    ).ravel()  # Summe der Eintraege in jeder Zeile von Phi

    spaltenSumme = np.asarray(
        Phi.sum(axis=0)
    ).ravel()  # Summe der Eintraege in jeder Spalte von Phi

    D_alpha = diags(
        gamma + reihenSumme / eps
    )  # Diagonalmatrix mit den Eintraegen gamma + row_sums / eps auf der Diagonalen

    D_beta = diags(
        gamma + spaltenSumme / eps
    )  # Diagonalmatrix mit den Eintraegen gamma + col_sums / eps auf der Diagonalen

    J = block_array(
        [[D_alpha, Phi / eps], [Phi.T / eps, D_beta]], format="csr"
    )  # Speicherung der verallgemeinerten Jacobi-Matrix als sparse Matrix im csr-Format

    return J


# Berechnung des Newton-Schritts
def newtonSchritt(alpha, beta, c, mu, nu, eps, gamma):
    """Loest die Newton Gleichung für gegebene Parameter"""

    negF = -F(alpha, beta, c, mu, nu, eps, gamma)

    J = allgemeineJacobi(alpha, beta, c, eps, gamma)

    d = spsolve(
        J, negF
    )  # Loesen des linearen Gleichungssystems J * d = -F(alpha, beta) für den Newton-Schritt d durch sparse solver für duennbesetzte Matrizen

    return d


def potentialF(alpha, beta, c, mu, nu, eps, gamma, Z_vorberechnet=None):
    """Berechnet das Potential der Funktion F fuer gegebene Parameter"""
    if Z_vorberechnet is None:
        Z_vorberechnet = alpha[:, None] + beta[None, :] - c

    # max(Z, 0)
    z = np.maximum(Z_vorberechnet, 0.0)

    return (
        1 / (2 * eps) * np.sum(z**2)
        + 0.5 * gamma * (np.dot(alpha, alpha) + np.dot(beta, beta))
        - np.dot(mu, alpha)
        - np.dot(nu, beta)
    )


# Semiglattes Newton-Verfahren
def semiglattesNewton(
    mu,
    nu,
    c,
    eps,
    gamma,
    alpha0=None,
    beta0=None,
    tol=1e-10,
    maxit=10000,
    min_schritt=1e-12,
    reduktionsfaktor=0.5,
):
    """Fuehrt den gesamten semiglatten Newtonalgorithmus aus und speichert in einer Container-Klasse die Daten für die Auswertung und Visualisierung der Ergebnisse.

    Args:
        mu: Vektor der Laenge n
        nu: Vektor der Laenge m
        c: Kostenmatrix (Matrix der Dimension nxm)
        eps: Skalar (positiv)
        gamma: Skalar (positiv)
        alpha0: Startvektor für alpha
        beta0: Startvektor für beta
        tol: Toleranz des Residuums als Abbruchbedingung. Defaults to 1e-10.
        maxit: maximale Anzahl der Iterationen. Defaults to 10000.
        min_schritt: minimale Schrittweite für Backtracking. Defaults to 1e-12.
        reduktionsfaktor: Reduktionsfaktor für Backtracking. Defaults to 0.5.

    Returns:
        Ergebnisobjekt der Container-Klasse
    """

    n = len(mu)
    m = len(nu)

    if alpha0 is None:
        alpha = np.zeros(n)
    else:
        alpha = alpha0.copy()
    if beta0 is None:
        beta = np.zeros(m)
    else:
        beta = beta0.copy()

    # Speicher für die Historie der Iterationen
    historie = {"FNorm": [], "iterationen": [], "Schrittweite": []}

    startZeit = time.perf_counter()

    zeta = 1e-4

    for k in range(maxit): 

        FWert = F(alpha, beta, c, mu, nu, eps, gamma)

        fehler = np.linalg.norm(
            FWert, np.inf
        )  # Berechnung der max-Norm von F(alpha, beta) zur Ueberpruefung der Konvergenz

        # speichern
        historie["FNorm"].append(fehler)
        historie["iterationen"].append(k)

        if (
            fehler < tol
        ):  # Abbruchbedingung: Wenn die Norm von F kleiner als die Toleranz ist
            break

        d = newtonSchritt(alpha, beta, c, mu, nu, eps, gamma)

        d_alpha = d[:n]
        d_beta = d[n:]

        G_alt = potentialF(alpha, beta, c, mu, nu, eps, gamma)

        richtungsableitung = np.dot(
            FWert, d
        )  # Newton-Richtung sollte eine Abstiegsrichtung sein

        if richtungsableitung >= 0:

            print(
                f"Newton-Richtung ist keine Abstiegsrichtung in Iteration {k}: F^T d = {richtungsableitung:.3e} "
            )

        schritt = 1.0

        akzeptiert = False

        A_vor = alpha[:, None] + beta[None, :] - c
        D_vor = d_alpha[:, None] + d_beta[None, :]

        while schritt >= min_schritt: # Armijo-Schrittweitensuche

            Z_trial = A_vor + schritt * D_vor

            alpha_trial = alpha + schritt * d_alpha

            beta_trial = beta + schritt * d_beta

            G_trial = potentialF(
                alpha_trial, beta_trial, c, mu, nu, eps, gamma, Z_vorberechnet=Z_trial
            )

            if G_trial <= (G_alt + zeta * schritt * richtungsableitung):

                alpha = alpha_trial

                beta = beta_trial

                historie["Schrittweite"].append(schritt)

                akzeptiert = True

                break
            
            schritt *= reduktionsfaktor

        # Falls keine Schrittweite akzeptiert wird

        if not akzeptiert:

            historie["Schrittweite"].append(np.nan)

            break

    endeZeit = time.perf_counter()

    pi = transportPlan(alpha, beta, c, eps)  # Berechnung des Transportplans

    # Ergebnisobjekt
    ergebnis = {
        "alpha": alpha,
        "beta": beta,
        "transportPlan": pi,
        "kosten": transportKosten(pi, c),
        "iterationen": len(historie["FNorm"]),
        "zeit": endeZeit - startZeit,
        "letztesResiduum": historie["FNorm"][-1],
        "historie": historie,
        "finalerMarginalfehler": max(
            np.abs(pi.sum(axis=1) - mu).max(),
            np.abs(pi.sum(axis=0) - nu).max(),
        ),
        "param": {"eps": eps, "gamma": gamma, "n": len(alpha), "m": len(beta)},
    }

    return ergebnis


# Berechnung des konkreten Transportplans aus alpha und beta
def transportPlan(alpha, beta, c, eps):
    """Berechnet den Transportplan fuer gegebene Parameter
    """

    return np.maximum(alpha[:, None] + beta[None, :] - c, 0.0) / eps


# Berechnung der Kosten des Transportplans
def transportKosten(pi, c):
    """Berechnet die Kosten fuer gegebenen Transportplan
    """
    # Forbeniusskalarprodukt der Transportmatrix pi und der Kostenmatrix c:
    return np.sum(pi * c)
