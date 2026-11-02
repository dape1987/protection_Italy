"""Funzioni comuni per le ricerche su Normattiva Open Data."""
import time
import requests

B = "https://api.normattiva.it/t/normattiva.api/bff-opendata/v1/api/v1/ricerca/avanzata"
CAMPI = ["denominazione", "data_emanazione", "numero", "codice_redazionale", "data_gu", "numero_gu", "titolo"]


def riga(a):
    return {"denominazione": a.get("denominazioneAtto"),
            "data_emanazione": f'{a["annoProvvedimento"]}-{int(a["meseProvvedimento"]):02d}-{int(a["giornoProvvedimento"]):02d}',
            "numero": a.get("numeroProvvedimento"), "codice_redazionale": a.get("codiceRedazionale"),
            "data_gu": a.get("dataGU"), "numero_gu": a.get("numeroGU"),
            "titolo": " ".join((a.get("titoloAtto") or "").strip("[] ").split())}


def cerca(extra, dal, al):
    """Tutte le pagine di una ricerca; restituisce (atti dichiarati, righe). Ripete le pagine fallite."""
    pag, out, dich = 1, [], None
    while True:
        body = {**extra, "dataInizioEmanazione": dal, "dataFineEmanazione": al, "orderType": "vecchio",
                "paginazione": {"paginaCorrente": pag, "numeroElementiPerPagina": 100}}
        j = {}
        for tentativo in range(6):
            try:
                j = requests.post(B, json=body, timeout=120).json() or {}
                if "listaAtti" in j:
                    break
            except Exception:
                pass
            time.sleep(20 * (tentativo + 1))
        dich = j.get("numeroAttiTrovati", dich)
        out += [riga(a) for a in j.get("listaAtti") or []]
        if pag >= int(j.get("numeroPagine") or 1):
            return dich, out
        pag += 1
        time.sleep(0.3)
