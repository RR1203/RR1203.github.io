import json,re,csv,math,collections
import gzip; D=json.load(gzip.open('raw/faers_cobenfy_all.json.gz'))
R=D['reports']
COB=re.compile(r'XANOMELINE|COBENFY|KARXT',re.I)
PDIND=re.compile(r'PARKINSON|LEWY',re.I)
PDMEDS=re.compile(r'LEVODOPA|CARBIDOPA|SINEMET|RYTARY|DUOPA|STALEVO|PRAMIPEXOLE|MIRAPEX|ROPINIROLE|REQUIP|RASAGILINE|AZILECT|SAFINAMIDE|XADAGO|AMANTADINE|GOCOVRI|OSMOLEX|PIMAVANSERIN|NUPLAZID|ROTIGOTINE|NEUPRO|ENTACAPONE|OPICAPONE|ISTRADEFYLLINE|SELEGILINE',re.I)
MOTOR={'TREMOR','RESTING TREMOR','ESSENTIAL TREMOR','DYSTONIA','PARKINSONISM','EXTRAPYRAMIDAL DISORDER','MUSCLE RIGIDITY','COGWHEEL RIGIDITY','BRADYKINESIA','HYPOKINESIA','AKINESIA','FREEZING PHENOMENON','GAIT DISTURBANCE','GAIT INABILITY','FALL','BALANCE DISORDER','DYSKINESIA','AKATHISIA','PARKINSON\'S DISEASE','MOVEMENT DISORDER','MOBILITY DECREASED','OROMANDIBULAR DYSTONIA','TORTICOLLIS','OCULOGYRIC CRISIS','MUSCLE SPASMS','TARDIVE DYSKINESIA','ABNORMAL INVOLUNTARY MOVEMENTS','POSTURE ABNORMAL','DYSARTHRIA','DYSPHAGIA'}
EPS_CORE={'TREMOR','RESTING TREMOR','DYSTONIA','PARKINSONISM','EXTRAPYRAMIDAL DISORDER','MUSCLE RIGIDITY','COGWHEEL RIGIDITY','BRADYKINESIA','HYPOKINESIA','AKINESIA','FREEZING PHENOMENON','DYSKINESIA','AKATHISIA','PARKINSON\'S DISEASE','OROMANDIBULAR DYSTONIA','TORTICOLLIS','OCULOGYRIC CRISIS','TARDIVE DYSKINESIA','MOVEMENT DISORDER'}
GAITFALL={'FALL','GAIT DISTURBANCE','GAIT INABILITY','BALANCE DISORDER','MOBILITY DECREASED'}
PSY=re.compile(r'HALLUCINATION|PSYCHO|DELUSION|PARANOIA|DRUG INEFFECTIVE|THERAPEUTIC RESPONSE|CONDITION AGGRAVATED|SYMPTOM RECURRENCE|OFF LABEL|DRUG EFFECTIVE|THERAPEUTIC PRODUCT EFFECT|NO ADVERSE EVENT',re.I)
rows=[];allrows=[]
for r in R:
    drugs=r['patient'].get('drug',[])
    cob=[d for d in drugs if COB.search(d.get('medicinalproduct','')+' '+' '.join(x.get('activesubstancename','') for x in [d.get('activesubstance',{})] if x))]
    cob_suspect=any(d.get('drugcharacterization')=='1' for d in cob)
    inds=[d.get('drugindication','') for d in drugs if d.get('drugindication')]
    cob_ind=[d.get('drugindication','') for d in cob if d.get('drugindication')]
    others=[d.get('medicinalproduct','') for d in drugs if d not in cob]
    pdmeds=sorted({m.group(0).upper() for o in others for m in [PDMEDS.search(o)] if m}|{m.group(0).upper() for d in drugs if d not in cob for m in [PDMEDS.search(json.dumps(d.get('openfda',{}).get('generic_name',[])))] if m})
    pd_ind=any(PDIND.search(i) for i in inds)
    reac=[x.get('reactionmeddrapt','').upper() for x in r['patient'].get('reaction',[])]
    flag=pd_ind or bool(pdmeds)
    row=dict(safetyreportid=r['safetyreportid'],receivedate=r.get('receivedate'),country=r.get('occurcountry',''),reporter_qual=r.get('primarysource',{}).get('qualification','') if r.get('primarysource') else '',
        age=r['patient'].get('patientonsetage',''),age_unit=r['patient'].get('patientonsetageunit',''),sex={'1':'M','2':'F'}.get(r['patient'].get('patientsex',''),''),serious=r.get('serious',''),
        cobenfy_role='suspect' if cob_suspect else 'concomitant/other',cobenfy_indication='; '.join(sorted(set(cob_ind))),all_indications='; '.join(sorted(set(inds))),
        pd_indication=pd_ind,pd_comeds='; '.join(pdmeds),pd_flag=flag,
        motor_any=bool(set(reac)&MOTOR),eps_core=bool(set(reac)&EPS_CORE),gait_fall=bool(set(reac)&GAITFALL),
        motor_pts='; '.join(sorted(set(reac)&MOTOR)),psychosis_outcome_pts='; '.join(sorted({x for x in reac if PSY.search(x)})),all_reactions='; '.join(reac),
        other_drugs='; '.join(o for o in others if o))
    allrows.append(row)
pdr=[x for x in allrows if x['pd_flag']]
with open('faers_pd_reports.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(allrows[0].keys()));w.writeheader();w.writerows(pdr)
json.dump(allrows,open('raw/faers_cobenfy_rows.json','w'))
def ror(a,b,c,d):
    if min(a,b,c,d)==0: a,b,c,d=a+.5,b+.5,c+.5,d+.5; cc=True
    else: cc=False
    o=(a/b)/(c/d); se=math.sqrt(1/a+1/b+1/c+1/d)
    return o,math.exp(math.log(o)-1.96*se),math.exp(math.log(o)+1.96*se),cc
res={}
for scope,rows_ in [('all_reports',allrows),('cobenfy_suspect_only',[x for x in allrows if x['cobenfy_role']=='suspect'])]:
    pd=[x for x in rows_ if x['pd_flag']]; non=[x for x in rows_ if not x['pd_flag']]
    for k in ['motor_any','eps_core','gait_fall']:
        a=sum(x[k] for x in pd); b=len(pd)-a; c=sum(x[k] for x in non); d=len(non)-c
        o,l,h,cc=ror(a,b,c,d); res[f'{scope}|{k}']=dict(n_pd=len(pd),pd_events=a,n_other=len(non),other_events=c,ror=round(o,2),ci=[round(l,2),round(h,2)],haldane=cc)
json.dump(res,open('raw/faers_cobenfy_ror.json','w'),indent=1)
print('total',len(allrows),'suspect',sum(x['cobenfy_role']=='suspect' for x in allrows),'PD-flagged',len(pdr),'(indication',sum(x['pd_indication'] for x in pdr),', comeds',sum(bool(x['pd_comeds']) for x in pdr),')')
for k,v in res.items(): print(k,v)
for x in pdr: print(x['safetyreportid'],x['receivedate'],x['age'],x['sex'],x['cobenfy_role'],'|IND:',x['all_indications'][:90],'|MEDS:',x['pd_comeds'],'|MOTOR:',x['motor_pts'],'|PSY:',x['psychosis_outcome_pts'],'|ALL:',x['all_reactions'][:150])
