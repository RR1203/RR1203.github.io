# Download SDUD rows for buprenorphine-related product names via data.medicaid.gov datastore API.
import sys, json, csv, time, urllib.request, urllib.parse, os
OUT = sys.argv[1]
YEARS = [int(y) for y in sys.argv[2].split(",")] if len(sys.argv) > 2 else None
DS = {
 2018:"a1f3598e-fc71-51aa-8560-78e7e1a61b09",2019:"daba7980-e219-5996-9bec-90358fd156f1",
 2020:"cc318bfb-a9b2-55f3-a924-d47376b32ea3",2021:"eec7fbe6-c4c4-5915-b3d0-be5828ef4e9d",
 2022:"200c2cba-e58d-4a95-aa60-14b99736808d",2023:"d890d3a9-6b00-43fd-8b31-fcba4c8e2909",
 2024:"61729e5a-7aa8-448c-8903-ba3e0cd0ea3c",2025:"158a1baa-5506-400a-8ec3-97756f0b0536",
 2026:"2957a7f9-9a15-453e-9afd-3bbdcbac8fd3"}
TERMS = ["BUPREN","BUP","SUBOX","SUBUT","ZUBSO","BUNAV","SUBLOC","BRIXA","BUTRAN","BELBU"]
FIELDS = ["utilization_type","state","ndc","labeler_code","product_code","package_size","year","quarter","suppression_used","product_name","units_reimbursed","number_of_prescriptions","total_amount_reimbursed","medicaid_amount_reimbursed"]
def get(url):
    for i in range(4):
        try:
            with urllib.request.urlopen(url, timeout=180) as r: return json.load(r)
        except Exception as e:
            print("retry", i, e, file=sys.stderr); time.sleep(5*(i+1))
    raise RuntimeError(url)
seen=set()
with open(OUT,"w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=FIELDS,extrasaction="ignore"); w.writeheader()
    for yr,ds in DS.items():
        if YEARS and yr not in YEARS: continue
        for t in TERMS:
            off=0
            while True:
                q={"conditions[0][property]":"product_name","conditions[0][value]":t,"conditions[0][operator]":"starts with","limit":"5000","offset":str(off),"count":"true","schema":"false"}
                d=get(f"https://data.medicaid.gov/api/1/datastore/query/{ds}/0?"+urllib.parse.urlencode(q))
                rows=d["results"]
                for r in rows:
                    k=(r["utilization_type"],r["state"],r["ndc"],r["year"],r["quarter"])
                    if k in seen: continue
                    seen.add(k); w.writerow(r)
                print(yr,t,off,len(rows),d.get("count"),file=sys.stderr)
                off+=len(rows)
                if len(rows)<5000: break
