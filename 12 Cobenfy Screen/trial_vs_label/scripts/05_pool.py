"""Harmonise terms, build PT- and group-level counts per trial-arm, and pool placebo-controlled trials
with a Mantel-Haenszel risk difference (Greenland-Robins variance, no continuity correction).
Primary input: ClinicalTrials.gov rows (patient counts; 'other' + 'serious' summed per PT)."""
import csv, os, math, re
from collections import defaultdict
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); R = lambda p: os.path.join(ROOT, p)
SYN = {'Diarrhea':'Diarrhoea','Increased weight':'Weight increased','Increased γ-glutamyltransferase level':'Gamma-glutamyltransferase increased',
       'Gamma-Glutamyltransferase increased':'Gamma-glutamyltransferase increased','Gastroesophageal reflux disease':'Gastrooesophageal reflux disease'}
def pt(t): t = t.strip(); t = SYN.get(t, t); return t[0].upper() + t[1:]
TRIALS = {  # placebo-controlled trials: arm ids (active, placebo)
  'EMERGENT-1': ('EG000','EG001'), 'EMERGENT-2': ('EG000','EG001'), 'EMERGENT-3': ('EG000','EG001'),
  'UNITE-001 (China)': ('EG000','EG001'), 'ARISE': ('EG000','EG001')}
cnt = defaultdict(int); N = {}; reported = defaultdict(set); thr = {}
for r in csv.DictReader(open(R('raw/ctgov_ae_long.csv'))):
    if r['study'] not in TRIALS: continue
    act, pbo = TRIALS[r['study']]
    if r['arm_id'] not in (act, pbo): continue
    arm = 'active' if r['arm_id'] == act else 'placebo'
    N[(r['study'], arm)] = int(r['n_arm']); thr[r['study']] = r['threshold_pct']
    p = pt(r['term']); cnt[(r['study'], arm, p)] += int(r['n_patients'])
    reported[p].add(r['study'])
groups = defaultdict(list)
for g in csv.DictReader(open(R('term_groups.csv'))): groups[g['group']].append(g['meddra_pt'])

def mh_rd(strata):
    """strata: list of (a, n1, c, n0). Returns RD, lo, hi (MH weights, Greenland-Robins/Sato variance)."""
    W = sum(n1*n0/(n1+n0) for a,n1,c,n0 in strata)
    rd = sum((a*n0 - c*n1)/(n1+n0) for a,n1,c,n0 in strata) / W
    # Sato (1989) / Greenland-Robins variance as used by RevMan and metafor::rma.mh(measure='RD')
    var = sum((a*(n1-a)*n0**3 + c*(n0-c)*n1**3)/(n1*n0*(n1+n0)**2) for a,n1,c,n0 in strata) / W**2
    se = math.sqrt(var); return rd, rd - 1.96*se, rd + 1.96*se

POOLS = {'E123': ['EMERGENT-1','EMERGENT-2','EMERGENT-3'], 'E23_label': ['EMERGENT-2','EMERGENT-3'],
         'E123_China': ['EMERGENT-1','EMERGENT-2','EMERGENT-3','UNITE-001 (China)'], 'ARISE_adjunctive': ['ARISE']}
items = [('PT', p, [p]) for p in sorted(reported)] + [('group', g, pts) for g, pts in groups.items()]
out = []
for level, name, pts in items:
    for pool, trials in POOLS.items():
        for method in ('available_case', 'unreported_as_zero') + (('group_max',) if level == 'group' else ()):
            strata, contrib = [], []
            for t in trials:
                rep = any(t in reported.get(p, ()) for p in pts)
                if not rep and method != 'unreported_as_zero': continue
                n1, n0 = N[(t,'active')], N[(t,'placebo')]
                agg = max if method == 'group_max' else sum
                a = min(n1, agg([cnt[(t,'active',p)] for p in pts])); c = min(n0, agg([cnt[(t,'placebo',p)] for p in pts]))
                strata.append((a,n1,c,n0)); contrib.append(t if rep else t + '(0 imputed)')
            if not strata: continue
            A = sum(s[0] for s in strata); N1 = sum(s[1] for s in strata); C = sum(s[2] for s in strata); N0 = sum(s[3] for s in strata)
            if A + C == 0: continue
            rd, lo, hi = mh_rd(strata)
            out.append(dict(level=level, term=name, pool=pool, method=method, trials=';'.join(contrib), n_trials=len(strata),
                events_active=A, n_active=N1, pct_active=round(100*A/N1,2), events_placebo=C, n_placebo=N0, pct_placebo=round(100*C/N0,2),
                rd_pct=round(100*rd,2), rd_lo_pct=round(100*lo,2), rd_hi_pct=round(100*hi,2)))
with open(R('pooled_ae.csv'),'w',newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(out[0])); w.writeheader(); w.writerows(out)
print(len(out), 'rows; thresholds', thr, {k:v for k,v in N.items()})
