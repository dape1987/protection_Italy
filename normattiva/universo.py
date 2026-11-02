"""Elenco di tutti gli atti 1926-1939 su Normattiva (ricerca per mese) e ricerca nel testo integrale per parole."""
import calendar, csv, os, time
import requests

B = "https://api.normattiva.it/t/normattiva.api/bff-opendata/v1/api/v1/ricerca/avanzata"
O = "normattiva/out/universo"
os.makedirs(O, exist_ok=True)
PAROLE = ["dazio", "dazi", "doganale", "doganali", "dogana", "dogane", "confine", "tariffa",
          "importazione", "importazioni", "esportazione", "esportazioni", "contingente", "contingenti",
          "contingentamento", "clearing", "compensazione", "compensazioni", "valuta", "valute", "divise", "cambi"]
CAMPI = ["denominazione", "data_emanazione", "numero", "codice_redazionale", "data_gu", "numero_gu", "titolo"]


def riga(a):
    return {"denominazione": a.get("denominazioneAtto"),
            "data_emanazione": f'{a["annoProvvedimento"]}-{int(a["meseProvvedimento"]):02d}-{int(a["giornoProvvedimento"]):02d}',
            "numero": a.get("numeroProvvedimento"), "codice_redazionale": a.get("codiceRedazionale"),
            "data_gu": a.get("dataGU"), "numero_gu": a.get("numeroGU"),
            "titolo": " ".join((a.get("titoloAtto") or "").strip("[] ").split())}


def cerca(extra, dal, al):
    """Tutte le pagine di una ricerca; restituisce (atti dichiarati, righe)."""
    pag, out, dich = 1, [], None
    while True:
        body = {**extra, "dataInizioEmanazione": dal, "dataFineEmanazione": al, "orderType": "vecchio",
                "paginazione": {"paginaCorrente": pag, "numeroElementiPerPagina": 100}}
        j = {}
        for _ in range(4):
            try:
                j = requests.post(B, json=body, timeout=120).json() or {}
                break
            except Exception:
                time.sleep(15)
        dich = j.get("numeroAttiTrovati", dich)
        out += [riga(a) for a in j.get("listaAtti") or []]
        if pag >= int(j.get("numeroPagine") or 1):
            return dich, out
        pag += 1
        time.sleep(0.3)


tot = open(f"{O}/_totali.csv", "w", encoding="utf-8")
tot.write("ricerca,periodo,dichiarati,scaricati\n")
with open(f"{O}/atti_1926_1939.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, CAMPI)
    w.writeheader()
    for anno in range(1926, 1940):
        for mese in range(1, 13):
            fine = calendar.monthrange(anno, mese)[1]
            d, rr = cerca({}, f"{anno}-{mese:02d}-01", f"{anno}-{mese:02d}-{fine}")
            w.writerows(rr)
            tot.write(f"tutti,{anno}-{mese:02d},{d},{len(rr)}\n")
            tot.flush()

with open(f"{O}/testo.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, ["parola"] + CAMPI)
    w.writeheader()
    for p in PAROLE:
        for anno in range(1926, 1940):
            d, rr = cerca({"testoRicerca": p}, f"{anno}-01-01", f"{anno}-12-31")
            w.writerows({"parola": p, **r} for r in rr)
            tot.write(f"{p},{anno},{d},{len(rr)}\n")
            tot.flush()
