"""Testi dei candidati (export AKN) e tabella con indizi di variazione tariffaria."""
import csv, glob, html, os, re, sys, zipfile

D = "normattiva"
SRC = sys.argv[1] if len(sys.argv) > 1 else f"{D}/out/export_pc"
OUT_T = f"{D}/testi_pc"
os.makedirs(OUT_T, exist_ok=True)
ALIQ = re.compile(r"\bL\.\s*\d[\d.]*(,\d+)?\s*(oro\s*)?(per|il|al)\s+(quintale|chilogramm|kg|ettolitr|capo|cento)|per cento|ad valorem|sul valore", re.I)
VOCE = re.compile(r"\bvoc[ei]\s+(?:n\.\s*|numer[oi]\s*)?(\d{1,4}(?:\s*[a-z]\))?(?:\s*(?:,|e|ed)\s*\d{1,4}(?:\s*[a-z]\))?)*)", re.I)
VERBO = re.compile(r"dazi\w*[^.;]{0,160}(stabilit|fissat|modificat|elevat|aumentat|ridott|sostituit|sospes|abolit|ripristinat|portat)|"
                   r"(stabilit|fissat|modificat|elevat|aumentat|ridott|sostituit|sospes|abolit|ripristinat|portat)\w*[^.;]{0,160}dazi", re.I)


def testo(xml):
    xml = re.sub(r"\s*</p>\s*(</t[dh]>)", r"\1", xml)
    xml = re.sub(r"<(br|/p|/tr|/div|/heading|/num)[^>]*>", "\n", xml)
    xml = re.sub(r"</t[dh]>", " | ", xml)
    t = html.unescape(re.sub(r"<[^>]+>", " ", xml))
    t = re.sub(r"[ \t]+", " ", t)
    return re.sub(r"\n\s*\n+", "\n", t).strip()


meta = {r["codice_redazionale"]: r for r in csv.DictReader(open(f"{D}/politica_commerciale_1926_1939.csv", encoding="utf-8"))}
MOD = re.compile(r"con (le seguenti |alcune )?modificazion|sono apportate le seguenti|e' modificat|sostituit[oa] dal seguente", re.I)
campi = ["codice_redazionale", "data_emanazione", "denominazione", "numero", "tipo", "temi", "paesi", "tabelle",
         "n_aliquote", "n_verbi_dazio", "voci_citate", "conversione", "convertito_da", "titolo", "gu_pdf", "testo_txt"]
righe = []
for z in sorted(glob.glob(f"{SRC}/*.zip")):
    c = re.search(r"(\d{3}[A-Z]\d{4})", os.path.basename(z)).group(1)
    with zipfile.ZipFile(z) as zz:
        xml = "".join(zz.read(n).decode("utf-8") for n in zz.namelist() if n.endswith(".xml"))
    t = testo(xml)
    i = xml.find("<preamble") if "<preamble" in xml else xml.find("<body")
    corpo = testo(xml[i:])
    tab = [len(re.findall(r"<tr", x)) for x in re.findall(r"<table.*?</table>", xml[i:], re.S)]
    m = meta.get(c, {})
    conv = re.search(r"convertit[oa][^.]*?dalla L\. \d+ \w+ \d{4}, n\. \d+", t)
    p = f"{OUT_T}/{c}.txt"
    open(p, "w", encoding="utf-8").write(f"{m.get('titolo', '')}\n{m.get('gu_pdf', '')}\n\n{corpo}\n")
    tipo = ("atto" if not re.match(r"conversione in legge", m.get("titolo", ""), re.I)
            else "conversione con modifiche" if MOD.search(corpo) else "conversione senza modifiche")
    voci = sorted({re.sub(r"\s+", " ", v) for v in VOCE.findall(corpo)})
    righe.append({"codice_redazionale": c, **{k: m.get(k, "") for k in ("data_emanazione", "denominazione", "numero",
                                                                        "temi", "paesi", "convertito_da", "titolo", "gu_pdf")},
                  "tabelle": ("formato grafico (vedi GU)" if "formato grafico" in corpo
                              else "solo intestazione (vedi GU)" if tab and max(tab) <= 1
                              else "trascritte" if tab else "nessuna tabella"),
                  "n_aliquote": len(ALIQ.findall(corpo)), "n_verbi_dazio": len(VERBO.findall(corpo)),
                  "voci_citate": "; ".join(voci)[:300], "conversione": conv.group(0) if conv else "", "tipo": tipo, "testo_txt": p})
righe.sort(key=lambda r: (r["data_emanazione"], int(r["numero"] or 0)))
with open(f"{D}/testi_candidati.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, campi)
    w.writeheader()
    w.writerows(righe)
print(len(righe), "testi estratti")
