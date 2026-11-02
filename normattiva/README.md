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

## Testi dei candidati (variazioni tariffarie)
- `candidati.csv` (da `seleziona.py`): 689 atti a rilevanza alta con temi tariffa, sopradazi/ritorsioni,
  esenzioni/riduzioni o trattato, esclusi i 49 già in `testi/`.
- `out/export_pc/`: export Akoma Ntoso originali (workflow `export_pc`, 3 processi paralleli; salta gli zip già presenti).
- `testi_pc/`: testo originario di ciascun candidato; `testi_candidati.csv` (da `estrai_pc.py`), una riga per atto:
  - `tipo`: atto / conversione senza modifiche / conversione con modifiche;
  - `tabelle`: formato grafico (vedi GU) / solo intestazione (vedi GU) / trascritte / nessuna tabella;
  - `n_aliquote`: importi per unità o percentuali nel testo; `n_verbi_dazio`: frasi con dazio + stabilito/modificato/ridotto ecc.;
  - `voci_citate`: numeri di voce della tariffa citati.
