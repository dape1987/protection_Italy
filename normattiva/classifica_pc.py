"""Seleziona e classifica gli atti di politica commerciale 1926-1939 (titoli + parole trovate nel testo)."""
import csv, re
from collections import defaultdict

D = "normattiva"
U = f"{D}/out/universo"
COMMERCIO = r"commerc|scambi|dogan|dazi|tariff|pagament|clearing|compensaz|navigazion|merci|contingent|importaz|esportaz|economic|\bvalut[ae]\b|valutari|stabiliment|prodotti|\bcambi\b"
ESTERO = r"italo-|fra l'italia|tra l'italia|internazional|(firmat|stipulat|conclus)\w* (a|in) (?!roma)|stati|repubblic|regno d|governo|paesi|esteri|confederazion|dominion"
INTERNO = r"societ|ditta|concession|comune di|provincia di|\bente\b|istituto|consorzio|azienda|banca|cassa"
MILITARE = r"leva|classe|arruolament|militar|esercito|marina|aeronautica|carabinieri|ufficial|milizia|truppa|reclut"
FORTI = {"dazio", "dazi", "doganale", "doganali", "dogana", "dogane", "importazione", "importazioni",
         "esportazione", "esportazioni", "contingentamento", "clearing"}
NONPERT = r"(contratt|accord)\w* (economic\w* )?collettiv|(rettific|delimitazion|modificazion|variazion|determinazion)\w* (de[il]|di) confin|confin\w* (fra|tra) (i )?comun|(dogan|scambi e (per le )?valute|commercio estero).*(personale|ruol|organic|funzionari|laboratori|praticant|previdenza|impiegat|carriera|circoscrizion|sede)|(personale|ruol|organic|funzionari|laboratori|praticant|previdenza|impiegat|carriera|circoscrizion).*(dogan|scambi e (per le )?valute)"
TEMI = {  # ordine = priorità per la categoria principale
    "trattato": r"trattat|accord|convenzion|protocoll|modus vivendi|scambio di note|arrangiament|atti stipulati|atti internazionali|dichiarazion",
    "contingenti_divieti": r"contingent|divieto d\w* (importazion|esportazion)|divieti d\w* (importazion|esportazion)|licenz\w* di (importazion|esportazion)|permess\w* di (importazion|esportazion)|autorizzazion\w* (all'|per l')(importazion|esportazion)",
    "pagamenti_valute": r"clearing|compensazion\w* (privat|dei pagamenti|dei crediti)|regolamento dei pagamenti|pagamenti (con|verso|fra|tra|commercial)|\bvalut[ae]\b|valutari|divise estere|divisa estera|\bcambi\b|istituto nazionale per i cambi|scambi e (per le )?valute",
    "sopradazi_ritorsioni": r"sopradaz|maggiorazion|tass\w* (speciali )?di compensazione|dazi[o]? (speciale|supplementar|aggiunt)|ritorsion|reciprocit|non estendono",
    "colonie_zone_franche": r"coloni|eritrea|somalia|libia|tripolitania|cirenaica|egeo|africa orientale|zona franca|zone franche|carnaro|zara|livigno|campione d'italia|\bfiume\b",
    "tariffa": r"regime doganale|trattamento doganale|tariffa (generale )?(dei )?dazi|tariff\w* doganal|\bdazi\b|\bdazio\b|diritt\w* di confine|diritt\w* doganal|dazi? (di|sul) valore|doganal|tassa speciale|merci (provenienti|importate) dall'estero|speciale dazio|diritt\w* di statistica",
    "esenzioni_riduzioni": r"esenzion|esent|franchigi|riduzion\w*|ridott|esoner|abolizion",
    "temporanea_restituzioni": r"temporanea (importazion|esportazion)|restituzion\w* (de[il]|di) (dazi|diritt)|drawback",
    "fabbricazione_confine": r"fabbricazione|sovrimposta di confine|sopratassa di confine|monopol|regime fiscale|tassa di vendita|tass\w* (di|sugli) scambi",
    "esportazione": r"esportazion|istituto nazionale per l'esportazione|marchio nazionale",
    "importazione": r"importazion",
    "organizzazione_commercio_estero": r"commercio (estero|con l'estero)|scambi commerciali|sottosegretariato per gli scambi|ministero per gli scambi|scambi e valute|istituto nazionale fascista per il commercio",
    "consumo_interni": r"\bconsumo\b|cint[ae] daziari|daziari|dazi[o]? comunal|imposte di consumo",
}
ALTI = {"tariffa", "sopradazi_ritorsioni", "contingenti_divieti", "pagamenti_valute", "temporanea_restituzioni",
        "esportazione", "importazione", "trattato"}
