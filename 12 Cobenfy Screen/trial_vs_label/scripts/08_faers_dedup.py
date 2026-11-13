"""Deduplicate FAERS (latest caseversion per caseid across all quarters; drop caseids on any FDA deletion list),
then write case-level exposure flags and case-PT pairs for reports with any antipsychotic.
Usage: python -I 08_faers_dedup.py <faers_ext_dir> <out_data_dir>"""
import sys, glob, os, pandas as pd
ext, out = sys.argv[1], sys.argv[2]
rd = lambda pat: pd.concat([pd.read_csv(f, dtype=str, keep_default_na=False) for f in sorted(glob.glob(os.path.join(ext, pat)))], ignore_index=True)
demo = rd('*_demo.csv'); drug = rd('*_drug_ap.csv'); reac = rd('*_reac_ap.csv'); dele = set(rd('*_deleted.csv').caseid)
log = {'quarters': sorted(demo.quarter.unique()), 'demo_rows_all': len(demo)}
demo['cv'] = pd.to_numeric(demo.caseversion, errors='coerce').fillna(0); demo['pid'] = pd.to_numeric(demo.primaryid)
demo = demo.sort_values(['caseid', 'cv', 'fda_dt', 'pid'])
latest = demo.drop_duplicates('caseid', keep='last')
log['unique_caseids'] = len(latest); log['deleted_caseids_matched'] = int(latest.caseid.isin(dele).sum())
latest = latest[~latest.caseid.isin(dele)]
log['cases_after_dedup_and_deletion'] = len(latest)
drug = drug[drug.primaryid.isin(set(latest.primaryid))]
susp = drug[drug.role_cod.isin(['PS', 'SS'])]
NEWER = {'lumateperone', 'brexpiprazole', 'cariprazine'}
g_any = drug.groupby('primaryid').ingredient.agg(lambda s: ';'.join(sorted(set(s))))
g_susp = susp.groupby('primaryid').ingredient.agg(lambda s: ';'.join(sorted(set(s))))
cases = latest[latest.primaryid.isin(set(drug.primaryid))][['primaryid','caseid','caseversion','quarter','fda_dt','occp_cod','reporter_country','sex','age','age_cod']].copy()
cases['ap_any_role'] = cases.primaryid.map(g_any).fillna(''); cases['ap_suspect'] = cases.primaryid.map(g_susp).fillna('')
has = lambda col, ing: cases[col].str.split(';').apply(lambda L: ing in L)
cases['cobenfy_suspect'] = has('ap_suspect', 'xanomeline-trospium'); cases['cobenfy_any'] = has('ap_any_role', 'xanomeline-trospium')
cases['newer_ap_suspect'] = cases.ap_suspect.str.split(';').apply(lambda L: bool(NEWER & set(L)))
cases['other_ap_suspect'] = cases.ap_suspect.str.split(';').apply(lambda L: bool(set(L) - {'xanomeline-trospium', ''}))
cases['hcp'] = cases.occp_cod.isin(['MD', 'PH', 'OT', 'HP'])
cases.to_csv(os.path.join(out, 'faers_cases.csv.gz'), index=False)
reac = reac[reac.primaryid.isin(set(cases.primaryid))].drop_duplicates()
reac.to_csv(os.path.join(out, 'faers_case_pt.csv.gz'), index=False)
log.update(ap_cases=len(cases), cobenfy_suspect_cases=int(cases.cobenfy_suspect.sum()), cobenfy_any_cases=int(cases.cobenfy_any.sum()),
           newer_comparator_cases=int((cases.newer_ap_suspect & ~cases.cobenfy_any).sum()),
           all_ap_comparator_cases=int((cases.other_ap_suspect & ~cases.cobenfy_any).sum()), case_pt_rows=len(reac))
pd.Series(log).to_csv(os.path.join(out, 'faers_dedup_log.csv'), header=['value'])
print(log)
