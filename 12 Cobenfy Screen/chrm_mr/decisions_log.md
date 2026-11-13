# Decisions log

Run date: 2026-11-13. Unattended run. Each entry: decision, then reason.

## Data access (what could and could not be reached)

1. **Network policy blocked most planned sources.** Blocked (proxy refused connection): OpenGWAS API (api.opengwas.io, gwas.mrcieu.ac.uk), PGC (pgc.unc.edu, figshare), GWAS Catalog FTP (ftp.ebi.ac.uk), eQTL Catalogue API, eQTLGen (molgeniscloud), MetaBrain (metabrain.nl), PsychENCODE, UKB-PPP (Synapse), deCODE, Fenland/omicscience, GTEx portal API, CRAN/Bioconductor, Ensembl REST, LDlink, UCSC. `OPENGWAS_JWT` was not set either.
   Reachable: Google Cloud Storage and AWS S3 public buckets, GitHub, conda, PyPI, NCBI E-utilities, Europe PMC, ClinicalTrials.gov.
   Decision: do not stall the overnight run on an approval prompt. Use what is reachable and log what is missing.
2. **Exposure (QTL) sources used:** GTEx v8 (EUR-only and all-ancestry analyses), GTEx v10 (all ancestry, larger N), GTEx v8 sQTL, GTEx v10 SuSiE credible sets (GCS bucket `adult-gtex`).
   **Not used (unreachable):** MetaBrain, PsychENCODE, eQTLGen, UKB-PPP, deCODE and Fenland pQTLs. Whether these hold CHRM1/CHRM4 instruments could not be checked.
3. **Blood eQTL:** eQTLGen was unreachable, so GTEx whole blood (v8 EUR n = 558; v10 n = 800) stands in. It is far smaller than eQTLGen.
4. **Outcome sources used:**
   - FinnGen R12 + UKBB inverse-variance meta-analysis (EUR; GRCh38) for disease endpoints.
   - FinnGen R12 alone where no meta exists.
   - Pan-UKB EUR (GRCh37, lifted to GRCh38) for continuous traits and a few binary traits.
   - PGC files were unreachable. FinnGen/UKBB psychiatric endpoints have far fewer cases than PGC (for example schizophrenia: 7,859 cases).
5. **Outcomes not available:** Lewy body dementia (no FinnGen/Pan-UKB endpoint found), the Tourette-specific endpoint (tic disorders `KRA_PSY_TIC_EXMORE` used as proxy), drinks per week (UKB alcohol intake frequency 1558 used; higher code = less frequent), AUDIT score.
   Hyperhidrosis (Pan-UKB phecode 705.8, 733 cases) and lactose intolerance (FinnGen, 1,020 cases) are badly underpowered.
6. **Non-EUR sensitivity analyses** (MVP multi-ancestry meta) were not run. The run had no candidate at a target gene whose evidence could be firmed up by ancestry, and time went to QC.
7. **LD reference:** the 1000 Genomes high-coverage GRCh38 phased files on S3 are 0-byte placeholders. Used 1000 Genomes phase 3 EUR (n = 503) at GRCh38 positions instead (`release/20130502/supporting/GRCh38_positions`).
8. **Liftover:** Hail public chain files (GRCh37 side named "11", GRCh38 side named "chr11"); pyliftover (0-based).
   A first run produced empty Pan-UKB extracts because of this naming. It was fixed and re-extracted.
9. **Tabix index race:** parallel remote tabix calls shared a cached index file, giving silent empty or partial reads. Fixed by downloading each index once to a local file. All outcome extracts were then deleted and re-extracted.

## Instrument selection

10. **Cis window:** gene body ± 500 kb (GRCh38). **Threshold:** p < 5×10⁻⁶ in GTEx significant pairs. **Clumping:** r² < 0.1, 1 Mb window, 1000G EUR, plink 1.9.
11. **Full GTEx all-pairs statistics are not public** (requester-pays bucket). Instruments come from the significant-pairs files. These contain every variant below the gene's permutation threshold, so they include all p < 5×10⁻⁶ variants.
12. **Allele-count QC (added after inspection):** require MAF ≥ 1% in the QTL sample, ≥ 10 minor-allele copies, and presence in 1000G EUR with MAF ≥ 1%.
    Reason: the only CHRM4 brain "eQTL" (v8 EUR anterior cingulate, p = 8×10⁻⁸) rests on one allele copy (ma_count = 1). The only CHRM1 brain signal (v8 all-ancestry substantia nigra) rests on 4 copies of a haplotype absent from EUR. Neither replicates in GTEx v10, which has more samples in the same tissues. These are artefacts, not instruments.
