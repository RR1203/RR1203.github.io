# Extract GTEx v8 eQTL (EUR and all-ancestry) rows for target genes
import gzip, glob, os, sys, csv
P = sys.argv[1]
raw = f"{P}/data/raw/gtex"
genes = {}
for f in glob.glob(f"{raw}/v8_all/*/Brain_Cortex.v8.egenes.txt.gz"):
    with gzip.open(f, 'rt') as fh:
        r = csv.DictReader(fh, delimiter='\t')
        for row in r:
            if row['gene_name'] in ('CHRM1','CHRM2','CHRM3','CHRM4','CHRM5','DRD2','HMGCR'):
                genes[row['gene_id']] = row
with open(f"{P}/data/clean/genes.tsv",'w') as o:
    o.write("gene\tgene_id\tchr\tstart\tend\tstrand\n")
    for gid,r in genes.items():
        o.write(f"{r['gene_name']}\t{gid}\t{r['gene_chr']}\t{r['gene_start']}\t{r['gene_end']}\t{r['strand']}\n")
ids = set(genes)
name = {k:v['gene_name'] for k,v in genes.items()}
out = open(f"{P}/data/clean/gtex_v8_target_signif_pairs.tsv",'w')
out.write("gene\tgene_id\ttissue\tancestry\tvariant_id\ttss_distance\tmaf\tma_count\tpval_nominal\tslope\tslope_se\tpval_nominal_threshold\tpval_beta\n")
eg = open(f"{P}/data/clean/gtex_v8_target_egenes.tsv",'w')
eg.write("gene\tgene_id\ttissue\tancestry\tnum_var\tpval_beta\tqval\ttop_variant\ttop_pval\n")
for anc, pat_s, pat_e in [("EUR", f"{raw}/eqtls/*.v8.EUR.signif_pairs.txt.gz", f"{raw}/eqtls/*.v8.EUR.egenes.txt.gz"),
                          ("ALL", f"{raw}/v8_all/*/*.v8.signif_variant_gene_pairs.txt.gz", f"{raw}/v8_all/*/*.v8.egenes.txt.gz")]:
    for f in sorted(glob.glob(pat_s)):
        t = os.path.basename(f).split('.v8')[0]
        with gzip.open(f,'rt') as fh:
            h = fh.readline().rstrip('\n').split('\t'); ix = {c:i for i,c in enumerate(h)}
            gcol = 'phenotype_id' if 'phenotype_id' in ix else 'gene_id'
            for line in fh:
                x = line.rstrip('\n').split('\t')
                if x[ix[gcol]] in ids:
                    g = x[ix[gcol]]
                    out.write("\t".join([name[g], g, t, anc, x[ix['variant_id']], x[ix['tss_distance']], x[ix['maf']], x[ix['ma_count']], x[ix['pval_nominal']], x[ix['slope']], x[ix['slope_se']], x[ix['pval_nominal_threshold']], x[ix['pval_beta']]])+"\n")
    for f in sorted(glob.glob(pat_e)):
        t = os.path.basename(f).split('.v8')[0]
        with gzip.open(f,'rt') as fh:
            r = csv.DictReader(fh, delimiter='\t')
            for row in r:
                g = row.get('phenotype_id', row.get('gene_id'))
                if g in ids:
                    eg.write("\t".join([name[g], g, t, anc, row['num_var'], row['pval_beta'], row['qval'], row['variant_id'], row['pval_nominal']])+"\n")
out.close(); eg.close()
