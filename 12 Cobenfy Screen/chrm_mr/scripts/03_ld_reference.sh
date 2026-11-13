#!/bin/bash
# Regional 1000 Genomes phase 3 EUR (n=503) reference, GRCh38 positions (1000G "GRCh38_positions" release), target gene +/- 1 Mb
set -e
P="$1"; export CURL_CA_BUNDLE=/root/.ccr/ca-bundle.crt; B=/opt/renv/bin
S=https://1000genomes.s3.amazonaws.com/release/20130502/supporting/GRCh38_positions
cd "$P/data/raw/ld"
tail -n +2 "$P/data/clean/genes.tsv" | while IFS=$'\t' read g gid chr st en strand; do
  a=$((st-1000000)); b=$((en+1000000)); c=${chr#chr}
  $B/bcftools view -r ${c}:${a}-${b} -S eur_samples_p3.txt -m2 -M2 \
     "$S/ALL.${chr}.phase3_shapeit2_mvncall_integrated_v3plus_nounphased.rsID.genotypes.GRCh38_dbSNP_no_SVs.vcf.gz" -Ou | \
  $B/bcftools view -q 0.005:minor -Ou | \
  $B/bcftools annotate --set-id 'chr%CHROM\_%POS\_%REF\_%ALT\_b38' -Oz -o ${g}_eur.vcf.gz
  $B/plink --vcf ${g}_eur.vcf.gz --vcf-half-call missing --double-id --keep-allele-order --make-bed --out ${g}_eur > /dev/null
  echo "$g $(wc -l < ${g}_eur.bim) variants"
done
