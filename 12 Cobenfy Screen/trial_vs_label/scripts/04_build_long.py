"""Build trial_ae_long.csv: every extracted AE count with its source.
Sources: ClinicalTrials.gov (raw/ctgov_ae_long.csv), journal tables parsed from JATS XML dumps,
label Table 1 (DailyMed SPL v6), EMERGENT-5 abstract (PubMed 41506001)."""
import csv, re, os, json, xml.etree.ElementTree as ET
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = lambda p: os.path.join(ROOT, p)
rows = []
COLS = ['source','study','nct','arm','n_arm','term_as_written','event_type','n_patients','pct_reported','source_location']

# 1. ClinicalTrials.gov
for r in csv.DictReader(open(R('raw/ctgov_ae_long.csv'))):
    rows.append(dict(source='ClinicalTrials.gov', study=r['study'], nct=r['nct'], arm=r['arm'], n_arm=r['n_arm'],
        term_as_written=r['term'], event_type=r['event_type'], n_patients=r['n_patients'], pct_reported='',
        source_location=r['source_location'] + f" (reporting threshold {r['threshold_pct']}%)"))

# 2. Journal tables: rows like "Term | 15 (17) | 3 (3)"
def table_rows(xmlfile, table_label):
    t = ET.parse(xmlfile)
    txt = lambda e: ' '.join(''.join(e.itertext()).split())
    for tw in t.iter('table-wrap'):
        lab = tw.find('label')
        if lab is not None and txt(lab).rstrip('.') == table_label:
            for tr in tw.iter('tr'):
                cells = [txt(c) for c in tr if c.tag in ('td', 'th')]
                if len(cells) == 3:
                    m1 = re.fullmatch(r'(\d+)(?: \(([\d.]+)\))?', cells[1]); m2 = re.fullmatch(r'(\d+)(?: \(([\d.]+)\))?', cells[2])
                    if m1 and m2: yield cells[0], m1.groups(), m2.groups()
PAPERS = [
  ('EMERGENT-1','NCT03697252','raw/europepmc/PMC7610870.xml','Table 3', 89, 90,
   'Brannan SK et al. NEJM 2021;384:717-26 (PMID 33626254, PMC7610870), Table 3'),
  ('EMERGENT-3','NCT04738123','raw/europepmc/PMC11063924.xml','Table 2', 125, 128,
   'Kaul I et al. JAMA Psychiatry 2024 (PMID 38691387, PMC11063924), Table 2'),
]
SKIP = re.compile(r'^(Any|Serious|Severe|TEAE|Adverse event leading)', re.I)
for study, nct, f, lab, n1, n0, cite in PAPERS:
    for term, a, b in table_rows(R(f), lab):
        if SKIP.search(term): continue
        term = re.sub(r'[a-z]$', '', term) if term.endswith('b') and term.startswith('Hypertension') else term
        for arm, n, (k, p) in (('Xanomeline-trospium', n1, a), ('Placebo', n0, b)):
            rows.append(dict(source='Journal article', study=study, nct=nct, arm=arm, n_arm=n, term_as_written=term,
                event_type='TEAE (paper table)', n_patients=k, pct_reported=p or '', source_location=cite))


# 2b. Phase 1 xanomeline alone vs xanomeline + trospium (healthy volunteers) and Bodick 1997 (secondary citation)
def tw_rows(xmlfile, table_label):
    t = ET.parse(xmlfile); txt = lambda e: ' '.join(''.join(e.itertext()).split())
    for tw in t.iter('table-wrap'):
        lab = tw.find('label')
        if lab is not None and txt(lab) == table_label:
            for tr in tw.iter('tr'): yield [txt(c) for c in tr if c.tag in ('td', 'th')]
CITE_P1 = 'Breier A et al. 2023 (PMID 37036495, PMC10102054)'
for cells in tw_rows(R('raw/europepmc/PMC10102054.xml'), 'Table 3'):
    m1 = re.fullmatch(r'(\d+) \(([\d.]+)\)', cells[1]) if len(cells) == 4 else None
    m2 = re.fullmatch(r'(\d+) \(([\d.]+)\)[a-z]?', cells[2]) if len(cells) == 4 else None
    if m1 and m2 and not cells[0].startswith('Any'):
        for arm, n, m in (('Xanomeline alone', 33, m1), ('Xanomeline + trospium', 35, m2)):
            rows.append(dict(source='Journal article', study='Phase 1 xanomeline vs xanomeline-trospium (healthy volunteers)', nct='NCT02831231',
                arm=arm, n_arm=n, term_as_written=cells[0], event_type='cholinergic TEAE (paper table)', n_patients=m.group(1),
                pct_reported=m.group(2), source_location=CITE_P1 + ', Table 3'))
for cells in tw_rows(R('raw/europepmc/PMC10102054.xml'), 'Table 5'):
    if len(cells) == 4 and re.fullmatch(r'-?\d+[a-z]?', cells[1]):
        rows.append(dict(source='Journal article (secondary citation)', study='Bodick 1997 Alzheimer trial, xanomeline 225 mg/day', nct='',
            arm='Xanomeline alone, high dose', n_arm=87, term_as_written=cells[0], event_type='placebo-adjusted incidence %', n_patients='',
            pct_reported=re.sub(r'[a-z]$', '', cells[1]), source_location=CITE_P1 + ', Table 5 (citing Bodick et al. 1997, Arch Neurol, PMID 9109749)'))

# 3. Label Table 1 (percentages only; pooled EMERGENT-2 + EMERGENT-3)
lab_txt = open(R('raw/label/label_v6.txt')).read().splitlines()
for ln in lab_txt:
    m = re.fullmatch(r'(.+?) \| (<?\d+)% \| (<?\d+)%', ln.strip())
    if m:
        for arm, n, p in (('COBENFY', 251, m.group(2)), ('Placebo', 253, m.group(3))):
            rows.append(dict(source='US label (DailyMed SPL v6, 2026-08-21)', study='EMERGENT-2+3 pooled', nct='NCT04659161;NCT04738123',
                arm=arm, n_arm=n, term_as_written=m.group(1), event_type='adverse reaction (label Table 1)', n_patients='',
                pct_reported=p, source_location='Section 6.1 Table 1, setid 8f0e73bf-6025-44f6-ab64-0983322de0df'))

# 4. EMERGENT-5 abstract (percentages)
ab = ET.parse(R('raw/pubmed/key_abstracts.xml'))
for a in ab.iter('PubmedArticle'):
    if a.findtext('.//PMID') == '41506001':
        s = ' '.join(''.join(x.itertext()) for x in a.iter('AbstractText'))
        s = s.replace('\u202f', ' ')
        seg = s[s.index('participants were ') + len('participants were '):]; seg = seg[:seg.index('. ')]
        for item in re.split(r', (?:and )?', seg):
            m = re.fullmatch(r'(.+?) \(([\d.]+) %(?: each)?\)', item.strip())
            for nm in m.group(1).split(' and '):
                rows.append(dict(source='Journal abstract', study='EMERGENT-5', nct='NCT04820309', arm='Xanomeline-trospium (open-label)',
                    n_arm=566, term_as_written=nm, event_type='TEAE >=5% (abstract)', n_patients='', pct_reported=m.group(2),
                    source_location='Kaul I et al. Schizophr Res 2026 (PMID 41506001), abstract'))
with open(R('trial_ae_long.csv'), 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=COLS); w.writeheader(); w.writerows(rows)
from collections import Counter
print(len(rows), Counter(r['source'] for r in rows))
