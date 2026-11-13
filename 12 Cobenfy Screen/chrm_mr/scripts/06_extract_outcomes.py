# Extract outcome GWAS summary statistics for each target-gene region (gene +/- 1 Mb, GRCh38) by remote tabix queries.
# FinnGen R12 (+UKBB meta) is GRCh38; Pan-UKB is GRCh37 -> region lifted to GRCh37, variants lifted back to GRCh38.
import sys, os, subprocess, io, pandas as pd, numpy as np
from concurrent.futures import ThreadPoolExecutor
from pyliftover import LiftOver
P = sys.argv[1]; C = f"{P}/data/clean"; R = f"{P}/data/raw"; OUT = f"{R}/outcomes"; os.makedirs(OUT, exist_ok=True)
os.environ["CURL_CA_BUNDLE"] = "/root/.ccr/ca-bundle.crt"; TABIX = "/opt/renv/bin/tabix"
lo38to37 = LiftOver(f"{R}/ld/grch38_to_grch37.over.chain.gz"); lo37to38 = LiftOver(f"{R}/ld/grch37_to_grch38.over.chain.gz")
genes = pd.read_csv(f"{C}/genes.tsv", sep="\t")
oc = pd.read_csv(f"{C}/outcomes.tsv", sep="\t", dtype=str).fillna("")
fgm = pd.read_csv(f"{R}/fg_manifest.tsv", sep="\t", dtype=str)
umap = pd.read_csv(f"{R}/ukbb_map.tsv", sep="\t", dtype=str)
pm = pd.read_csv(f"{R}/panukb_manifest.tsv", sep="\t", dtype=str, low_memory=False)
FGB = "https://storage.googleapis.com/finngen-public-data-r12"
PUB = "https://pan-ukb-us-east-1.s3.amazonaws.com"
meta = []
def info(o):
    if o.source == "FG_UKBB_META":
        r = umap[umap.fg_phenotype == o.code].iloc[0]
        nca = float(r.fg_n_cases) + float(r.ukbb_n_cases); nco = float(r.fg_n_controls) + float(r.ukbb_n_controls)
        return dict(url=f"{FGB}/meta_analysis/ukbb/summary_stats/finngen_R12_{o.code}_meta_out.tsv.gz", idx=None, build=38, ncase=nca, nctrl=nco)
    if o.source == "FG":
        r = fgm[fgm.phenocode == o.code].iloc[0]
        return dict(url=r.path_https, idx=None, build=38, ncase=float(r.num_cases), nctrl=float(r.num_controls))
    s = pm[(pm.phenocode == o.code) & (pm.pheno_sex == "both_sexes")]
    if o.coding:
        s = s[(s.coding == o.coding) | (s.modifier == o.coding)]
    else:
        s = s[s.modifier.isna() & s.coding.isna()]
    assert len(s) == 1, (o.outcome_id, len(s))
    r = s.iloc[0]
    u = r.aws_path.replace("s3://pan-ukb-us-east-1", PUB); ix = r.aws_path_tabix.replace("s3://pan-ukb-us-east-1", PUB)
    nca = float(r.n_cases_EUR); nco = float(r.n_controls_EUR) if isinstance(r.n_controls_EUR, str) and r.n_controls_EUR not in ("", "nan") else np.nan
    return dict(url=u, idx=ix, build=37, ncase=nca, nctrl=nco)
def header(i):
    u = i["url"] if not i["idx"] else f"{i['url']}##idx##{i['idx']}"
    import urllib.request, zlib
    raw = subprocess.run(["curl", "-s", "-r", "0-65535", i["url"]], capture_output=True).stdout
    d = zlib.decompressobj(31); txt = d.decompress(raw)
    return txt.split(b"\n")[0].decode().lstrip("#").split("\t")
IDX = f"{OUT}/idx"; os.makedirs(IDX, exist_ok=True)
def local_index(i, oid):
    # download the tabix index once per outcome (avoids htslib index-cache races between parallel jobs)
    src = i["idx"] if i["idx"] else i["url"] + ".tbi"
    dst = f"{IDX}/{oid}.tbi"
    if not os.path.exists(dst):
        subprocess.run(["curl", "-sS", "--retry", "5", "-o", dst, src], check=True)
    return dst
