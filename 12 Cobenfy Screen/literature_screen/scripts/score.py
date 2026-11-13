import json,glob,csv,sys,collections
sys.path.insert(0,'scripts'); from conditions import BENEFIT,HARM
LAB={**{k:v[0] for k,v in BENEFIT.items()},**{k:v[0] for k,v in HARM.items()}}
GRP={**{k:v[1] for k,v in BENEFIT.items()},**{k:v[1] for k,v in HARM.items()}}
abst=json.load(open('raw/abstracts.json'))
rows=[json.loads(l) for f in sorted(glob.glob('extraction/out_*.jsonl')) for l in open(f) if l.strip()]
override=json.load(open('extraction/spotcheck_overrides.json')) if glob.glob('extraction/spotcheck_overrides.json') else {}
for r in rows:
    k=f"{r['pmid']}|{r['condition']}"
    if k in override: r.update(override[k]); r['spotcheck_corrected']=True
rel=[r for r in rows if r.get('relevant') and r.get('evidence_type')]
TYPES=['0_antipsychotic_response','1_human_pharm','2_anticholinergic_burden','3_genetics','4_postmortem_imaging','5_animal','6_clinical_obs']
HUMAN=set(TYPES)-{'5_animal'}
STRONG_ST={'RCT','meta-analysis','crossover','cohort','case-control','GWAS','MR','postmortem','PET'}
def type_call(items,want):
    """direction call for one condition x type. Returns (weight_multiplier, n_for, n_against)"""
    f=[i for i in items if i['direction']==want]
    opp='harms' if want=='helps' else 'helps'
    a=[i for i in items if i['direction'] in (opp,'null')]
    against=sum(1 if i['direction']==opp else 0.5 for i in a)        # v2: a null counts half against
    if not f or len(f)<=len([i for i in items if i['direction']==opp]): return 0,len(f),len(a)
    mult=1.0
    if against>=len(f): mult*=0.5                                  # contradictory
    big=[i for i in f if (i.get('n') or 0)>=20 or i.get('study_type') in STRONG_ST]
    if not big and all(i['evidence_type']!='5_animal' for i in f): mult*=0.5   # only tiny / anecdotal human studies
    return mult,len(f),len(a)
STATUS={
 'ad_psychosis':('in trials','KarXT Ph3 ADEPT program: NCT05511363, NCT06126224, NCT05980949; agitation NCT06937229'),
 'dementia_cognition':('in trials','xanomeline AD RCT (PMID 9109749, 9339268); KarXT AD trials NCT07011732, NCT07011745, NCT07212062'),
 'bipolar_mania':('in trials','KarXT Ph3 NCT06951698, NCT06951711, NCT07140913; NBI-1117568 Ph2 NCT07288320'),
 'autism_irritability':('in trials','KarXT Ph3 NCT07284745, NCT07285798'),
 'cocaine':('in trials','Cobenfy Ph1/2 NCT07624227'),
 'schizophrenia_cog':('tested (approved population)','KarXT post hoc PMID 36414626; NCT07084831 withdrawn'),
 'epilepsy':('in trials (memory, not seizures)','NCT07228338, NCT07721272 mechanistic memory studies in epilepsy surgery pts'),
 'pd_psychosis':('untested (1 case report)','PMID 42729706'),
 'ocd':('untested (1 case report)','PMID 42069559 (clozapine-induced obsessions)'),
 'catatonia':('untested (case discussion)','PMID 42579811'),
 'pd_cognition':('untested (M1 PAM TAK-071 tested)','NCT04334317 (TAK-071, not Cobenfy)'),
 'drug_parkinsonism':('safety outcome in EMERGENT trials',''),'dystonia':('safety outcome in EMERGENT trials',''),
 'sialorrhea':('observed adverse effect',''),'hyperhidrosis':('observed adverse effect',''),'bradycardia':('safety data in trials',''),
}
search=json.load(open('raw/search_log.json'))
TOTAL={s['condition']:s['count'] for s in search if s['evidence']=='TOTAL_LITERATURE'}
out=[];cells=[]
for c in LAB:
    items=[r for r in rel if r['condition']==c]
    res={}
    for want in ('helps','harms'):
        score=0;human=0;types=[]
        hum_present=any(i['direction']==want and i['evidence_type'] in HUMAN for i in items)
        for t in TYPES:
            it=[i for i in items if i['evidence_type']==t]
            m,nf,na=type_call(it,want)
            if m==0: continue
            if t=='5_animal' and not hum_present: m=0   # animal counts only alongside human
            w=(2 if t in HUMAN else 1)*m
            if w>0:
                score+=w; types.append(t)
                if t in HUMAN and m==1.0: human+=1
                elif t in HUMAN: human+=0.5
            if want=='helps' or True: cells.append(dict(condition=c,type=t,want=want,weight=w,n_for=nf,n_against=na))
        res[want]=(score,human,types)
    peri=sum(1 for i in items if i.get('peripheral') and i['direction'] in('helps','harms'))
    out.append(dict(condition=c,label=LAB[c],group=GRP[c],status=STATUS.get(c,('untested',''))[0],status_source=STATUS.get(c,('',''))[1],
        benefit_score=res['helps'][0],benefit_human_types=res['helps'][1],benefit_types=';'.join(res['helps'][2]),
        harm_score=res['harms'][0],harm_human_types=res['harms'][1],harm_types=';'.join(res['harms'][2]),
        n_relevant=len(items),n_peripheral=peri,total_pubmed_papers=TOTAL.get(c)))
json.dump(cells,open('raw/score_cells.json','w'),indent=0)
with open('condition_scores.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(out[0].keys()));w.writeheader();w.writerows(sorted(out,key=lambda x:-x['benefit_score']))
# evidence csv
with open('condition_evidence.csv','w',newline='') as f:
    fn=['condition','label','evidence_type','direction','study_type','n','drug_or_exposure','finding','pmid','doi','year','xanomeline_tested','peripheral','spotcheck_corrected']
    w=csv.DictWriter(f,fieldnames=fn,extrasaction='ignore');w.writeheader()
    for r in sorted(rel,key=lambda r:(r['condition'],r['evidence_type'])):
        a=abst.get(r['pmid'],{})
        w.writerow({**r,'label':LAB[r['condition']],'doi':a.get('doi',''),'year':a.get('year','')})
for o in sorted(out,key=lambda x:-x['benefit_score']):
    print(f"{o['benefit_score']:4.1f} h{o['benefit_human_types']:<3} harm{o['harm_score']:4.1f} {o['condition']:20} {o['status'][:22]:22} {o['benefit_types']}  | {o['total_pubmed_papers']}")
