import json, urllib.parse, urllib.request, time, csv, sys
def get(url, data=None, hdr=None):
    for i in range(4):
        try:
            req=urllib.request.Request(url, data=data, headers=hdr or {})
            with urllib.request.urlopen(req, timeout=60) as r: return r.read()
        except Exception as e: err=e; time.sleep(2*(i+1))
    raise err
log=[]
# --- ClinicalTrials.gov v2 ---
DRUGS=["xanomeline","KarXT","Cobenfy","emraclidine","CVL-231","NBI-1117568","cevimeline","pilocarpine","bethanechol","M1 positive allosteric modulator","M4 positive allosteric modulator","muscarinic agonist","HTL0016878","NBI-1117567","MK-7622","TAK-071","VU319","ML-007"]
trials={}
for d in DRUGS:
    tok=None; n=0
    while True:
        q={"query.intr":d,"pageSize":200,"format":"json"}
        if tok: q["pageToken"]=tok
        j=json.loads(get("https://clinicaltrials.gov/api/v2/studies?"+urllib.parse.urlencode(q)))
        for s in j.get("studies",[]):
            p=s["protocolSection"]; nct=p["identificationModule"]["nctId"]
            t=trials.setdefault(nct,dict(nct=nct,title=p["identificationModule"].get("briefTitle",""),
              conditions="; ".join(p.get("conditionsModule",{}).get("conditions",[])),
              interventions="; ".join(i.get("name","") for i in p.get("armsInterventionsModule",{}).get("interventions",[])),
              phase="; ".join(p.get("designModule",{}).get("phases",[]) or []),
              status=p["statusModule"].get("overallStatus",""),
              start=p["statusModule"].get("startDateStruct",{}).get("date",""),
              sponsor=p.get("sponsorCollaboratorsModule",{}).get("leadSponsor",{}).get("name",""),
              enrollment=p.get("designModule",{}).get("enrollmentInfo",{}).get("count",""),
              has_results=s.get("hasResults",False), matched_query=[]))
            t["matched_query"].append(d); n+=1
        tok=j.get("nextPageToken")
        if not tok: break
    log.append(dict(source="ClinicalTrials.gov v2",query=f"query.intr={d}",count=n))
for t in trials.values(): t["matched_query"]="; ".join(sorted(set(t["matched_query"])))
with open("trials.csv","w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=list(next(iter(trials.values())).keys())); w.writeheader(); w.writerows(sorted(trials.values(),key=lambda x:(x["matched_query"],x["start"])))
# --- Europe PMC xanomeline/Cobenfy x condition counts ---
sys.path.insert(0,"scripts"); from conditions import BENEFIT,HARM
EPMC_TERMS={k:v[0].split("(")[0].split("/")[0].strip() for k,v in {**BENEFIT,**HARM}.items()}
EPMC_TERMS.update({"ad_psychosis":'alzheimer AND (psychosis OR agitation)',"dementia_cognition":'alzheimer AND cognition',"pd_psychosis":'parkinson AND psychosis',"pd_cognition":'parkinson AND (cognitive OR dementia)',"autism_irritability":"autism","binge_eating":'("binge eating" OR obesity)',"cocaine":"cocaine","methamphetamine":"methamphetamine","alcohol":"alcohol","nicotine":"nicotine","chronic_pain":"pain","sleep":"(sleep OR narcolepsy)","post_stroke":"stroke","long_covid":'("long COVID" OR "post-COVID")',"chemo_brain":'chemotherapy AND cognitive',"tbi":'"traumatic brain injury"',"pd_tremor":"parkinson AND tremor","drug_parkinsonism":"(extrapyramidal OR parkinsonism)","bradycardia":"bradycardia","peptic_ulcer":'(ulcer OR reflux)',"sjogren":'(sjogren OR xerostomia)',"schizophrenia_cog":'schizophrenia AND cognition',"down_syndrome":'"down syndrome"',"tardive":'"tardive dyskinesia"',"tourette":"(tourette OR tic)","ocd":'"obsessive compulsive"',"mdd":'(depression OR depressive)',"bipolar_mania":'(mania OR bipolar)',"bipolar_depression":'"bipolar depression"',"anorexia":'"anorexia nervosa"',"borderline":'"borderline personality"',"dlb":'"lewy body"'})
epmc={}
for k,t in EPMC_TERMS.items():
    q=f'(xanomeline OR KarXT OR Cobenfy OR "xanomeline-trospium") AND {t}'
    j=json.loads(get("https://www.ebi.ac.uk/europepmc/webservices/rest/search?"+urllib.parse.urlencode({"query":q,"format":"json","pageSize":25,"resultType":"lite"})))
    epmc[k]=dict(query=q,count=j["hitCount"],top=[dict(id=r.get("pmid") or r.get("id"),title=r.get("title"),year=r.get("pubYear")) for r in j["resultList"]["result"]])
    log.append(dict(source="Europe PMC",query=q,count=j["hitCount"])); time.sleep(0.2)
json.dump(epmc,open("raw/europepmc_xanomeline.json","w"),indent=1)
# --- Open Targets genetics ---
GENES={"CHRM1":"ENSG00000168539","CHRM2":"ENSG00000181072","CHRM3":"ENSG00000133019","CHRM4":"ENSG00000180720","CHRM5":"ENSG00000184984"}
Q="""query($id:String!){target(ensemblId:$id){approvedSymbol associatedDiseases(page:{index:0,size:300}){count rows{disease{id name} score datatypeScores{id score}}}}}"""
ot={}
for g,e in GENES.items():
    j=json.loads(get("https://api.platform.opentargets.org/api/v4/graphql",json.dumps({"query":Q,"variables":{"id":e}}).encode(),{"Content-Type":"application/json"}))
    rows=j["data"]["target"]["associatedDiseases"]["rows"]
    ot[g]=[dict(disease=r["disease"]["name"],efo=r["disease"]["id"],overall=r["score"],genetic=next((d["score"] for d in r["datatypeScores"] if d["id"]=="genetic_association"),0),literature=next((d["score"] for d in r["datatypeScores"] if d["id"]=="literature"),0),known_drug=next((d["score"] for d in r["datatypeScores"] if d["id"]=="known_drug"),0)) for r in rows]
    log.append(dict(source="Open Targets",query=f"{g} associatedDiseases",count=len(rows)))
json.dump(ot,open("raw/opentargets.json","w"),indent=1)
# --- GWAS Catalog ---
gw={}
for g in GENES:
    try:
        j=json.loads(get(f"https://www.ebi.ac.uk/gwas/rest/api/v2/associations?mapped_gene={g}&size=200"))
        a=j.get("_embedded",{}).get("associations",[])
        gw[g]=[dict(trait=", ".join(x.get("efo_traits",[{}])[0].get("efo_trait","") for _ in [0]) if x.get("efo_traits") else x.get("reported_trait"),p=x.get("p_value"),pubmed=x.get("pubmed_id"),snp=x.get("snp_effect_allele")) for x in a]
        log.append(dict(source="GWAS Catalog v2",query=f"associations?mapped_gene={g}",count=j.get("page",{}).get("totalElements",len(a))))
    except Exception as e:
        log.append(dict(source="GWAS Catalog v2",query=f"mapped_gene={g}",count=f"ERROR {e}"))
json.dump(gw,open("raw/gwas_catalog.json","w"),indent=1)
json.dump(log,open("raw/clinical_genetics_log.json","w"),indent=1)
print(len(trials),"trials")
