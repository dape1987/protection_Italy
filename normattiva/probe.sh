#!/usr/bin/env bash
# Ricerca per titolo dei decreti con numero non corrispondente alla lista
set -u
B="https://api.normattiva.it/t/normattiva.api/bff-opendata/v1/api/v1"
O=normattiva/probe
mkdir -p "$O"
post() { curl -s -m 60 -o "$O/$1.json" -w "$1,%{http_code}\n" -X POST "$B/ricerca/avanzata" -H "Content-Type: application/json" --data "$2" >> "$O/_status2.csv"; sleep 1; }
echo "test,http" > "$O/_status2.csv"
pg='"orderType":"vecchio","paginazione":{"paginaCorrente":1,"numeroElementiPerPagina":100}'
post T_frumento '{"titoloRicerca":"frumento","dataInizioEmanazione":"1930-01-01","dataFineEmanazione":"1934-12-31",'"$pg"'}'
post T_grano '{"titoloRicerca":"grano","dataInizioEmanazione":"1930-01-01","dataFineEmanazione":"1934-12-31",'"$pg"'}'
post T_scambio '{"titoloRicerca":"tassa di scambio","dataInizioEmanazione":"1931-01-01","dataFineEmanazione":"1932-12-31",'"$pg"'}'
post T_macinazione '{"titoloRicerca":"macinazione","dataInizioEmanazione":"1930-01-01","dataFineEmanazione":"1934-12-31",'"$pg"'}'
post N_869_1931 '{"annoProvvedimento":"1931","numeroProvvedimento":"869",'"$pg"'}'
