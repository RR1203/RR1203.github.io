"""Per FAERS quarter: keep all DEMO rows, DRUG rows naming an antipsychotic, REAC rows of those reports, and the deletion list.
Usage: python -I 07_faers_extract.py <quarter_dir> <out_dir>"""
import sys, os, re, glob, pandas as pd
qdir, out = sys.argv[1], sys.argv[2]; os.makedirs(out, exist_ok=True); q = os.path.basename(qdir.rstrip('/'))
AP = {  # active ingredient -> regex on drugname/prod_ai (upper case); ATC N05A antipsychotics excl. lithium; antiemetic-only agents excluded
 'xanomeline-trospium': r'XANOMELINE|COBENFY|KARXT', 'lumateperone': r'LUMATEPERONE|CAPLYTA', 'brexpiprazole': r'BREXPIPRAZOLE|REXULTI',
 'cariprazine': r'CARIPRAZINE|VRAYLAR', 'aripiprazole': r'ARIPIPRAZOLE|ABILIFY|ARISTADA', 'olanzapine': r'OLANZAPINE|ZYPREXA|LYBALVI',
 'quetiapine': r'QUETIAPINE|SEROQUEL', 'risperidone': r'RISPERIDONE|RISPERDAL|PERSERIS|UZEDY|RYKINDO', 'paliperidone': r'PALIPERIDONE|INVEGA',
 'clozapine': r'CLOZAPINE|CLOZARIL|VERSACLOZ', 'ziprasidone': r'ZIPRASIDONE|GEODON', 'lurasidone': r'LURASIDONE|LATUDA',
 'asenapine': r'ASENAPINE|SAPHRIS|SECUADO', 'iloperidone': r'ILOPERIDONE|FANAPT', 'haloperidol': r'HALOPERIDOL|HALDOL',
 'chlorpromazine': r'CHLORPROMAZINE', 'fluphenazine': r'FLUPHENAZINE', 'perphenazine': r'PERPHENAZINE', 'thioridazine': r'THIORIDAZINE',
 'trifluoperazine': r'TRIFLUOPERAZINE', 'loxapine': r'LOXAPINE|ADASUVE', 'thiothixene': r'THIOTHIXENE|TIOTIXENE', 'molindone': r'MOLINDONE',
 'pimozide': r'PIMOZIDE', 'pimavanserin': r'PIMAVANSERIN|NUPLAZID', 'amisulpride': r'AMISULPRIDE', 'sulpiride': r'(?<!AMI)SULPIRIDE',
 'zuclopenthixol': r'ZUCLOPENTHIXOL', 'flupentixol': r'FLUPENTIXOL|FLUPENTHIXOL', 'levomepromazine': r'LEVOMEPROMAZINE|METHOTRIMEPRAZINE',
 'sertindole': r'SERTINDOLE', 'blonanserin': r'BLONANSERIN', 'perospirone': r'PEROSPIRONE', 'zotepine': r'ZOTEPINE', 'tiapride': r'TIAPRIDE',
}
def read(pat, cols):
    f = glob.glob(os.path.join(qdir, pat))[0]
    return pd.read_csv(f, sep='$', dtype=str, usecols=cols, encoding='latin-1', quoting=3, on_bad_lines='warn', keep_default_na=False)
demo = read('DEMO*.txt', ['primaryid','caseid','caseversion','fda_dt','occp_cod','reporter_country','sex','age','age_cod'])
drug = read('DRUG*.txt', ['primaryid','caseid','drug_seq','role_cod','drugname','prod_ai'])
txt = (drug.drugname + ' ' + drug.prod_ai).str.upper()
drug['ingredient'] = ''
for ing, pat in AP.items():
    m = txt.str.contains(pat, regex=True) & (drug.ingredient == '')
    drug.loc[m, 'ingredient'] = ing
drug = drug[drug.ingredient != '']
reac = read('REAC*.txt', ['primaryid','pt'])
reac = reac[reac.primaryid.isin(set(drug.primaryid))]
dele = []
for f in glob.glob(os.path.join(qdir, '*DELETE*')) + glob.glob(os.path.join(qdir, '*eleted*')):
    dele += [l.strip() for l in open(f, encoding='latin-1') if l.strip().isdigit()]
demo.assign(quarter=q).to_csv(f'{out}/{q}_demo.csv', index=False); drug.assign(quarter=q).to_csv(f'{out}/{q}_drug_ap.csv', index=False)
reac.to_csv(f'{out}/{q}_reac_ap.csv', index=False); pd.Series(sorted(set(dele)), name='caseid').to_csv(f'{out}/{q}_deleted.csv', index=False)
print(q, 'demo', len(demo), 'ap drug rows', len(drug), 'cobenfy rows', (drug.ingredient=='xanomeline-trospium').sum(), 'reac', len(reac), 'deleted', len(set(dele)))
