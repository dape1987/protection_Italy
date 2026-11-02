"""Export AKN del testo originario dei candidati. Uso: python export_pc.py SHARD N_SHARD"""
import csv, os, subprocess, sys, time
from normattiva import Normattiva

O = "normattiva/out/export_pc"
os.makedirs(O, exist_ok=True)
shard, n = int(sys.argv[1]), int(sys.argv[2])
righe = [r for i, r in enumerate(csv.DictReader(open("normattiva/candidati.csv", encoding="utf-8"))) if i % n == shard]
log = f"{O}/_log_{shard}.csv"


def salva(msg):
    subprocess.run(["git", "add", O], check=False)
    if subprocess.run(["git", "commit", "-qm", msg]).returncode:
        return
    for _ in range(5):
        subprocess.run(["git", "pull", "-q", "--rebase"], check=False)
        if subprocess.run(["git", "push", "-q"]).returncode == 0:
            return
        time.sleep(10)


fatti = 0
with Normattiva() as nt:
    for r in righe:
        dest = f"{O}/{r['codice_redazionale']}.zip"
        if os.path.exists(dest):
            continue
        a, m, g = map(int, r["data_emanazione"].split("-"))
        t0 = time.time()
        for tentativo in range(3):
            try:
                ex = nt.start_export(format="AKN", mode="originale", massimo_atti=5, denominazione=r["denominazione"],
                                     anno=a, numero=r["numero"], mese=m, giorno=g)
                ex.wait(timeout=1800)
                ex.save(dest)
                esito = f"ok,{time.time() - t0:.0f}s"
                break
            except Exception as e:
                esito = f"errore,{type(e).__name__}: {str(e)[:150]!r}"
                time.sleep(30)
        with open(log, "a", encoding="utf-8") as f:
            f.write(f"{r['codice_redazionale']},{esito}\n")
        fatti += 1
        if fatti % 25 == 0:
            salva(f"Normattiva: export candidati (shard {shard}, {fatti})")
        time.sleep(2)
salva(f"Normattiva: export candidati (shard {shard}, fine)")
