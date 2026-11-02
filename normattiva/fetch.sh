#!/usr/bin/env bash
# Scarica da Normattiva Open Data il dettaglio (versione originaria) di ogni atto in elenco.csv
set -u
API="https://api.normattiva.it/t/normattiva.api/bff-opendata/v1/api/v1/atto/dettaglio-atto-urn"
OUT=normattiva/json
mkdir -p "$OUT"
echo "file,http" > "$OUT/_status.csv"
tail -n +2 normattiva/elenco.csv | while IFS=, read -r urn file rest; do
  code=$(curl -s -m 60 -o "$OUT/$file.json" -w "%{http_code}" -X POST "$API" \
    -H "Content-Type: application/json" --data "{\"urn\":\"$urn\"}")
  echo "$file,$code" >> "$OUT/_status.csv"
  sleep 1
done
