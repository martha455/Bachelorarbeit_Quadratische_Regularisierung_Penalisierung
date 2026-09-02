# Quadratische Regularisierung und Penalisierung des Hitchcock-Problems — Semiglattes Newton-Verfahren

Dieses Repository enthält den Quellcode sowie die Skripte zur Generierung der numerischen Testergebnisse der Bachelorarbeit von **Martha Winning** an der Technischen Universität Dortmund (Fakultät für Mathematik, Lehrstuhl für Numerische Analysis und Optimierung, Sommersemester 2026).

---

## Übersicht

Das Hauptziel dieser Arbeit ist die theoretische Untersuchung und praktische Evaluierung eines **semiglatten Newton-Verfahrens** für das quadratisch regularisierte und penalisierte Hitchcock-Problem (endliches Transportproblem). Zur Einordnung der Performanz, Laufzeit und Genauigkeit wird das Verfahren empirisch mit zwei etablierten Algorithmen verglichen:
- **Sinkhorn-Algorithmus** (entropische Regularisierung)
- **Simplex-Algorithmus** (exaktes Verfahren via *Python Optimal Transport*, POT)

---

## Projektstruktur

Das Projekt ist grob in drei Bereiche aufgeteilt. Der Ordner Algorithmen_Funktionen enthält die Implementierungen der verschiedenen Lösungsverfahren, sowie die Datengenerierung. Der Ordner Tests enthält die verschiedenen Skripte zur Ausführung der numerischen Experimente und Ergebnisse speichert diese in CSV, PDF oder TEX Dateien. Mit dem Ausführen der main.py Methode können alle numerische Experimente aufgerufen werden.
