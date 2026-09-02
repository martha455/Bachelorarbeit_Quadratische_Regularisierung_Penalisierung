# Daten generieren fuer das Transportproblem

# Pakete
import numpy as np

def datenGenerierenEinfach(n, m):
    """Generiert eine Kostenmatrix und "einfache" Marginale fuer gegebene Dimensionen 
    """
    # Generiere Kostenmatrix fuer die paarweisen Abstaende von Indizes
    x = np.linspace(1, n, n)    
    y = np.linspace(1, m, m)
    c = np.abs(x[:, None] - y[None, :])

    # Generiere einfache Marginale
    mu = np.ones(n) / n
    nu = np.ones(m) / m

    return mu, nu, c

def datenGenerierenZufall(n, m, seed=None):
    """Generiert eine Kostenmatrix und "zufaellige" Marginale fuer gegebene Dimensionen 
    """
    if seed is not None:
        np.random.seed(seed)

    # Generiere Kostenmatrix für die paarweisen Abstaende von Indizes
    x = np.linspace(1, n, n)    
    y = np.linspace(1, m, m)
    c = np.abs(x[:, None] - y[None, :])

    # Generiere zufaellige Marginale
    mu = np.random.rand(n)
    mu /= mu.sum()  

    nu = np.random.rand(m)
    nu /= nu.sum()  

    return mu, nu, c