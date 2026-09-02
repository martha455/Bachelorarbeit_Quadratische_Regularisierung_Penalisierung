# Legt die globalen Einstellung fuer die Darstellung der Plots fuer alle Tests fest.

# Pakete für Plots
import matplotlib.pyplot as plt

from cycler import cycler # für die Farbpalette der Plots

# ---------- Globale Einstellungen ---------- 

# Schriftart bei matplotlib
plt.rcParams.update({

    "text.usetex": True,
    "font.family": "serif",
    "font.serif": ["Computer Modern Roman"],

    # "figure.figsize": (6,4),
    # "figure.dpi": 300,

    "axes.labelsize": 11,
    "font.size": 11,

    "legend.fontsize": 10,

    # "savefig.format": "pdf"
})

# Farbeinstellungen
COLORS = {
    "Peach":          (1.00, 0.50, 0.30),
    "CornflowerBlue": (0.35, 0.87, 1.00),
    "SeaGreen":       (0.31, 1.00, 0.50),
    "Plum":           (0.50, 0.00, 1.00),
    "Goldenrod":      (1.00, 0.90, 0.16),
    "RoyalBlue":      (0.00, 0.50, 1.00)
}

COLORS_LIGHT = {
    "Peach":          (1.00, 0.70, 0.58),
    "CornflowerBlue": (0.61, 0.922, 1.00),
    "SeaGreen":       (0.586, 1.00, 0.70),
    "Plum":           (0.70, 0.40, 1.00),
    "Goldenrod":      (1.00, 0.94, 0.496),
    "RoyalBlue":      (0.40, 0.70, 1.00)
}

plt.rcParams["axes.prop_cycle"] = cycler(color=COLORS.values()) # Legt die Standardfarben für die Plots fest