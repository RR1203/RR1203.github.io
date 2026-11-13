# Pre-specified rule: per gene x tissue class x release family, keep the QC-passing tissue with the strongest lead eQTL.
# Release families: GTEx v8 (EUR-only analysis preferred; all-ancestry only if EUR has no QC-passing set) and GTEx v10.
# Classes: brain, blood for all genes; peripheral only for CHRM3 (mechanism control), CHRM4 (tissue consistency),
# DRD2 and HMGCR (method positive controls). sQTLs are reported in feasibility but not used for MR.
import sys, pandas as pd, numpy as np
P = sys.argv[1]; C = f"{P}/data/clean"
f = pd.read_csv(f"{C}/feasibility_all_tissues.tsv", sep="\t")
ins = pd.read_csv(f"{C}/instruments_clumped_all.tsv", sep="\t")
f = f[(f.n_clumped > 0) & (f.qtl_type == "eQTL")].copy()
f["family"] = np.where(f.release.str.startswith("v8"), "v8", "v10")
f = f[(f.tclass != "peripheral") | f.gene.isin(["CHRM3", "CHRM4", "DRD2", "HMGCR"])]
out = []
for (g, cl, fam), d in f.groupby(["gene", "tclass", "family"]):
    if fam == "v8":
        d = d[d.release == "v8_EUR"] if (d.release == "v8_EUR").any() else d
    out.append(d.sort_values("top_p").iloc[0])
ex = pd.DataFrame(out)
ex["exposure_id"] = ex.gene + "|" + ex.release + "|" + ex.tissue + "|eQTL"
ex["role"] = ex.gene.map({"CHRM1": "target", "CHRM4": "target", "CHRM2": "contrast", "CHRM3": "contrast/mechanism control",
                          "CHRM5": "contrast", "DRD2": "positive control", "HMGCR": "positive control"})
ex.to_csv(f"{C}/exposures.tsv", sep="\t", index=False)
ii = ins[ins.exposure_id.isin(ex.exposure_id)]
ii.to_csv(f"{C}/instruments_mr.tsv", sep="\t", index=False)
print(ex[["exposure_id", "tclass", "role", "n_samples", "n_clumped", "F_min", "F_mean", "top_p"]].to_string())
print(len(ii), "instrument rows")
