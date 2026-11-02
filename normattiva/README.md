# Atti doganali 1930-1938 da Normattiva

- `elenco.csv`: atti richiesti (data e tipo in lista, data corretta, note sulle discrepanze)
- `atti_normattiva.csv`: per atto, estremi Normattiva, GU, legge di conversione, stato delle tabelle, link al PDF della GU
- `testi/`: testo originario di ciascun atto (versione «originale» di Normattiva)
- `out/export/`: export Akoma Ntoso originali; `out/ricerca.csv`: esito della ricerca per anno e numero

Le tabelle in «formato grafico» non sono nell'export: vanno lette nel PDF della GU (`gu_pdf`).
Rilancio: modificare `run_args.txt` (codici file o `all`) e fare push; poi `python normattiva/estrai.py`.

## Atti di politica commerciale 1926-1939
- `out/universo/atti_1926_1939.csv`: tutti i 34.562 atti emanati 1926-1939 presenti su Normattiva (estremi e titolo).
- `out/universo/testo.csv`: atti che contengono nel testo integrale almeno una di 22 parole (dazio, dazi, doganale/i,
  dogana/e, confine, tariffa, importazione/i, esportazione/i, contingente/i, contingentamento, clearing,
  compensazione/i, valuta/e, divise, cambi); `_totali.csv` confronta atti dichiarati e scaricati.
- `politica_commerciale_1926_1939.csv` (da `classifica_pc.py`): atti selezionati, una riga per atto.
  - `temi`: etichette dal titolo (anche più d'una); `categoria` = la prima per priorità.
  - `rilevanza`: alta / media / bassa / da verificare (parole doganali solo nel testo).
  - `paesi`: paesi nominati nel titolo; `conversione_di` / `convertito_da`: legame R.D.L. - legge di conversione.
  - `parole_testo`: parole trovate nel testo integrale; `in_lista_49`: atti già scaricati in `testi/`.
- Rilancio: push di `universo.py` (o `recupera.py` per le ricerche incomplete), poi `python normattiva/classifica_pc.py`.
