"""Da export AKN a testi .txt e tabella riepilogativa atti_normattiva.csv."""
import csv, glob, html, os, re, zipfile

D = "normattiva"
os.makedirs(f"{D}/testi", exist_ok=True)


def testo(xml):
    xml = re.sub(r"<(br|/p|/tr|/div|/heading|/num)[^>]*>", "\n", xml)
    xml = re.sub(r"</t[dh]>", " | ", xml)
    t = html.unescape(re.sub(r"<[^>]+>", " ", xml))
    t = re.sub(r"[ \t]+", " ", t)
    return re.sub(r"\n\s*\n+", "\n", t).strip()


ric = {r["file"]: r for r in csv.DictReader(open(f"{D}/out/ricerca.csv", encoding="utf-8"))}
campi = ["file", "data_lista", "tipo_lista", "oggetto_lista", "denominazione", "data_emanazione", "numero",
         "codice_redazionale", "data_gu", "numero_gu", "conversione", "tabelle", "corrisponde_lista",
         "titolo", "gu_pdf", "testo_txt"]
with open(f"{D}/atti_normattiva.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, campi)
    w.writeheader()
    for r in csv.DictReader(open(f"{D}/elenco.csv", encoding="utf-8")):
        a = ric.get(r["file"], {})
        z = glob.glob(f"{D}/out/export/{r['file']}_*.zip")
        row = {"file": r["file"], "data_lista": r["data"], "tipo_lista": r["tipo"], "oggetto_lista": r["oggetto"],
               "denominazione": a.get("denominazione"), "data_emanazione": a.get("data_emanazione"),
               "numero": r["num"], "codice_redazionale": a.get("codice_redazionale"),
               "data_gu": a.get("data_gu"), "numero_gu": a.get("numero_gu"), "titolo": a.get("titolo"),
               "gu_pdf": a.get("gu_pdf"),
               "corrisponde_lista": "sì" if a.get("data_emanazione") == r["data"] else "NO: data diversa"}
        if z:
            with zipfile.ZipFile(z[0]) as zz:
                xml = "".join(zz.read(n).decode("utf-8") for n in zz.namelist() if n.endswith(".xml"))
            t = testo(xml)
            i = t.find("VITTORIO EMANUELE")
            corpo = t[i:] if i >= 0 else t
            m = re.search(r"convertit[oa][^.]*?dalla L\. \d+ \w+ \d{4}, n\. \d+", t)
            row["conversione"] = m.group(0) if m else ""
            row["tabelle"] = ("formato grafico (vedi GU)" if "formato grafico" in corpo
                              else "trascritte" if " | " in corpo else "nessuna")
            p = f"{D}/testi/{r['file']}.txt"
            open(p, "w", encoding="utf-8").write(f"{a.get('titolo', '')}\n{a.get('gu_pdf', '')}\n\n{corpo}\n")
            row["testo_txt"] = p
        w.writerow(row)
