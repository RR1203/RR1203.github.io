# Extract GTEx v10 eQTL signif pairs + SuSiE credible sets, and GTEx v8 sQTL signif pairs, for target genes
import sys, glob, os, gzip, pandas as pd
P = sys.argv[1]; raw = f"{P}/data/raw/gtex"
genes = pd.read_csv(f"{P}/data/clean/genes.tsv", sep="\t")
base = {g.split('.')[0]: n for g, n in zip(genes.gene_id, genes.gene)}
# v10 egenes
eg = []
for f in sorted(glob.glob(f"{raw}/v10/*/*.v10.eGenes.txt.gz")):
    t = os.path.basename(f).split('.v10')[0]
    d = pd.read_csv(f, sep="\t"); d['gid0'] = d.gene_id.str.split('.').str[0]
    d = d[d.gid0.isin(base)]; d.insert(0, 'tissue', t); eg.append(d)
eg = pd.concat(eg); eg['gene'] = eg.gid0.map(base)
eg.to_csv(f"{P}/data/clean/gtex_v10_target_egenes.tsv", sep="\t", index=False)
pr = []
for f in sorted(glob.glob(f"{raw}/v10/*/*.v10.eQTLs.signif_pairs.parquet")):
    t = os.path.basename(f).split('.v10')[0]
    d = pd.read_parquet(f); d['gid0'] = d.gene_id.str.split('.').str[0]
    d = d[d.gid0.isin(base)].copy(); d.insert(0, 'tissue', t); pr.append(d)
pr = pd.concat(pr); pr['gene'] = pr.gid0.map(base)
pr.to_csv(f"{P}/data/clean/gtex_v10_target_signif_pairs.tsv", sep="\t", index=False)
su = []
for f in sorted(glob.glob(f"{raw}/v10susie/*.v10.eQTLs.SuSiE_summary.parquet")):
    t = os.path.basename(f).split('.v10')[0]
    d = pd.read_parquet(f); d['gid0'] = d.phenotype_id.str.split('.').str[0]
    d = d[d.gid0.isin(base)].copy(); d.insert(0, 'tissue', t); su.append(d)
su = pd.concat(su); su['gene'] = su.gid0.map(base)
su.to_csv(f"{P}/data/clean/gtex_v10_target_susie.tsv", sep="\t", index=False)
sq = []
for f in sorted(glob.glob(f"{raw}/v8_sqtl/*/*.v8.sqtl_signifpairs.txt.gz")):
    t = os.path.basename(f).split('.v8')[0]
    d = pd.read_csv(f, sep="\t"); d['gid0'] = d.phenotype_id.str.split(':').str[-1].str.split('.').str[0]
    d = d[d.gid0.isin(base)].copy(); d.insert(0, 'tissue', t); sq.append(d)
sq = pd.concat(sq); sq['gene'] = sq.gid0.map(base)
sq.to_csv(f"{P}/data/clean/gtex_v8_target_sqtl_signif_pairs.tsv", sep="\t", index=False)
print(len(eg), len(pr), len(su), len(sq))
