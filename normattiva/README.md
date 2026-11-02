# Atti doganali 1930-1938 da Normattiva

- `elenco.csv`: atti richiesti (data e tipo in lista, data corretta, note sulle discrepanze)
- `atti_normattiva.csv`: per atto, estremi Normattiva, GU, legge di conversione, stato delle tabelle, link al PDF della GU
- `testi/`: testo originario di ciascun atto (versione «originale» di Normattiva)
- `out/export/`: export Akoma Ntoso originali; `out/ricerca.csv`: esito della ricerca per anno e numero

Le tabelle in «formato grafico» non sono nell'export: vanno lette nel PDF della GU (`gu_pdf`).
Rilancio: modificare `run_args.txt` (codici file o `all`) e fare push; poi `python normattiva/estrai.py`.
