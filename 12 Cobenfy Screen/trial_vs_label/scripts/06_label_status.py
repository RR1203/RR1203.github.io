"""Label status of every PT in the trial data and in term_groups.csv, against DailyMed SPL v6 (2026-08-21).
Status: 'Listed (6.1 Table 1)' / 'Listed (6.1 text)' / 'Mentioned elsewhere (<sections>)' / 'Missing'.
Each mapping gives the exact label wording; the script verifies the wording occurs in that section of the label text,
and records the first label version (v1 2024-09-26 ... v6) whose text contains it."""
import csv, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); R = lambda p: os.path.join(ROOT, p)
def sections(path):
    secs, cur = {}, None
    for ln in open(path).read().splitlines():
        m = re.match(r'^#+ (\d+(?:\.\d+)?) ', ln)
        if m: cur = m.group(1); secs.setdefault(cur, ''); continue
        if ln.startswith('# '): cur = 'other'
        if cur: secs[cur] = secs.get(cur, '') + '\n' + ln
    return secs
VERS = {v: sections(R(f'raw/label/label_v{v}.txt')) for v in (1, 3, 4, 5, 6)}
S = VERS[6]
T1 = S['6.1'][S['6.1'].index('Table 1:'):S['6.1'].index('Increases in Heart Rate In a dedicated')]
TXT61 = S['6.1'].replace(T1, '')
# PT -> list of (section, exact label wording). Section 'T1' = 6.1 Table 1 incl. footnotes.
MAP = {
 'Nausea':[('T1','Nausea')], 'Dyspepsia':[('T1','Dyspepsia')], 'Oesophageal discomfort':[('T1','esophageal discomfort')],
 'Constipation':[('T1','Constipation')], 'Vomiting':[('T1','Vomiting')], 'Hypertension':[('T1','Hypertension')],
 'Blood pressure increased':[('T1','blood pressure increased')], 'Labile hypertension':[('T1','labile hypertension')],
 'Orthostatic hypertension':[('T1','orthostatic hypertension')], 'Abdominal pain':[('T1','abdominal pain')],
 'Abdominal discomfort':[('T1','abdominal discomfort')], 'Abdominal pain upper':[('T1','abdominal pain upper')],
 'Abdominal pain lower':[('T1','abdominal pain lower')], 'Abdominal tenderness':[('T1','abdominal tenderness')],
 'Diarrhoea':[('T1','Diarrhea')], 'Tachycardia':[('T1','Tachycardia')], 'Heart rate increased':[('T1','heart rate increased')],
 'Sinus tachycardia':[('T1','sinus tachycardia')], 'Dizziness':[('T1','Dizziness')],
 'Gastrooesophageal reflux disease':[('T1','Gastroesophageal reflux disease')], 'Dry mouth':[('T1','Dry mouth')],
 'Somnolence':[('T1','Somnolence')], 'Vision blurred':[('T1','Vision blurred')], 'Salivary hypersecretion':[('T1','Salivary hypersecretion')],
 'Orthostatic hypotension':[('T1','Orthostatic hypotension')], 'Cough':[('T1','Cough')], 'Dyskinesia':[('T1','dyskinesia')],
 'Drooling':[('T1','drooling')], 'Dystonia':[('T1','dystonia')], 'Extrapyramidal disorder':[('T1','extrapyramidal disorder')],
 'Muscle contraction involuntary':[('T1','muscle contraction involuntary')], 'Muscle spasms':[('T1','muscle spasms')],
 'Urinary retention':[('6.1txt','urinary retention'),('5.1','urinary retention'),('10','urinary retention')],
 'Urinary hesitation':[('6.1txt','urinary hesitation'),('5.1','urinary hesitancy')], 'Dysuria':[('6.1txt','dysuria'),('5.1','dysuria')],
 'Urinary tract infection':[('6.1txt','urinary tract infections'),('5.8','urinary tract infection')],
 'Alanine aminotransferase increased':[('6.1txt','ALT or AST elevations'),('5.3','liver enzymes')],
 'Aspartate aminotransferase increased':[('6.1txt','ALT or AST elevations'),('5.3','liver enzymes')],
 'Gamma-glutamyltransferase increased':[('6.1txt','elevated liver enzymes'),('5.3','liver enzymes')],
 'Hepatic enzyme increased':[('6.1txt','elevated liver enzymes')], 'Transaminases increased':[('6.1txt','ALT or AST elevations')],
 'Liver function test increased':[('6.1txt','elevated liver enzymes')],
 'Blood bilirubin increased':[('6.1txt','increase in bilirubin')],
 'Hyperhidrosis':[('10','hyperhidrosis')], 'Ileus':[('10','ileus')], 'Agitation':[('10','agitation')],
 'Confusional state':[('5.9','confusion'),('6.2','confusion')], 'Hallucination':[('5.9','hallucinations'),('6.2','hallucinations')],
 'Hallucination, auditory':[('5.9','hallucinations')], 'Syncope':[('6.2','syncope')], 'Palpitations':[('6.2','palpitations')],
 'Angioedema':[('5.5','Angioedema'),('6.2','angioedema')], 'Rash':[('6.2','rash')], 'Dry eye':[('10','dry mouth and eyes')],
 'Cholelithiasis':[('5.3','gallstone')], 'Biliary colic':[('5.3','biliary')], 'Cholecystitis':[('5.3','gallbladder disorders')],
 'Cholecystitis acute':[('5.3','gallbladder disorders')], 'Seizure':[('10','seizures')], 'Hypotension':[('10','hypotension')],
 'Delirium':[('6.2','delirium'),('10','delirium')], 'Chest pain':[('6.2','chest pain')], 'Gastritis':[('6.2','gastritis')],
 'Sedation':[], 'Pruritus':[('5.3','pruritus')], 'Dysarthria':[('10','garbled speech')], 'Intestinal obstruction':[('5.4','gastrointestinal obstructive disorders')], 'Abdominal distension':[],
}
pts = set()
for r in csv.DictReader(open(R('pooled_ae.csv'))):
    if r['level'] == 'PT': pts.add(r['term'])