13. **Exposure choice rule (pre-specified before outcome data were analysed):** for each gene × tissue class (brain, blood) × release family (v8, v10), keep the QC-passing tissue with the strongest lead eQTL.
    - v8: the EUR-only analysis is preferred; all-ancestry is used only if EUR has no QC-passing set.
    - Peripheral tissues are used only for CHRM3 (mechanism control), CHRM4 (tissue-consistency check), and DRD2/HMGCR (positive controls).
14. **sQTLs** are reported in feasibility but not used for MR. No CHRM1/CHRM4 sQTL exists in any brain or blood tissue, and the direction of intron usage relative to receptor amount is not interpretable.
15. **F-statistic** = (β/SE)² per variant. R² = F/(F + N − 2). N per tissue was counted from the GTEx covariate files.

## MR

16. Effects are expressed per 1 SD higher (inverse-normal-transformed) expression of the GTEx ALT allele.
17. Outcome alleles were aligned by GRCh38 position + REF/ALT (allowing a swap). Both datasets use forward-strand reference alleles, so palindromic SNPs were kept. Rows whose 1000G EUR vs outcome allele frequency differed by > 0.2 were dropped.
18. One variant: Wald ratio (first-order SE). Two or more: generalised fixed-effect IVW with the signed 1000G EUR LD matrix (MendelianRandomization::mr_ivw with `correlation`), plus standard IVW.
    MR-Egger and weighted median were used only when there were ≥ 3 variants. Leave-one-out was used when there were ≥ 2.
19. **Steiger:** TwoSampleMR::mr_steiger. Outcome r for binary traits comes from `get_r_from_lor` with sample prevalence.
20. **FDR:** Benjamini–Hochberg across all gene × source × outcome tests in one family (490 tests), including control genes and control outcomes.

## Colocalisation

21. coloc.abf with default priors (p1 = p2 = 10⁻⁴, p12 = 10⁻⁵), window gene ± 500 kb. Variant universe: outcome variants present in 1000G EUR with MAF ≥ 1%.
22. **Missing eQTL statistics:** variants absent from GTEx significant pairs get eQTL β = 0, with SE from 1/√(2N·MAF·(1−MAF)).
    This makes PP.H4 conservative when the outcome's causal variant has a sub-threshold eQTL. Sensitivity: coloc restricted to significant-pair variants only (`PP.H4_signif_only`).
23. **SuSiE-coloc:** full eQTL statistics are unavailable, so SuSiE was run on the outcome side only (susie_rss, 1000G EUR LD, L = 5), in regions with outcome p < 10⁻⁶. Its credible-set log Bayes factors were compared with the single-signal eQTL log Bayes factors using coloc.bf_bf.
    LD comes from 503 Europeans while the outcome is FinnGen/UKB, so mismatch is possible.
24. **Candidate rule** (as specified): q < 0.05 AND PP.H4 > 0.8 AND direction consistent across sensitivity methods (IVW/Egger/WM/leave-one-out where applicable) AND across tissues/releases of the same gene.

## Checks added beyond the brief

25. **Neighbouring-gene pleiotropy:** for each instrument, every gene for which it is a significant eQTL in any GTEx v8/v10 tissue (`data/clean/instrument_neighbour_genes.tsv`).
26. **GWAS-based HMGCR sanity check:** LDL-associated variants within ± 100 kb of HMGCR (Pan-UKB, p < 5×10⁻⁸, clumped) → coronary heart disease. This checks the harmonisation and estimation code independently of eQTL tissue relevance.
27. **Bug caught during QC:** allele alignment de-duplicated by variant only. Exposures sharing a variant (CHRM4 v8/v10 skin, DRD2 v8 nerve/cerebellum, CHRM3 v8/v10 thyroid) were silently dropped or partly dropped. Fixed (de-duplicate by exposure + variant) and the whole analysis re-run.
28. **Gene coordinates and IDs** were taken from the GTEx v8 annotation (no hard-coded IDs).