DEBOLI = {"esenzioni_riduzioni", "fabbricazione_confine"}  # valgono solo con parole nel testo
DEBOLISSIMI = {"colonie_zone_franche", "consumo_interni"}  # solo con parole doganali/commerciali forti nel testo
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
AGG = {"austriac": "Austria", "german": "Germania", "tedesc": "Germania", "frances": "Francia", "svizzer": "Svizzera",
       "ungheres": "Ungheria", "jugoslav": "Jugoslavia", "iugoslav": "Jugoslavia", "cecoslovacc": "Cecoslovacchia",
       "polacc": "Polonia", "romen": "Romania", "rumen": "Romania", "bulgar": "Bulgaria", "grec": "Grecia", "turc": "Turchia",
       "albanes": "Albania", "spagnol": "Spagna", "portoghes": "Portogallo", "belg": "Belgio", "lussemburghes": "Lussemburgo",
       "oland": "Paesi Bassi", "danes": "Danimarca", "norveges": "Norvegia", "svedes": "Svezia", "finlandes": "Finlandia",
       "eston": "Estonia", "letton": "Lettonia", "lituan": "Lituania", "soviet": "URSS", "russ": "URSS",
       "britannic": "Gran Bretagna", "ingles": "Gran Bretagna", "irlandes": "Irlanda", "american": "Stati Uniti",
       "statunitens": "Stati Uniti", "canades": "Canada", "messican": "Messico", "argentin": "Argentina",
       "brasilian": "Brasile", "cilen": "Cile", "uruguaian": "Uruguay", "peruvian": "Perù", "giappones": "Giappone",
       "cines": "Cina", "egizian": "Egitto", "persian": "Iran", "iranian": "Iran", "etiopic": "Etiopia", "afgan": "Afghanistan",
       "siames": "Siam", "sudafrican": "Sud Africa", "australian": "Australia", "venezuelan": "Venezuela",
       "colombian": "Colombia", "cuban": "Cuba", "ecuadorian": "Ecuador", "bolivian": "Bolivia", "paraguaian": "Paraguay",
       "islandes": "Islanda", "iraches": "Iraq", "manciuk": "Manciukuò", "yemen": "Yemen", "danzic": "Danzica",
       "sammarines": "San Marino"}
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
    if "trattato" in temi and re.search(INTERNO, t) and not re.search(ESTERO, t):
        temi[temi.index("trattato")] = "trattato_altro"  # convenzioni con società, enti, comuni
    if "trattato" in temi and not re.search(COMMERCIO, t):
        temi[temi.index("trattato")] = "trattato_altro"
    if "contingenti_divieti" in temi and re.search(MILITARE, t) and not re.search(COMMERCIO.replace("|contingent", ""), t):
        temi.remove("contingenti_divieti")
    forte = bool(parole[c] & FORTI)
    if not parole[c]:
        temi = [k for k in temi if k not in DEBOLI]
    if not forte:
        temi = [k for k in temi if k not in DEBOLISSIMI]
    if ALTI & set(temi) or (set(temi) & {"esenzioni_riduzioni", "fabbricazione_confine"} and forte):
        rilev = "alta"
    elif set(temi) & {"colonie_zone_franche", "organizzazione_commercio_estero", "esenzioni_riduzioni", "fabbricazione_confine"}:
        rilev = "media"
    elif temi == ["consumo_interni"]:
        rilev = "bassa"
    elif forte or ("trattato_altro" in temi and parole[c]):
        rilev = "da verificare"  # solo testo o trattato non commerciale con parole doganali nel testo
    else:
        continue
    paesi = {NORM.get(p, p) for p in PAESI if re.search(r"\b" + re.escape(p), r["titolo"])}
    for m in re.finditer(r"italo-([a-zàèéìòù-]+)", t):
        paesi |= {v for x in m.group(1).split("-") for k, v in AGG.items() if x.startswith(k)}
    paesi = sorted(paesi)
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
