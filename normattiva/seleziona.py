"""Candidati per le variazioni tariffarie: temi tariffa/sopradazi/esenzioni/trattato, rilevanza alta,
escluse le leggi di conversione senza modificazioni e i 49 atti già scaricati."""
import csv

D = "normattiva"
K = {"tariffa", "sopradazi_ritorsioni", "esenzioni_riduzioni", "trattato"}
R = list(csv.DictReader(open(f"{D}/politica_commerciale_1926_1939.csv", encoding="utf-8")))
C = [r for r in R if set(r["temi"].split(";")) & K and r["rilevanza"] == "alta" and r["in_lista_49"] != "sì"
     and not (r["conversione_di"] and "modificazion" not in r["titolo"].lower())]
with open(f"{D}/candidati.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, ["codice_redazionale", "denominazione", "data_emanazione", "numero", "temi", "titolo"],
                       extrasaction="ignore")
    w.writeheader()
    w.writerows(C)
print(len(C), "candidati")
