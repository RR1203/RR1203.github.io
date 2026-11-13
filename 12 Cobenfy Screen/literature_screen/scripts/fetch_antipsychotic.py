import json,sys
sys.path.insert(0,'scripts')
from conditions import BENEFIT
from pubmed_fetch import esearch,efetch
AP='(antipsychotic*[tiab] OR neuroleptic*[tiab] OR haloperidol[tiab] OR risperidone[tiab] OR olanzapine[tiab] OR quetiapine[tiab] OR aripiprazole[tiab] OR ziprasidone[tiab] OR lurasidone[tiab] OR clozapine[tiab])'
log=[];hits={}
for k,(lab,g,term) in BENEFIT.items():
    q=f'{term} AND {AP} AND (randomized controlled trial[pt] OR meta-analysis[pt]) AND humans[mh]'
    n,ids=esearch(q,retmax=4)
    log.append(dict(condition=k,evidence='0_antipsychotic_response',query=q,count=n,retrieved=ids))
    for p in ids: hits.setdefault(p,[]).append(k)
recs=efetch(list(hits))
items=[dict(pmid=p,title=r['title'],abstract=r['abstract'][:3000] or '(no abstract)',screen_for=[{'condition':c,'label':BENEFIT[c][0]} for c in hits[p]]) for p,r in recs.items()]
json.dump(items,open('extraction/batch_ap.json','w'),indent=0)
s=json.load(open('raw/search_log.json')); s+=log; json.dump(s,open('raw/search_log.json','w'),indent=1)
a=json.load(open('raw/abstracts.json'))
for p,r in recs.items(): a.setdefault(p,{**r,'hits':[]})['hits']+= [[c,'0_antipsychotic_response'] for c in hits[p]]
json.dump(a,open('raw/abstracts.json','w'),indent=1)
print(len(items),'abstracts',sum(len(i['screen_for']) for i in items),'pairs')
