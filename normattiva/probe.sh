#!/usr/bin/env bash
# Test di formati di richiesta per i R.D.L. non trovati via URN
set -u
B="https://api.normattiva.it/t/normattiva.api/bff-opendata/v1/api/v1"
O=normattiva/probe
mkdir -p "$O"
post() { curl -s -m 60 -o "$O/$1.json" -w "$1,%{http_code}\n" -X POST "$B/$2" -H "Content-Type: application/json" --data "$3" >> "$O/_status.csv"; sleep 1; }
echo "test,http" > "$O/_status.csv"
post A_rdl692_nosuffix atto/dettaglio-atto-urn '{"urn":"urn:nir:stato:regio.decreto.legge:1930-06-04;692"}'
post B_l340_orig atto/dettaglio-atto-urn '{"urn":"urn:nir:stato:legge:1931-03-26;340@originale"}'
post C_l340 atto/dettaglio-atto-urn '{"urn":"urn:nir:stato:legge:1931-03-26;340"}'
post D_rdl1496 atto/dettaglio-atto-urn '{"urn":"urn:nir:stato:regio.decreto.legge:1930-11-27;1496"}'
post E_avanz_num ricerca/avanzata '{"denominazioneAtto":"REGIO DECRETO-LEGGE","annoProvvedimento":"1930","numeroProvvedimento":"692","orderType":"vecchio","paginazione":{"paginaCorrente":1,"numeroElementiPerPagina":10}}'
post F_avanz_date ricerca/avanzata '{"denominazioneAtto":"REGIO DECRETO-LEGGE","dataInizioEmanazione":"1930-06-01","dataFineEmanazione":"1930-06-10","orderType":"vecchio","paginazione":{"paginaCorrente":1,"numeroElementiPerPagina":50}}'
post G_sempl_filtro ricerca/semplice '{"testoRicerca":"dazio","orderType":"vecchio","paginazione":{"paginaCorrente":1,"numeroElementiPerPagina":50},"filtriMap":{"codice_tipo_provvedimento":"PRL","anno_provvedimento":1930}}'
post H_sempl_testo ricerca/semplice '{"testoRicerca":"decreto-legge 4 giugno 1930, n. 692","orderType":"vecchio","paginazione":{"paginaCorrente":1,"numeroElementiPerPagina":20}}'
curl -s -m 60 -o "$O/I_denominazioni.json" -w "I_denominazioni,%{http_code}\n" "$B/tipologiche/denominazione-atto" >> "$O/_status.csv"
