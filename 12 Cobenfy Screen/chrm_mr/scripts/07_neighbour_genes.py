# For every MR instrument variant, list all genes (any GTEx v8/v10 tissue) for which it is a significant cis-eQTL
import sys, glob, os, gzip, pandas as pd
P = sys.argv[1]; C = f"{P}/data/clean"; raw = f"{P}/data/raw/gtex"
ins = pd.read_csv(f"{C}/instruments_mr.tsv", sep="\t")
vs = set(ins.variant_id)
names = {}
for f in glob.glob(f"{raw}/v8_all/*/*.egenes.txt.gz") + glob.glob(f"{raw}/v10/*/*.eGenes.txt.gz"):
    d = pd.read_csv(f, sep="\t", usecols=["gene_id", "gene_name"]); names.update({k.split(".")[0]: v for k, v in zip(d.gene_id, d.gene_name)})
hits = []
for rel, pat in [("v8_EUR", f"{raw}/eqtls/*.signif_pairs.txt.gz"), ("v8_ALL", f"{raw}/v8_all/*/*.signif_variant_gene_pairs.txt.gz")]:
    for f in sorted(glob.glob(pat)):
        t = os.path.basename(f).split(".v8")[0]
        with gzip.open(f, "rt") as fh:
            h = fh.readline().rstrip("\n").split("\t"); ix = {c: i for i, c in enumerate(h)}
            gc = "phenotype_id" if "phenotype_id" in ix else "gene_id"
            for line in fh:
                x = line.split("\t")
                if x[ix["variant_id"]] in vs:
                    hits.append((rel, t, x[ix["variant_id"]], x[ix[gc]], float(x[ix["pval_nominal"]]), float(x[ix["slope"]])))
for f in sorted(glob.glob(f"{raw}/v10/*/*.signif_pairs.parquet")):
    t = os.path.basename(f).split(".v10")[0]
    d = pd.read_parquet(f, columns=["gene_id", "variant_id", "pval_nominal", "slope"])
    d = d[d.variant_id.isin(vs)]
    hits += [("v10", t, v, g, p, s) for g, v, p, s in zip(d.gene_id, d.variant_id, d.pval_nominal, d.slope)]
h = pd.DataFrame(hits, columns=["release", "tissue", "variant_id", "gene_id", "pval", "slope"])
h["gene_name"] = h.gene_id.str.split(".").str[0].map(names)
h.to_csv(f"{C}/instrument_all_eqtl_genes.tsv", sep="\t", index=False)
summ = []
for (eid, v), d in ins.groupby(["exposure_id", "variant_id"]):
    g = eid.split("|")[0]
    o = h[(h.variant_id == v) & (h.gene_name != g)]
    best = o.sort_values("pval").drop_duplicates("gene_name")
    summ.append(dict(exposure_id=eid, variant_id=v, n_other_genes=best.gene_name.nunique(),
                     other_genes="; ".join(f"{r.gene_name}({r.tissue},{r.release},p={r.pval:.1e},b={r.slope:+.2f})" for r in best.head(12).itertuples())))
pd.DataFrame(summ).to_csv(f"{C}/instrument_neighbour_genes.tsv", sep="\t", index=False)
print(pd.DataFrame(summ).to_string())