for r in csv.DictReader(open(R('term_groups.csv'))): pts.add(r['meddra_pt'])
for r in csv.DictReader(open(R('raw/ctgov_ae_long.csv'))):
    pts.add({'Diarrhea':'Diarrhoea','Gamma-Glutamyltransferase increased':'Gamma-glutamyltransferase increased'}.get(r['term'], r['term']))
def text_of(secs, s):
    if s == 'T1':
        t = secs['6.1']; return t[t.index('Table 1:'):t.index('Increases in Heart Rate In a dedicated')]
    if s == '6.1txt':
        t = secs['6.1']; return t.replace(t[t.index('Table 1:'):t.index('Increases in Heart Rate In a dedicated')], '')
    return secs.get(s, '')
out, problems = [], []
for p in sorted(pts):
    refs = MAP.get(p, [])
    for s, w in refs:
        if w.lower() not in text_of(S, s).lower(): problems.append((p, s, w))
    secs = [s for s, w in refs]
    if 'T1' in secs: st = 'Listed (6.1 Table 1)'
    elif '6.1txt' in secs: st = 'Listed (6.1 text, not Table 1)'
    elif secs: st = 'Mentioned elsewhere (' + ', '.join(sorted(set(secs))) + ')'
    else: st = 'Missing'
    first = ''
    if refs:
        s0, w0 = refs[0]
        for v in (1, 3, 4, 5, 6):
            if w0.lower() in text_of(VERS[v], s0).lower(): first = f'v{v}'; break
    out.append(dict(meddra_pt=p, label_status=st, label_wording=' ; '.join(f'{s}: "{w}"' for s, w in refs), first_label_version=first))
with open(R('label_status.csv'), 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(out[0])); w.writeheader(); w.writerows(out)
print('verification problems:', problems)
from collections import Counter; print(Counter(o['label_status'].split(' (')[0] for o in out), Counter(o['first_label_version'] for o in out))
