"""Atti emanati in finestre di date, per correggere numeri della lista che non corrispondono."""
import csv, requests

B = "https://api.normattiva.it/t/normattiva.api/bff-opendata/v1/api/v1"
FINESTRE = {
    "869 frumento": ("1930-07-01", "1930-07-08"),
    "980 frumento 1930": ("1930-08-13", "1930-08-19"),
    "980 frumento 1931": ("1931-08-13", "1931-08-19"),
    "1100 grano": ("1933-08-10", "1933-08-16"),
    "1562 tassa scambio": ("1931-12-21", "1931-12-28"),
}
with open("normattiva/out/cerca_data.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["caso", "denominazione", "data_emanazione", "numero", "codice_redazionale", "data_gu", "numero_gu", "titolo"])
    for caso, (dal, al) in FINESTRE.items():
        pag = 1
        while True:
            body = {"dataInizioEmanazione": dal, "dataFineEmanazione": al, "orderType": "vecchio",
                    "paginazione": {"paginaCorrente": pag, "numeroElementiPerPagina": 100}}
            j = requests.post(f"{B}/ricerca/avanzata", json=body, timeout=60).json() or {}
            for a in j.get("listaAtti") or []:
                w.writerow([caso, a.get("denominazioneAtto"),
                            f'{a["annoProvvedimento"]}-{int(a["meseProvvedimento"]):02d}-{int(a["giornoProvvedimento"]):02d}',
                            a.get("numeroProvvedimento"), a.get("codiceRedazionale"), a.get("dataGU"),
                            a.get("numeroGU"), (a.get("titoloAtto") or "").strip("[] ")])
            if pag >= int(j.get("numeroPagine") or 1):
                break
            pag += 1
