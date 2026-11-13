import json,csv,matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
cells=json.load(open('raw/score_cells.json'))
sc={r['condition']:r for r in csv.DictReader(open('condition_scores.csv'))}
TYPES=['0_antipsychotic_response','1_human_pharm','2_anticholinergic_burden','3_genetics','4_postmortem_imaging','5_animal','6_clinical_obs']
TL=['Antipsychotic\nresponse','Human\npharmacology','Anticholinergic\nburden','Genetics','Postmortem /\nimaging','Animal','Clinical obs.\n(xanomeline)']
order=sorted(sc,key=lambda c:(float(sc[c]['harm_score'])-float(sc[c]['benefit_score'])))
fig,ax=plt.subplots(figsize=(9,0.27*len(order)+1.5))
for y,c in enumerate(order):
    for x,t in enumerate(TYPES):
        h=next((d for d in cells if d['condition']==c and d['type']==t and d['want']=='helps' and d['weight']>0),None)
        m=next((d for d in cells if d['condition']==c and d['type']==t and d['want']=='harms' and d['weight']>0),None)
        if h: ax.scatter(x,y,s=60*h['weight']+15,c='#1f77b4',alpha=.85)
        if m: ax.scatter(x+(0.18 if h else 0),y,s=60*m['weight']+15,c='#d62728',alpha=.85)
ax.set_yticks(range(len(order)));GAP={'chronic_pain','cocaine','copd','delirium','chemo_brain','methamphetamine'}
ax.set_yticklabels([f"{sc[c]['label']}{' *' if c in GAP else ''}  [{sc[c]['status'].split(' (')[0]}]" for c in order],fontsize=7)
ax.set_xticks(range(len(TYPES)));ax.set_xticklabels(TL,fontsize=7);ax.xaxis.tick_top()
ax.set_xlim(-.6,len(TYPES)-.4);ax.set_ylim(-.6,len(order)-.4);ax.grid(alpha=.2)
ax.scatter([],[],c='#1f77b4',label='More M1/M4 signalling predicted to HELP');ax.scatter([],[],c='#d62728',label='Predicted to HARM')
ax.legend(loc='lower center',bbox_to_anchor=(.5,-0.06),ncol=2,fontsize=7,frameon=False)
ax.set_title('Evidence map: conditions × evidence types (dot size = weight; halved for tiny/contradictory)\n* = most abstracts not extracted (extraction batch blocked); empty rows are NOT evidence of absence',fontsize=8,pad=40)
plt.tight_layout();plt.savefig('figures/evidence_heatmap.png',dpi=200);print('ok')
