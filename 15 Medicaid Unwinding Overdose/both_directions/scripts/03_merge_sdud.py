# Merge SDUD pulls: 2018-2021 from the first pull, 2022-2026 from per-year pulls; dedupe on key.
import csv, sys, glob
out = sys.argv[1]; main = sys.argv[2]; parts = sorted(glob.glob(sys.argv[3]))
seen = set(); n = 0
with open(out + ".tmp", "w", newline="") as f:
    w = None
    for path, keep in [(main, lambda r: int(r["year"]) <= 2021)] + [(p, lambda r: True) for p in parts]:
        for r in csv.DictReader(open(path)):
            if not keep(r): continue
            k = (r["utilization_type"], r["state"], r["ndc"], r["year"], r["quarter"])
            if k in seen: continue
            seen.add(k)
            if w is None:
                w = csv.DictWriter(f, fieldnames=list(r.keys())); w.writeheader()
            w.writerow(r); n += 1
import os; os.replace(out + ".tmp", out); print(n)
