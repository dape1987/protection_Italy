"""Seleziona e classifica gli atti di politica commerciale 1926-1939 (titoli + parole trovate nel testo)."""
import csv, re
from collections import defaultdict

D = "normattiva"
U = f"{D}/out/universo"
COMMERCIO = r"commerc|scambi|dogan|dazi|tariff|pagament|clearing|compensaz|navigazion|merci|contingent|importaz|esportaz|economic|valut|stabiliment|prodotti|cambi"
NONPERT = r"(rettific|delimitazion|modificazion|variazion|determinazion)\w* (de[il]|di) confin|confin\w* (fra|tra) (i )?comun|dogan.*(personale|ruol|organic|funzionari|laboratori|praticant|previdenza|impiegat|carriera|circoscrizion|sede)|(personale|ruol|organic|funzionari|laboratori|praticant|previdenza|impiegat|carriera|circoscrizion).*dogan"
TEMI = {  # ordine = priorità per la categoria principale
    "trattato": r"trattat|accord|convenzion|protocoll|modus vivendi|scambio di note|arrangiament|atti stipulati|atti internazionali|dichiarazion",
    "contingenti_divieti": r"contingent|divieto|divieti|vietat|licenz\w* di (importazion|esportazion)|permess\w* di (importazion|esportazion)|autorizzazion\w* (all'|per l')(importazion|esportazion)",
    "pagamenti_valute": r"clearing|compensazion\w* privat|pagament|valut|divis[ae]|\bcambi\b|\bcambio\b|istituto nazionale per i cambi|scambi e (per le )?valute",
    "sopradazi_ritorsioni": r"sopradaz|maggiorazion|tass\w* (speciali )?di compensazione|dazi[o]? (speciale|supplementar|aggiunt)|ritorsion|reciprocit|non estendono",
    "colonie_zone_franche": r"coloni|eritrea|somalia|libia|tripolitania|cirenaica|egeo|africa orientale|zona franca|zone franche|carnaro|zara|livigno|campione d'italia|\bfiume\b",
    "tariffa": r"regime doganale|trattamento doganale|tariffa (generale )?(dei )?dazi|tariff\w* doganal|\bdazi\b|\bdazio\b|diritt\w* di confine|diritt\w* doganal|dazi? (di|sul) valore|doganal|tassa speciale|merci (provenienti|importate) dall'estero|speciale dazio|diritt\w* di statistica",
    "esenzioni_riduzioni": r"esenzion|esent|franchigi|riduzion\w*|ridott|esoner|abolizion",
    "temporanea_restituzioni": r"temporanea|restituzion|rimbors|drawback",
    "fabbricazione_confine": r"fabbricazione|sovrimposta di confine|sopratassa di confine|monopol|regime fiscale|tassa di vendita|tassa di scambio",
    "esportazione": r"esportazion|istituto nazionale per l'esportazione|marchio nazionale|premi\b",
    "importazione": r"importazion",
    "organizzazione_commercio_estero": r"commercio (estero|con l'estero)|scambi commerciali|sottosegretariato per gli scambi|ministero per gli scambi|scambi e valute|istituto nazionale fascista per il commercio",
    "consumo_interni": r"\bconsumo\b|cint[ae] daziari|daziari|dazi[o]? comunal|imposte di consumo",
}
ALTI = {"tariffa", "sopradazi_ritorsioni", "contingenti_divieti", "pagamenti_valute", "esenzioni_riduzioni",
        "temporanea_restituzioni", "fabbricazione_confine", "esportazione", "importazione"}
PAESI = ["Albania", "Argentina", "Australia", "Austria", "Belgio", "Bolivia", "Brasile", "Bulgaria", "Canada",
         "Cecoslovacchia", "Cile", "Cina", "Colombia", "Cuba", "Danimarca", "Danzica", "Ecuador", "Egitto",
         "Estonia", "Etiopia", "Finlandia", "Francia", "Germania", "Giappone", "Gran Bretagna", "Grecia",
         "Guatemala", "Haiti", "India", "Irak", "Iraq", "Irlanda", "Islanda", "Jugoslavia", "Lettonia",
         "Liberia", "Lituania", "Lussemburgo", "Manciukuò", "Marocco", "Messico", "Norvegia", "Nuova Zelanda",
         "Olanda", "Paesi Bassi", "Paraguay", "Persia", "Iran", "Perù", "Polonia", "Portogallo", "Regno Unito",
         "Romania", "Rumania", "Russia", "Unione delle Repubbliche Sovietiche", "U.R.S.S.", "Salvador", "San Marino",
         "Serbi, Croati e Sloveni", "Siam", "Spagna", "Stati Uniti", "Sud Africa", "Unione Sudafricana", "Svezia",
         "Svizzera", "Tunisia", "Turchia", "Ungheria", "Uruguay", "Venezuela", "Yemen", "Afghanistan", "Arabia"]
