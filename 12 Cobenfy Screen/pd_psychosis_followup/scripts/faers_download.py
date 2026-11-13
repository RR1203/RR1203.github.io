import json,urllib.request,urllib.parse,time
Q='(patient.drug.activesubstance.activesubstancename:"XANOMELINE" OR patient.drug.medicinalproduct:"COBENFY" OR patient.drug.medicinalproduct:"XANOMELINE" OR patient.drug.openfda.generic_name:"XANOMELINE")'
recs={};skip=0
while True:
    u="https://api.fda.gov/drug/event.json?"+urllib.parse.urlencode({'search':Q,'limit':100,'skip':skip})
    for i in range(5):
        try: j=json.loads(urllib.request.urlopen(u,timeout=120).read());break
        except urllib.error.HTTPError as e:
            if e.code==404: j={'results':[]};break
            print('HTTP',e.code,e.read()[:200]); time.sleep(5)
    res=j.get('results',[])
    for r in res: recs[r['safetyreportid']]=r
    total=j.get('meta',{}).get('results',{}).get('total',0)
    print(skip,len(res),total,flush=True)
    skip+=100
    if not res or skip>=total: break
json.dump(dict(query=Q,total=total,retrieved=len(recs),last_updated=j.get('meta',{}).get('last_updated'),reports=list(recs.values())),open('raw/faers_cobenfy_all.json','w'))
print('unique',len(recs))
