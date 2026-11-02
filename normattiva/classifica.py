"""Unisce i risultati della ricerca 'dazio' 1926-1939, toglie i doppioni e classifica gli atti per titolo."""
import csv, re
from collections import defaultdict

D = "normattiva"
CAT = [
    ("dazi e imposte di consumo (interni)", r"\bconsumo\b|cint[ae] daziari|dazi[o]? comunal|daziari"),
    ("colonie, possedimenti, zone franche", r"coloni|eritrea|somalia|libia|tripolitania|cirenaica|egeo|africa orientale|zona franca|zone franche|carnaro|zara|livigno|campione"),
    ("trattati e accordi internazionali", r"trattat|accord|convenzion|protocoll|modus vivendi|scambio di note|dichiarazion|arrangiament"),
    ("temporanea importazione/esportazione", r"temporanea"),
    ("regime doganale e tariffa", r"dogan|\bdazi\b|\bdazio\b|tariff|confine|sopradaz|compensazion|importazion|esportazion|franchigi|contingent|valut|scambi"),
]
lista = {r["codice_redazionale"] for r in csv.DictReader(open(f"{D}/atti_normattiva.csv", encoding="utf-8"))}
atti, parole = {}, defaultdict(set)
for r in csv.DictReader(open(f"{D}/out/dazio/risultati.csv", encoding="utf-8")):
    atti.setdefault(r["codice_redazionale"], r)
    parole[r["codice_redazionale"]].add(r["parola"])

out = []
for c, r in atti.items():
    t = r["titolo"].lower()
    out.append({"data_emanazione": r["data_emanazione"], "denominazione": r["denominazione"], "numero": r["numero"],
                "codice_redazionale": c, "data_gu": r["data_gu"], "numero_gu": r["numero_gu"],
                "categoria": next((k for k, p in CAT if re.search(p, t)), "altro (parola solo nel testo)"),
                "conversione": "sì" if t.startswith("conversione in legge") else "",
                "in_lista_49": "sì" if c in lista else "",
                "parole": "+".join(p for p in ("dazio", "dazi", "doganale") if p in parole[c]),
                "gu_pdf": r["data_gu"] and f'https://www.gazzettaufficiale.it/eli/gu/{r["data_gu"].replace("-", "/")}/{r["numero_gu"]}/sg/pdf',
                "titolo": r["titolo"]})
out.sort(key=lambda x: (x["data_emanazione"], int(x["numero"] or 0)))
with open(f"{D}/dazio_1926_1939.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, list(out[0]))
    w.writeheader()
    w.writerows(out)
