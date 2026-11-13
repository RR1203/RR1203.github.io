import json,urllib.request,urllib.parse,csv,itertools
DRUGS=["xanomeline","KarXT","Cobenfy","xanomeline trospium","emraclidine","CVL-231","NBI-1117568","NBI-1117567","muscarinic agonist","muscarinic","M4 positive allosteric modulator","M1 positive allosteric modulator","TAK-071","MK-7622","HTL0016878","VU319","ML-007","KarX-EC","ANAVEX3-71","cevimeline"]
CONDS=["Parkinson Disease","Parkinson Disease Psychosis","Lewy Body Disease","Dementia with Lewy Bodies","Parkinsonism","Parkinson Disease Dementia"]
log=[];trials={}
def run(q):
    out=[];tok=None
    while True:
        p={**q,"pageSize":200,"format":"json"}
        if tok:p["pageToken"]=tok
        j=json.loads(urllib.request.urlopen("https://clinicaltrials.gov/api/v2/studies?"+urllib.parse.urlencode(p),timeout=60).read())
        out+=j.get("studies",[]);tok=j.get("nextPageToken")
        if not tok:return out
for d,c in itertools.product(DRUGS,CONDS):
    s=run({"query.intr":d,"query.cond":c})   # all statuses by default
    log.append(dict(query=f"query.intr={d} & query.cond={c}",hits=len(s)))
    for st in s:
        p=st["protocolSection"];n=p["identificationModule"]["nctId"]
        t=trials.setdefault(n,dict(nct=n,title=p["identificationModule"].get("briefTitle",""),conditions="; ".join(p.get("conditionsModule",{}).get("conditions",[])),interventions="; ".join(i.get("name","") for i in p.get("armsInterventionsModule",{}).get("interventions",[])),phase="; ".join(p.get("designModule",{}).get("phases",[]) or []),status=p["statusModule"].get("overallStatus",""),start=p["statusModule"].get("startDateStruct",{}).get("date",""),sponsor=p.get("sponsorCollaboratorsModule",{}).get("leadSponsor",{}).get("name",""),enrollment=p.get("designModule",{}).get("enrollmentInfo",{}).get("count",""),matched=set()))
        t["matched"].add(f"{d}|{c}")
# free-text sweep
for term in ["xanomeline AND parkinson","KarXT AND parkinson","cobenfy AND parkinson","xanomeline AND lewy","cobenfy AND lewy","muscarinic AND parkinson psychosis"]:
    s=run({"query.term":term});log.append(dict(query=f"query.term={term}",hits=len(s)))
    for st in s:
        p=st["protocolSection"];n=p["identificationModule"]["nctId"]
        t=trials.setdefault(n,dict(nct=n,title=p["identificationModule"].get("briefTitle",""),conditions="; ".join(p.get("conditionsModule",{}).get("conditions",[])),interventions="; ".join(i.get("name","") for i in p.get("armsInterventionsModule",{}).get("interventions",[])),phase="; ".join(p.get("designModule",{}).get("phases",[]) or []),status=p["statusModule"].get("overallStatus",""),start=p["statusModule"].get("startDateStruct",{}).get("date",""),sponsor=p.get("sponsorCollaboratorsModule",{}).get("leadSponsor",{}).get("name",""),enrollment=p.get("designModule",{}).get("enrollmentInfo",{}).get("count",""),matched=set()))
        t["matched"].add("term:"+term)
for t in trials.values():t["matched"]="; ".join(sorted(t["matched"]))
with open("trials_pd.csv","w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=list(next(iter(trials.values())).keys()) if trials else ["nct"]);w.writeheader();w.writerows(trials.values())
json.dump(log,open("raw/ctgov_log.json","w"),indent=1)
for t in trials.values(): print(t["nct"],t["status"],t["phase"],"|",t["conditions"][:50],"|",t["interventions"][:50],"|",t["title"][:60])
print(sum(1 for x in log if x['hits']),'queries with hits of',len(log))
