import json,urllib.request,urllib.parse,time,re
KW=re.compile(r'xanomeline|karxt|cobenfy|trospium|emraclidine|NBI-1117568|M4 (positive allosteric|PAM|agonist)|M1/M4',re.I)
PD=re.compile(r'parkinson|lewy|parkinsonism|dyskines|dystoni|extrapyramidal|catalep',re.I)
out=[];log=[]
for server,cats in [("medrxiv",["neurology","psychiatry and clinical psychology","pharmacology and therapeutics"]),("biorxiv",["neuroscience","pharmacology and toxicology"])]:
    for cat in cats:
        cur=0;n=0
        while True:
            u=f"https://api.biorxiv.org/details/{server}/2024-01-01/2026-11-13/{cur}?category={urllib.parse.quote(cat) if False else cat.replace(' ','_')}"
            for i in range(4):
                try: j=json.loads(urllib.request.urlopen(u,timeout=60).read());break
                except Exception as e: time.sleep(3); j=None
            if not j: log.append(dict(server=server,cat=cat,error=True,at=cur));break
            col=j.get('collection',[])
            for x in col:
                n+=1; txt=x.get('title','')+' '+x.get('abstract','')
                if KW.search(txt): out.append(dict(server=server,category=cat,doi=x['doi'],date=x['date'],title=x['title'],pd_related=bool(PD.search(txt)),abstract=x.get('abstract','')[:1500]))
            tot=int(j['messages'][0].get('total',0)) if j.get('messages') else 0
            cur+=len(col)
            if not col or cur>=tot: break
        log.append(dict(server=server,category=cat,scanned=n,total=tot))
        print(server,cat,n,flush=True)
json.dump(dict(log=log,hits=out),open('raw/biorxiv_scan.json','w'),indent=1)
print(len(out),'keyword hits',sum(x['pd_related'] for x in out),'PD-related')
