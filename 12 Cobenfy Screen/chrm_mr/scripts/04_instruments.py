# Step 0: instrument selection (p<5e-6, cis +/-500 kb of gene), LD clumping (r2<0.1, 1000G EUR), F-statistics
import sys, os, subprocess, pandas as pd, numpy as np
P = sys.argv[1]; C = f"{P}/data/clean"; LD = f"{P}/data/raw/ld"; PL = "/opt/renv/bin/plink"
genes = pd.read_csv(f"{C}/genes.tsv", sep="\t").set_index("gene")
ns = pd.read_csv(f"{C}/gtex_sample_sizes.tsv", sep="\t")
v8 = pd.read_csv(f"{C}/gtex_v8_target_signif_pairs.tsv", sep="\t")
v8["release"] = np.where(v8.ancestry == "EUR", "v8_EUR", "v8_ALL")
v10 = pd.read_csv(f"{C}/gtex_v10_target_signif_pairs.tsv", sep="\t"); v10["release"] = "v10"
sq = pd.read_csv(f"{C}/gtex_v8_target_sqtl_signif_pairs.tsv", sep="\t"); sq["release"] = "v8_ALL_sQTL"
v10["maf"] = np.minimum(v10.af, 1 - v10.af)
cols = ["gene", "release", "tissue", "variant_id", "pval_nominal", "slope", "slope_se", "maf", "ma_count"]
sq["intron"] = sq.phenotype_id
qtl = pd.concat([v8[cols], v10[cols], sq[cols + ["intron"]]], ignore_index=True)
qtl["chr"] = qtl.variant_id.str.split("_").str[0]
qtl["pos"] = qtl.variant_id.str.split("_").str[1].astype(int)
# cis window: +/-500 kb of gene body
qtl = qtl.merge(genes[["start", "end"]], left_on="gene", right_index=True)
qtl["cis500"] = (qtl.pos >= qtl.start - 500000) & (qtl.pos <= qtl.end + 500000)
qtl["F"] = (qtl.slope / qtl.slope_se) ** 2
def tclass(t):
    if t.startswith("Brain_"): return "brain"
    if t == "Whole_Blood": return "blood"
    return "peripheral"
qtl["tclass"] = qtl.tissue.map(tclass)
qtl["qtl_type"] = np.where(qtl.release.str.contains("sQTL"), "sQTL", "eQTL")
qtl["release_n"] = qtl.release.str.replace("_sQTL", "")
qtl = qtl.merge(ns[["release", "tissue", "n_samples"]].rename(columns={"release": "release_n"}), on=["release_n", "tissue"], how="left")
# 1000G EUR availability (match on chr/pos/alleles, either orientation)
bims = []
for g in genes.index:
    b = pd.read_csv(f"{LD}/{g}_eur.bim", sep="\t", header=None, names=["c", "id", "cm", "pos", "a1", "a2"]); b["gene"] = g; bims.append(b)
bim = pd.concat(bims)
ids = set(bim.id)
def flipid(v):
    c, p, r, a, b = v.split("_"); return f"{c}_{p}_{a}_{r}_{b}"
qtl["ld_id"] = [v if v in ids else (flipid(v) if flipid(v) in ids else None) for v in qtl.variant_id]
# 1000G EUR MAF
frq = []
for g in genes.index:
    subprocess.run([PL, "--bfile", f"{LD}/{g}_eur", "--freq", "--out", f"/tmp/w/frq_{g}"], capture_output=True)
    frq.append(pd.read_csv(f"/tmp/w/frq_{g}.frq", sep=r"\s+")[["SNP", "MAF"]])
frq = pd.concat(frq).drop_duplicates("SNP").rename(columns={"SNP": "ld_id", "MAF": "maf_1000G_EUR"})
qtl = qtl.merge(frq, on="ld_id", how="left")
# QC: minor allele frequency >= 1% and >= 10 minor-allele copies in the eQTL sample, present in 1000G EUR with MAF >= 1%
qtl["qc_pass"] = (qtl.maf >= 0.01) & (qtl.ma_count >= 10) & (qtl.maf_1000G_EUR >= 0.01)
qtl.to_csv(f"{C}/qtl_target_all.tsv", sep="\t", index=False)
sel = qtl[(qtl.pval_nominal < 5e-6) & qtl.cis500].copy()
# For sQTL: keep the strongest intron per gene x tissue
sel = sel.sort_values("pval_nominal")
# clumping per gene x release x tissue x qtl_type (and intron for sQTL)
rows = []
for (g, rel, t, qt), d in sel.groupby(["gene", "release", "tissue", "qtl_type"]):
    if qt == "sQTL":
        best = d.iloc[0].intron; d = d[d.intron == best]
    d = d.drop_duplicates("variant_id")
    inld = d[d.ld_id.notna() & d.qc_pass]
    tag = f"{g}_{rel}_{t}".replace("/", "_")
    rec = dict(gene=g, release=rel, tissue=t, tclass=d.tclass.iloc[0], qtl_type=qt, n_samples=d.n_samples.iloc[0],
               n_p5e6=len(d), n_p5e6_in_1000G=int(d.ld_id.notna().sum()), n_p5e6_qc=len(inld), top_ma_count=d.iloc[0].ma_count, top_variant=d.iloc[0].variant_id, top_p=d.iloc[0].pval_nominal,
               top_F=d.iloc[0].F, intron=d.intron.iloc[0] if qt == "sQTL" else "")
    clumped = []
    if len(inld) == 1:
        clumped = [inld.iloc[0].ld_id]
    elif len(inld) > 1:
        tmp = f"/tmp/w/clump_{tag}"
        inld[["ld_id", "pval_nominal"]].rename(columns={"ld_id": "SNP", "pval_nominal": "P"}).to_csv(tmp + ".txt", sep="\t", index=False)
        subprocess.run([PL, "--bfile", f"{LD}/{g}_eur", "--clump", tmp + ".txt", "--clump-p1", "5e-6", "--clump-p2", "1",
                        "--clump-r2", "0.1", "--clump-kb", "1000", "--out", tmp], capture_output=True)
        cl = pd.read_csv(tmp + ".clumped", sep=r"\s+")
        clumped = list(cl.SNP)
    keep = inld[inld.ld_id.isin(clumped)].copy()
    rec["n_clumped"] = len(keep)
    rec["clumped_variants"] = ";".join(keep.variant_id)
    rec["F_min"] = keep.F.min() if len(keep) else np.nan
    rec["F_mean"] = keep.F.mean() if len(keep) else np.nan
    rec["R2_sum"] = (keep.F / (keep.F + keep.n_samples - 2)).sum() if len(keep) else np.nan
    rows.append(rec)
    keep.assign(exposure_id=f"{g}|{rel}|{t}|{qt}").to_csv(f"{C}/instr_tmp_{tag}_{qt}.tsv", sep="\t", index=False)
feas = pd.DataFrame(rows)
feas.to_csv(f"{C}/feasibility_all_tissues.tsv", sep="\t", index=False)
import glob
ins = pd.concat([pd.read_csv(f, sep="\t") for f in glob.glob(f"{C}/instr_tmp_*.tsv")])
for f in glob.glob(f"{C}/instr_tmp_*.tsv"): os.remove(f)
ins.to_csv(f"{C}/instruments_clumped_all.tsv", sep="\t", index=False)
print(feas[feas.tclass != "peripheral"].sort_values(["gene", "release", "top_p"]).to_string())
print(len(feas), "gene x release x tissue sets with >=1 variant p<5e-6")