def fetch(o, i, g):
    c = g.chr.replace("chr", ""); a = int(g.start) - 1000000; b = int(g.end) + 1000000
    if i["build"] == 37:
        la = lo38to37.convert_coordinate(g.chr, a); lb = lo38to37.convert_coordinate(g.chr, b)
        a, b = la[0][1] - 50000, lb[0][1] + 50000  # small margin; variants filtered after lift-back
    u = f"{i['url']}##idx##{i['lidx']}"
    for attempt in range(4):
        r = subprocess.run([TABIX, u, f"{c}:{a}-{b}"], capture_output=True, text=True, cwd=IDX)
        if r.returncode == 0 and r.stdout: break
    return r.stdout
rows = []
def work(args):
    o, i, hdr, g = args
    fn = f"{OUT}/{o.outcome_id}__{g.gene}.tsv.gz"
    if os.path.exists(fn): return fn, "cached"
    txt = fetch(o, i, g)
    if not txt: return fn, "EMPTY"
    d = pd.read_csv(io.StringIO(txt), sep="\t", header=None, names=hdr, dtype=str, na_values=["NA", ""])
    if o.source == "FG_UKBB_META":
        af = pd.to_numeric(d.UKBB_af_alt, errors="coerce").fillna(pd.to_numeric(d.FINNGEN_af_alt, errors="coerce"))
        x = pd.DataFrame(dict(chr=d.CHR, pos38=d.POS.astype(int), ref=d.REF, alt=d.ALT, beta=d.all_inv_var_meta_beta, se=d.all_inv_var_meta_sebeta,
                              p=d.all_inv_var_meta_p, af=af, nstudies=d.all_meta_N, het_p=d.all_inv_var_het_p, rsid=d.rsid))
    elif o.source == "FG":
        x = pd.DataFrame(dict(chr=d.chrom, pos38=d.pos.astype(int), ref=d.ref, alt=d.alt, beta=d.beta, se=d.sebeta, p=d.pval, af=d.af_alt, rsid=d.rsids))
    else:
        if "low_confidence_EUR" in d: d = d[d.low_confidence_EUR.astype(str).str.lower() != "true"]
        d = d[d.beta_EUR.notna()]
        p38 = []
        for c_, p_ in zip(d.chr, d.pos.astype(int)):
            l = lo37to38.convert_coordinate(str(c_), p_ - 1)  # chain uses "11" for GRCh37 and "chr11" for GRCh38; pyliftover is 0-based
            p38.append(l[0][1] + 1 if l and l[0][0] == "chr" + str(c_) else -1)
        x = pd.DataFrame(dict(chr=d.chr, pos37=d.pos.astype(int), pos38=p38, ref=d.ref, alt=d.alt, beta=d.beta_EUR, se=d.se_EUR,
                              p=10 ** (-pd.to_numeric(d.neglog10_pval_EUR)), af=d["af_EUR"] if "af_EUR" in d else d["af_controls_EUR"]))
        x = x[x.pos38 > 0]
    x["ncase"] = i["ncase"]; x["nctrl"] = i["nctrl"]
    x.to_csv(fn, sep="\t", index=False, compression="gzip")
    return fn, len(x)
jobs = []
for _, o in oc.iterrows():
    i = info(o); hdr = header(i); i["lidx"] = local_index(i, o.outcome_id)
    meta.append(dict(outcome_id=o.outcome_id, url=i["url"], build=i["build"], ncase=i["ncase"], nctrl=i["nctrl"]))
    for _, g in genes.iterrows(): jobs.append((o, i, hdr, g))
pd.DataFrame(meta).to_csv(f"{C}/outcomes_files.tsv", sep="\t", index=False)
with ThreadPoolExecutor(8) as ex:
    for fn, n in ex.map(work, jobs): print(os.path.basename(fn), n, flush=True)
