"""Tutti gli atti 1926-1939 che contengono nel testo le parole cercate (Normattiva Open Data)."""
import csv, os, time
import requests

B = "https://api.normattiva.it/t/normattiva.api/bff-opendata/v1/api/v1/ricerca/avanzata"
O = "normattiva/out/dazio"
os.makedirs(O, exist_ok=True)
PAROLE = ["dazio", "dazi", "doganale"]
campi = ["parola", "anno", "denominazione", "data_emanazione", "numero", "codice_redazionale",
         "data_gu", "numero_gu", "titolo"]
tot = open(f"{O}/_totali.csv", "w", encoding="utf-8")
tot.write("parola,anno,trovati_dichiarati,righe_scaricate\n")
with open(f"{O}/risultati.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, campi)
    w.writeheader()
    for p in PAROLE:
        for anno in range(1926, 1940):
            pag, righe, dichiarati = 1, 0, None
            while True:
                body = {"testoRicerca": p, "dataInizioEmanazione": f"{anno}-01-01",
                        "dataFineEmanazione": f"{anno}-12-31", "orderType": "vecchio",
                        "paginazione": {"paginaCorrente": pag, "numeroElementiPerPagina": 100}}
                for tentativo in range(3):
                    try:
                        j = requests.post(B, json=body, timeout=120).json() or {}
                        break
                    except Exception:
                        time.sleep(10)
                else:
                    j = {}
                dichiarati = j.get("numeroAttiTrovati", dichiarati)
                for a in j.get("listaAtti") or []:
                    righe += 1
                    w.writerow({"parola": p, "anno": anno, "denominazione": a.get("denominazioneAtto"),
                                "data_emanazione": f'{a["annoProvvedimento"]}-{int(a["meseProvvedimento"]):02d}-{int(a["giornoProvvedimento"]):02d}',
                                "numero": a.get("numeroProvvedimento"), "codice_redazionale": a.get("codiceRedazionale"),
                                "data_gu": a.get("dataGU"), "numero_gu": a.get("numeroGU"),
                                "titolo": " ".join((a.get("titoloAtto") or "").strip("[] ").split())})
                if pag >= int(j.get("numeroPagine") or 1):
                    break
                pag += 1
                time.sleep(0.5)
            tot.write(f"{p},{anno},{dichiarati},{righe}\n")
            tot.flush()
