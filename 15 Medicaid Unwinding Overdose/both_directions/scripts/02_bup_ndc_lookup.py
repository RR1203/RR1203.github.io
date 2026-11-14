# Build buprenorphine product-NDC lookup (labeler-product, 5-4) from FDA NDC directory (current + excluded).
import sys, zipfile, csv, io
fda, out = sys.argv[1], sys.argv[2]
rows = []
for z, f in [("ndctext.zip","product.txt"),("ndc_excluded.zip","Products_excluded.txt")]:
    with zipfile.ZipFile(f"{fda}/{z}") as zz:
        txt = zz.read(f).decode("latin-1")
    for r in csv.DictReader(io.StringIO(txt), delimiter="\t"):
        if "BUPRENORPHINE" in (r.get("SUBSTANCENAME") or "").upper():
            lab, prod = r["PRODUCTNDC"].split("-")
            rows.append({"labeler_code": lab.zfill(5), "product_code": prod.zfill(4), "source": f,
                         "proprietary": r["PROPRIETARYNAME"], "nonproprietary": r["NONPROPRIETARYNAME"],
                         "dosage_form": r["DOSAGEFORMNAME"], "route": r["ROUTENAME"], "substance": r["SUBSTANCENAME"]})
seen = {}
for r in rows:
    seen.setdefault((r["labeler_code"], r["product_code"]), r)
with open(out, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(seen.values())
print(len(seen))
