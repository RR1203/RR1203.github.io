# Write feasibility.md from data/clean tables (all numbers come from the data files)
import sys, pandas as pd, numpy as np
P = sys.argv[1]; C = f"{P}/data/clean"
f = pd.read_csv(f"{C}/feasibility_all_tissues.tsv", sep="\t")
q = pd.read_csv(f"{C}/qtl_target_all.tsv", sep="\t")
ex = pd.read_csv(f"{C}/exposures.tsv", sep="\t")
nb = pd.read_csv(f"{C}/instrument_neighbour_genes.tsv", sep="\t")
def fmt(x, d=1):
    return "–" if pd.isna(x) else (f"{x:.{d}f}")
def tab(d):
    rows = ["| Gene | GTEx release | Tissue | Class | QTL | N | Variants p<5e-6 (cis ±500 kb) | In 1000G EUR | Pass allele QC | Lead minor-allele copies | Lead p | After clumping (r²<0.1) | F (min) | F (mean) |",
            "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in d.itertuples():
        rows.append(f"| {r.gene} | {r.release} | {r.tissue} | {r.tclass} | {r.qtl_type} | {int(r.n_samples) if not pd.isna(r.n_samples) else '–'} | {r.n_p5e6} | {r.n_p5e6_in_1000G} | {r.n_p5e6_qc} | {int(r.top_ma_count)} | {r.top_p:.1e} | {r.n_clumped} | {fmt(r.F_min)} | {fmt(r.F_mean)} |")
    return "\n".join(rows)
# any-signal summary: number of tissues with any significant pair (any p) per gene x class
anyp = q[q.cis500].groupby(["gene", "tclass"]).agg(n_tissue_release=("tissue", lambda s: s.nunique()), min_p=("pval_nominal", "min")).reset_index()
L = []
L.append("# Step 0 – Feasibility of cis-instruments for CHRM1 and CHRM4 (and contrast genes)\n")
L.append("All numbers below were computed from the downloaded GTEx files (scripts 01–05). Sources that could not be reached are listed at the end.\n")
L.append("**Rules.**\n- Selection: p < 5×10⁻⁶ within the gene ± 500 kb (GRCh38).\n- Allele QC: MAF ≥ 1% and ≥ 10 minor-allele copies in the QTL sample, plus presence in 1000G phase 3 EUR with MAF ≥ 1%.\n- Clumping: r² < 0.1 in 1000G EUR (n = 503), 1 Mb window.\n- F = (β/SE)² per variant.\n")
v = f[f.gene.isin(["CHRM1", "CHRM4"])]
ok = v[(v.tclass.isin(["brain", "blood"])) & (v.n_clumped > 0) & (v.F_min > 10)]
L.append("## Verdict\n")
L.append(f"- **CHRM1: no usable instrument in any brain or blood source.** The only brain hit was the v8 all-ancestry substantia nigra set (lead p = {v[(v.gene=='CHRM1')&(v.tissue=='Brain_Substantia_nigra')].top_p.min():.1e}). It is carried by {int(v[(v.gene=='CHRM1')&(v.tissue=='Brain_Substantia_nigra')].top_ma_count.min())} minor-allele copies and is absent from 1000G EUR. It is not significant in GTEx v10. No sQTL or pQTL source was available.")
c4b = v[(v.gene=='CHRM4')&(v.tissue.str.contains('cingulate'))].iloc[0]
c4w = v[(v.gene=='CHRM4')&(v.tissue=='Whole_Blood')&(v.release=='v10')].iloc[0]
L.append(f"- **CHRM4 brain: no usable instrument.** The single v8 EUR anterior-cingulate hit (p = {c4b.top_p:.1e}, F = {c4b.top_F:.1f}) rests on {int(c4b.top_ma_count)} minor-allele copy. It is not significant in v10, which has more samples in the same tissue.")
L.append(f"- **CHRM4 blood: one usable instrument.** GTEx v10 whole blood (N = {int(c4w.n_samples)}): {c4w.n_p5e6} variants at p < 5×10⁻⁶ → {c4w.n_clumped} after clumping, F = {c4w.F_min:.1f}, variance explained R² = {c4w.R2_sum:.3f}.")
L.append(f"- Brain/blood CHRM1/CHRM4 sources passing the stop rule (F > 10): **{len(ok)}**. The analysis therefore continued, for CHRM4 only, using a blood instrument and, as a secondary tissue-consistency source, skin eQTLs.")
L.append("- **Weakness, stated plainly.** The usable CHRM4 instrument is a single variant from an 800-sample blood eQTL map, for a receptor whose physiological site of action is the brain (striatum). Blood CHRM4 expression is low. The variant is also a stronger eQTL for neighbouring genes (table below). This is a weak and indirect proxy for M4 stimulation.")
L.append("- **Direction assumption.** Higher receptor expression is taken as agonist-like (more receptor signalling). This is an approximation. An agonist acts acutely and on existing receptor protein, while lifelong higher expression may cause compensation (desensitisation). Expression in blood or skin need not track brain receptor density, and mRNA need not track protein.\n")
L.append("## Target genes (CHRM1, CHRM4): every gene × release × tissue with ≥ 1 variant at p < 5×10⁻⁶\n")
L.append(tab(v.sort_values(["gene", "tclass", "top_p"])))
L.append("\nTissue classes with any GTEx significant pair (any p) for the target genes, within ± 500 kb:\n")
L.append("| Gene | Class | Tissue-release sets with any significant pair | Best p |\n|---|---|---|---|")
for r in anyp[anyp.gene.isin(["CHRM1", "CHRM4"])].itertuples():
    L.append(f"| {r.gene} | {r.tclass} | {r.n_tissue_release} | {r.min_p:.1e} |")
L.append("\n## Contrast genes (CHRM2, CHRM3, CHRM5) and positive-control genes (DRD2, HMGCR): brain/blood sets, and the peripheral sets used\n")
cg = f[(~f.gene.isin(["CHRM1", "CHRM4"])) & (f.tclass.isin(["brain", "blood"]) | f.tissue.isin(ex.tissue))]
L.append(tab(cg.sort_values(["gene", "tclass", "top_p"])))
L.append("\nThe full table across all 49 GTEx tissues (169 gene × release × tissue × QTL-type sets) is in `data/clean/feasibility_all_tissues.tsv`.\n")
L.append("## Exposures carried into MR (pre-specified choice rule, see decisions_log.md #13)\n")
L.append("| Exposure | Role | Class | N | Variants | F (min) | F (mean) |\n|---|---|---|---|---|---|---|")
for r in ex.itertuples():
    L.append(f"| {r.exposure_id} | {r.role} | {r.tclass} | {int(r.n_samples)} | {r.n_clumped} | {r.F_min:.1f} | {r.F_mean:.1f} |")
L.append("\n## Other genes regulated by each instrument (any GTEx v8/v10 tissue; first 12 by p shown)\n")
L.append("| Exposure | Variant | No. other genes | Other genes (tissue, release, p, β) |\n|---|---|---|---|")
for r in nb.itertuples():
    L.append(f"| {r.exposure_id} | {r.variant_id} | {r.n_other_genes} | {r.other_genes if isinstance(r.other_genes, str) else ''} |")
L.append("\n## Sources not checked (unreachable from this environment)\n")
L.append("- MetaBrain, PsychENCODE (brain eQTL); eQTLGen (blood eQTL); UKB-PPP, deCODE, Fenland (pQTL); eQTL Catalogue.\n- Whether CHRM1/CHRM4 are measured on those protein panels, and whether they carry stronger instruments, **is unknown**. A larger brain or blood eQTL resource could change this verdict.")
open(f"{P}/feasibility.md", "w").write("\n".join(L) + "\n")
print("ok")
