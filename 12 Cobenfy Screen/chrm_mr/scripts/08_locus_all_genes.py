# Specificity check input: GTEx v10 significant pairs for ALL genes with cis variants in the CHRM4 window (CHRM4 +/- 500 kb),
# in the tissues used for CHRM4 instruments (skin sun-exposed, whole blood) plus all brain tissues.
import sys, glob, os, pandas as pd
P = sys.argv[1]; raw = f"{P}/data/raw/gtex"; C = f"{P}/data/clean"
g = pd.read_csv(f"{C}/genes.tsv", sep="\t").set_index("gene").loc["CHRM4"]
lo, hi = g.start - 500000, g.end + 500000
names = {}
for f in glob.glob(f"{raw}/v10/*/*.eGenes.txt.gz"):
    d = pd.read_csv(f, sep="\t", usecols=["gene_id", "gene_name"]); names.update(dict(zip(d.gene_id, d.gene_name)))
out = []
for f in sorted(glob.glob(f"{raw}/v10/*/*.signif_pairs.parquet")):
    t = os.path.basename(f).split(".v10")[0]
    if not (t in ("Skin_Sun_Exposed_Lower_leg", "Whole_Blood") or t.startswith("Brain_")): continue
    d = pd.read_parquet(f, columns=["gene_id", "variant_id", "af", "ma_count", "pval_nominal", "slope", "slope_se"])
    d = d[d.variant_id.str.startswith("chr11_")]
    pos = d.variant_id.str.split("_").str[1].astype(int)
    d = d[(pos >= lo) & (pos <= hi)].copy(); d["tissue"] = t
    out.append(d)
o = pd.concat(out); o["gene_name"] = o.gene_id.map(names)
ns = pd.read_csv(f"{C}/gtex_sample_sizes.tsv", sep="\t"); ns = ns[ns.release == "v10"].set_index("tissue").n_samples
o["n_samples"] = o.tissue.map(ns)
o.to_csv(f"{C}/chrm4_locus_v10_all_genes.tsv", sep="\t", index=False)
print(o.groupby(["tissue"]).gene_name.nunique())
print(o[o.tissue == "Skin_Sun_Exposed_Lower_leg"].groupby("gene_name").pval_nominal.min().sort_values().head(25))
