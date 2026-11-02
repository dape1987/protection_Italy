"""Normattiva Open Data: ricerca per anno+numero e export del testo originario."""
import csv, json, os, sys, time
import requests
from normattiva import Normattiva

B = "https://api.normattiva.it/t/normattiva.api/bff-opendata/v1/api/v1"
O = "normattiva/out"
os.makedirs(f"{O}/export", exist_ok=True)
EXPORT = sys.argv[1:]  # codici file da esportare; "all" = tutti i trovati


def cerca(anno, numero):
    body = {"numeroProvvedimento": numero, "orderType": "vecchio",
            "paginazione": {"paginaCorrente": 1, "numeroElementiPerPagina": 50}}
    if anno:
        body["annoProvvedimento"] = anno
    r = requests.post(f"{B}/ricerca/avanzata", json=body, timeout=60)
    atti = (r.json() or {}).get("listaAtti") or []
    return [a for a in atti if a.get("numeroProvvedimento") == str(numero)
            and 1929 <= int(a.get("annoProvvedimento") or 0) <= 1939]


rows = list(csv.DictReader(open("normattiva/elenco.csv", encoding="utf-8")))
campi = ["file", "data_lista", "tipo_lista", "oggetto", "esito", "denominazione", "data_emanazione",
         "codice_redazionale", "data_gu", "numero_gu", "gu_pdf", "titolo"]
trovati = []
with open(f"{O}/ricerca.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, campi)
    w.writeheader()
    for r in rows:
        anno = r["data"][:4]
        atti, esito = cerca(anno, r["num"]), "anno+numero"
        if not atti:
            atti, esito = cerca(None, r["num"]), "solo numero 1929-39"
        if not atti:
            esito = "non trovato"
        for a in atti or [{}]:
            de = a and f'{a["annoProvvedimento"]}-{int(a["meseProvvedimento"]):02d}-{int(a["giornoProvvedimento"]):02d}'
            gu = a.get("dataGU", "")
            w.writerow({"file": r["file"], "data_lista": r["data"], "tipo_lista": r["tipo"],
                        "oggetto": r["oggetto"], "esito": esito if len(atti) < 2 else f"{esito} ({len(atti)} atti)",
                        "denominazione": a.get("denominazioneAtto", ""), "data_emanazione": de or "",
                        "codice_redazionale": a.get("codiceRedazionale", ""), "data_gu": gu,
                        "numero_gu": a.get("numeroGU", ""),
                        "gu_pdf": gu and f'https://www.gazzettaufficiale.it/eli/gu/{gu.replace("-", "/")}/{a["numeroGU"]}/sg/pdf',
                        "titolo": (a.get("titoloAtto") or "").strip("[] ")})
            if a:
                trovati.append((r["file"], a))
        time.sleep(1)

log = open(f"{O}/export/_log.csv", "a", encoding="utf-8")
with Normattiva() as nt:
    for file, a in trovati:
        if "all" not in EXPORT and file not in EXPORT:
            continue
        dest = f"{O}/export/{file}_{a['codiceRedazionale']}.zip"
        if os.path.exists(dest):
            continue
        t0 = time.time()
        try:
            ex = nt.start_export(format="AKN", mode="originale", massimo_atti=5,
                                 denominazione=a["denominazioneAtto"], anno=int(a["annoProvvedimento"]),
                                 numero=a["numeroProvvedimento"], mese=int(a["meseProvvedimento"]),
                                 giorno=int(a["giornoProvvedimento"]))
            ex.wait(timeout=1800)
            ex.save(dest)
            log.write(f"{file},ok,{time.time() - t0:.0f}s\n")
        except Exception as e:
            log.write(f"{file},errore,{type(e).__name__}: {str(e)[:200]!r}\n")
        log.flush()
