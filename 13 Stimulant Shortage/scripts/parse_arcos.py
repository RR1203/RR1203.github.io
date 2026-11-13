"""Parse ARCOS Retail Drug Summary Report 2 (grams by state x quarter x drug code)
from pdftotext -layout output. Usage: python3 -I parse_arcos.py <txt_dir> <out_csv>"""
import re, sys, glob, os, csv
txt_dir, out = sys.argv[1], sys.argv[2]
KEEP = {"1100", "1205", "1724", "1105"}
num = r"(-?[\d,]+(?:\.\d+)?)"
row_re = re.compile(r"^\s*([A-Z][A-Z .'\-]+?)\s{2,}" + r"\s+".join([num]*5) + r"\s*$")
rep_re = re.compile(r"ARCOS 3 - REPORT 0?(\d+)")
drug_re = re.compile(r"DRUG(?: CODE)?:\s*(\d{4})")
rows = []
for f in sorted(glob.glob(os.path.join(txt_dir, "*.txt"))):
    year = int(os.path.basename(f)[:4])
    rep, drug = None, None
    for line in open(f, encoding="utf-8", errors="ignore"):
        m = rep_re.search(line)
        if m: rep = int(m.group(1)); continue
        if rep != 2: continue
        m = drug_re.search(line)
        if m: drug = m.group(1); continue
        if drug not in KEEP: continue
        m = row_re.match(line)
        if m:
            st = m.group(1).strip()
            if "TOTAL" in st.upper() or st.startswith("STATE"): continue
            q = [float(x.replace(",", "")) for x in m.groups()[1:]]
            rows.append([year, drug, st] + q)
with open(out, "w", newline="") as fh:
    w = csv.writer(fh); w.writerow(["year","drug_code","state","q1","q2","q3","q4","total"]); w.writerows(rows)
print(len(rows), "rows")
