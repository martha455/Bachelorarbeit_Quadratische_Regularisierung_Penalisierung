# Quadratische Regularisierung und Penalisierung des Hitchcock-Problems — Semiglattes Newton-Verfahren

Dieses Repository enthält den Quellcode sowie die Skripte zur Generierung der numerischen Testergebnisse der Bachelorarbeit von **Martha Winning** an der Technischen Universität Dortmund (Fakultät für Mathematik, Lehrstuhl für Numerische Analysis und Optimierung, Sommersemester 2026).

---

## Übersicht

Das Hauptziel dieser Arbeit ist die theoretische Untersuchung und praktische Evaluierung eines **semiglatten Newton-Verfahrens** für das quadratisch regularisierte und penalisierte Hitchcock-Problem (endliches Transportproblem). Zur Einordnung der Leistung, Laufzeit und Genauigkeit wird das Verfahren empirisch mit zwei etablierten Algorithmen verglichen:
- **Sinkhorn-Algorithmus** (entropische Regularisierung)
- **Simplex-Algorithmus** (exaktes Verfahren via *Python Optimal Transport*, POT)

---

## Projektstruktur

Das Projekt ist grob in drei Bereiche aufgeteilt. Der Ordner Algorithmen_Funktionen enthält die Implementierungen der verschiedenen Lösungsverfahren, sowie die Datengenerierung. Der Ordner Tests enthält die verschiedenen Skripte zur Ausführung der numerischen Experimente und Ergebnisse speichert diese in CSV, PDF oder TEX Dateien. Mit dem Ausführen der main.py Methode können alle numerische Experimente aufgerufen werden.

## Systemanforderungen & Installation

Der Code wurde unter **Python 3.14** entwickelt und getestet.

### Benötigte Bibliotheken
Die externen Abhängigkeiten und deren Verwendungszweck im Projekt:

- **`numpy`**: Datenverwaltung, Vektorarithmetik und Erzeugung stochastischer Testdaten
- **`scipy`**: Effiziente Verwaltung dünnbesetzter Matrizen (`csr_matrix`, `block_array`) und Lösen des Newton-Schrittes (`spsolve`)
- **`POT`** (Python Optimal Transport, `import ot`): Vergleichsmessungen mit dem Simplex-Algorithmus
- **`pandas`**: Strukturierte Auswertung und Export der Messergebnisse
- **`matplotlib`**: Erstellung und Anpassung der Plot-Visualisierungen

*(Hinweis: Weitere genutzte Module wie `time`, `sys`, `csv`, `math` und `cycler` sind Bestandteil der Python-Standardbibliothek.)*

### Ein-Klick-Installation
Sämtliche benötigten Pakete können über den folgenden Befehl installiert werden:

```bash
pip install numpy scipy POT pandas matplotlib