NORM = {"Rumania": "Romania", "Olanda": "Paesi Bassi", "Irak": "Iraq", "Persia": "Iran", "Regno Unito": "Gran Bretagna",
        "Serbi, Croati e Sloveni": "Jugoslavia", "Unione delle Repubbliche Sovietiche": "URSS", "U.R.S.S.": "URSS",
        "Russia": "URSS", "Unione Sudafricana": "Sud Africa"}
MESI = {m: i for i, m in enumerate(["gennaio", "febbraio", "marzo", "aprile", "maggio", "giugno", "luglio", "agosto",
                                    "settembre", "ottobre", "novembre", "dicembre"], 1)}
DN = re.compile(r"(\d+)°?\s+(" + "|".join(MESI) + r")\s+(\d{4})[^,]*?,\s*n\.\s*(\d+)", re.I)
CONV = ("conversione in legge", "conversione, in legge", "convalidazione")


def convertiti(t):
    m = re.search(r",?\s+(che|con cui|concernent|recant|relativ|portant|riguardant|contenent|riflettent|sul|sull|sulla|sui|per)\b", t)
    testa = t[:m.start()] if m else t
    return [f"{a}-{MESI[mm.lower()]:02d}-{int(g):02d}_{n}" for g, mm, a, n in DN.findall(testa)]


universo = {r["codice_redazionale"]: r for r in csv.DictReader(open(f"{U}/atti_1926_1939.csv", encoding="utf-8"))}
universo = sorted(universo.values(), key=lambda r: r["data_emanazione"])
parole = defaultdict(set)
for r in csv.DictReader(open(f"{U}/testo.csv", encoding="utf-8")):
    parole[r["codice_redazionale"]].add(r["parola"])
lista = {r["codice_redazionale"] for r in csv.DictReader(open(f"{D}/atti_normattiva.csv", encoding="utf-8"))}

conv = {}  # RDL convertiti: chiave data_numero -> legge di conversione
for r in universo:
    t = r["titolo"]
    if t.lower().startswith(CONV):
        for k in convertiti(t):
            conv.setdefault(k, f'L. {r["data_emanazione"]} n. {r["numero"]}' + (" (con modif.)" if "modificazion" in t.lower() else ""))

out = []
for r in universo:
    t, c = r["titolo"].lower(), r["codice_redazionale"]
    if re.search(NONPERT, t):
        continue
    temi = [k for k, p in TEMI.items() if re.search(p, t)]
    if "trattato" in temi and not re.search(COMMERCIO, t):
        temi[temi.index("trattato")] = "trattato_altro"
    if not temi and not parole[c]:
        continue
    alto = ALTI & set(temi) or ("trattato" in temi)
    rilev = ("alta" if alto else "media" if set(temi) & {"colonie_zone_franche", "organizzazione_commercio_estero"}
             else "bassa" if temi == ["consumo_interni"] else "da verificare")
    if rilev == "da verificare" and not parole[c]:
        continue  # es. trattati non commerciali senza parole di commercio nel testo
    paesi = sorted({NORM.get(p, p) for p in PAESI if re.search(r"\b" + re.escape(p), r["titolo"])})
    conversione = t.startswith(CONV)
    rdl = convertiti(r["titolo"]) if conversione else []
    out.append({**{k: r[k] for k in ("data_emanazione", "denominazione", "numero", "codice_redazionale",
                                       "data_gu", "numero_gu")},
                "categoria": (temi[0] if temi else "solo testo"), "temi": ";".join(temi), "rilevanza": rilev,
                "paesi": ";".join(paesi),
                "conversione_di": ";".join(rdl),
                "convertito_da": "" if conversione else conv.get(f'{r["data_emanazione"]}_{r["numero"]}', ""),
                "in_lista_49": "sì" if c in lista else "",
                "parole_testo": "+".join(sorted(parole[c])),
                "gu_pdf": r["data_gu"] and f'https://www.gazzettaufficiale.it/eli/gu/{r["data_gu"].replace("-", "/")}/{r["numero_gu"]}/sg/pdf',
                "titolo": r["titolo"]})
out.sort(key=lambda x: (x["data_emanazione"], int(x["numero"] or 0)))
with open(f"{D}/politica_commerciale_1926_1939.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, list(out[0]))
    w.writeheader()
    w.writerows(out)
print(len(universo), "atti nell'universo;", len(out), "selezionati")
