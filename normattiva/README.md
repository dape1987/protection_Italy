# Atti doganali 1930-1938 da Normattiva

- `elenco.csv`: atti richiesti (data e tipo in lista, data corretta, note sulle discrepanze)
- `atti_normattiva.csv`: per atto, estremi Normattiva, GU, legge di conversione, stato delle tabelle, link al PDF della GU
- `testi/`: testo originario di ciascun atto (versione «originale» di Normattiva)
- `out/export/`: export Akoma Ntoso originali; `out/ricerca.csv`: esito della ricerca per anno e numero

Le tabelle in «formato grafico» non sono nell'export: vanno lette nel PDF della GU (`gu_pdf`).
Rilancio: modificare `run_args.txt` (codici file o `all`) e fare push; poi `python normattiva/estrai.py`.

## Ricerca a tappeto 1926-1939
- `dazio_1926_1939.csv`: tutti gli atti emanati 1926-1939 che contengono nel testo almeno una tra
  dazio, dazi, doganale, doganali, dogana, dogane, confine, tariffa (ricerca a parola esatta, testo integrale).
  Una riga per atto; `parole` = parole trovate; `categoria` e `rilevanza` assegnate dal titolo (`classifica.py`), da rivedere.
- `out/dazio/`: risultati grezzi per parola e anno; `_totali.csv` confronta atti dichiarati e scaricati.
- Rilancio: `cerca_dazio.py` (push su GitHub), poi `python normattiva/classifica.py`.
