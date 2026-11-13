import json,urllib.request,urllib.parse,time,math
def total(q):
    u="https://api.fda.gov/drug/event.json?"+urllib.parse.urlencode({'search':q,'limit':1})
    for i in range(5):
        try: return json.loads(urllib.request.urlopen(u,timeout=60).read())['meta']['results']['total']
        except urllib.error.HTTPError as e:
            if e.code==404: return 0
            time.sleep(3)
    raise RuntimeError(q)
MOTOR=['TREMOR','RESTING TREMOR','ESSENTIAL TREMOR','DYSTONIA','PARKINSONISM','EXTRAPYRAMIDAL DISORDER','MUSCLE RIGIDITY','COGWHEEL RIGIDITY','BRADYKINESIA','HYPOKINESIA','AKINESIA','FREEZING PHENOMENON','GAIT DISTURBANCE','GAIT INABILITY','FALL','BALANCE DISORDER','DYSKINESIA','AKATHISIA',"PARKINSON'S DISEASE",'MOVEMENT DISORDER','MOBILITY DECREASED','OROMANDIBULAR DYSTONIA','TORTICOLLIS','OCULOGYRIC CRISIS','MUSCLE SPASMS','TARDIVE DYSKINESIA','ABNORMAL INVOLUNTARY MOVEMENTS','POSTURE ABNORMAL','DYSARTHRIA','DYSPHAGIA']
EPS=['TREMOR','RESTING TREMOR','DYSTONIA','PARKINSONISM','EXTRAPYRAMIDAL DISORDER','MUSCLE RIGIDITY','COGWHEEL RIGIDITY','BRADYKINESIA','HYPOKINESIA','AKINESIA','FREEZING PHENOMENON','DYSKINESIA','AKATHISIA',"PARKINSON'S DISEASE",'OROMANDIBULAR DYSTONIA','TORTICOLLIS','OCULOGYRIC CRISIS','TARDIVE DYSKINESIA','MOVEMENT DISORDER']
def rq(lst): return '('+' OR '.join(f'patient.reaction.reactionmeddrapt.exact:"{x}"' for x in lst)+')'
PD='(patient.drug.drugindication:parkinson OR patient.drug.drugindication:parkinsonism OR patient.drug.drugindication:"lewy")'
DR={'pimavanserin':'patient.drug.openfda.generic_name:"PIMAVANSERIN"','quetiapine':'patient.drug.openfda.generic_name:"QUETIAPINE"','xanomeline-trospium':'(patient.drug.activesubstance.activesubstancename:"XANOMELINE" OR patient.drug.medicinalproduct:"COBENFY")'}
out={}
for name,dq in DR.items():
    n_all=total(dq); n_pd=total(f'{dq} AND {PD}')
    r={'n_all':n_all,'n_pd':n_pd,'n_nonpd':n_all-n_pd}
    for lab,L in [('motor_any',MOTOR),('eps_core',EPS)]:
        a=total(f'{dq} AND {PD} AND {rq(L)}'); call=total(f'{dq} AND {rq(L)}'); c=call-a
        b=n_pd-a; d=(n_all-n_pd)-c
        hal=min(a,b,c,d)==0
        A,B,C,Dd=[x+.5 if hal else x for x in (a,b,c,d)]
        o=(A/B)/(C/Dd); se=math.sqrt(1/A+1/B+1/C+1/Dd)
        r[lab]=dict(pd_events=a,pd_pct=round(100*a/n_pd,1) if n_pd else None,nonpd_events=c,nonpd_pct=round(100*c/(n_all-n_pd),1) if n_all-n_pd else None,ror_pd_vs_nonpd=round(o,2),ci=[round(math.exp(math.log(o)-1.96*se),2),round(math.exp(math.log(o)+1.96*se),2)],haldane=hal)
        time.sleep(.3)
    out[name]=r; print(name,json.dumps(r))
json.dump(dict(note='report-level openFDA counts; PD = any drug indication text matching parkinson/parkinsonism/lewy; drug present in any role',pd_query=PD,results=out),open('raw/faers_reference.json','w'),indent=1)
