"""Parse ClinicalTrials.gov v2 adverseEventsModule into long format (one row per study x arm x term x seriousness)."""
import json, csv, sys, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STUDIES = {'NCT03697252':'EMERGENT-1','NCT04659161':'EMERGENT-2','NCT04738123':'EMERGENT-3',
           'NCT04659174':'EMERGENT-4','NCT04820309':'EMERGENT-5','NCT05145413':'ARISE',
           'NCT05643170':'PENNANT','NCT05919823':'UNITE-001 (China)','NCT06572449':'Slow-titration/food (NCT06572449)'}
rows = []
for nct, name in STUDIES.items():
    d = json.load(open(f'{ROOT}/raw/ctgov/{nct}.json'))
    ae = d['resultsSection']['adverseEventsModule']
    groups = {g['id']: g for g in ae['eventGroups']}
    thr = ae.get('frequencyThreshold')
    for kind in ('seriousEvents', 'otherEvents'):
        for e in ae.get(kind, []):
            for s in e['stats']:
                g = groups[s['groupId']]
                rows.append(dict(source='ClinicalTrials.gov', study=name, nct=nct, arm=g['title'],
                    arm_id=s['groupId'], n_arm=s.get('numAtRisk'), term=e['term'], organ_system=e.get('organSystem'),
                    event_type='serious' if kind=='seriousEvents' else 'other(non-serious)',
                    n_patients=s.get('numAffected'), n_events=s.get('numEvents'),
                    vocab=e.get('sourceVocabulary', ae.get('eventsVocabulary') if False else e.get('sourceVocabulary')),
                    threshold_pct=thr, source_location=f'https://clinicaltrials.gov/api/v2/studies/{nct} resultsSection.adverseEventsModule.{kind}'))
out = f'{ROOT}/raw/ctgov_ae_long.csv'
with open(out, 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
print(len(rows), 'rows ->', out)
