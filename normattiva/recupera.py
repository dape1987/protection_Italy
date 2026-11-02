"""Ripete le ricerche incomplete di universo.py (dichiarati != scaricati) e aggiunge le righe mancanti."""
import calendar, csv, sys, time
sys.path.insert(0, "normattiva")
from universo_lib import cerca, CAMPI  # noqa: E402

O = "normattiva/out/universo"
tot = list(csv.reader(open(f"{O}/_totali.csv", encoding="utf-8")))
for i, (ric, per, dich, scar) in enumerate(tot[1:], 1):
    if dich == scar:
        continue
    if ric == "tutti":
        a, m = map(int, per.split("-"))
        d, rr = cerca({}, f"{per}-01", f"{per}-{calendar.monthrange(a, m)[1]}")
        dest, extra = f"{O}/atti_1926_1939.csv", {}
    else:
        d, rr = cerca({"testoRicerca": ric}, f"{per}-01-01", f"{per}-12-31")
        dest, extra = f"{O}/testo.csv", {"parola": ric}
    with open(dest, "a", newline="", encoding="utf-8") as f:
        csv.DictWriter(f, (["parola"] if extra else []) + CAMPI).writerows({**extra, **r} for r in rr)
    tot[i] = [ric, per, str(d), str(len(rr))]
    time.sleep(2)
with open(f"{O}/_totali.csv", "w", newline="", encoding="utf-8") as f:
    csv.writer(f, lineterminator="\n").writerows(tot)
