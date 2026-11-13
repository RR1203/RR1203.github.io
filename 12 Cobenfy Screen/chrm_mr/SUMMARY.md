# SUMMARY: drug-target MR for muscarinic M1/M4 (CHRM1/CHRM4)

Run: 2026-11-13, unattended. All numbers come from files downloaded in this run. They are in `mr_results.csv`, `feasibility.md`, `data/clean/` and the knitted `analysis.html`.

---

## Part 1 – Audit: what was actually run

### Data that could be retrieved
- **GTEx v8** eQTL significant pairs and eGenes, EUR-only and all-ancestry, 49 tissues. Public GCS bucket `adult-gtex`.
- **GTEx v10** eQTL significant pairs (larger N), SuSiE credible sets and covariate files (used to count N per tissue).
- **GTEx v8** sQTL significant pairs.
- **1000 Genomes phase 3 EUR** (n = 503), GRCh38 positions, regional genotypes for gene ± 1 Mb. AWS S3.
- **FinnGen R12 + UKBB meta-analysis** (EUR) for 25 disease outcomes, and **FinnGen R12** alone for 6. Region extracts by remote tabix.
- **Pan-UKB EUR** for 18 outcomes (continuous traits, parental Alzheimer's, hair colour, incontinence, hyperhidrosis), lifted GRCh37 → GRCh38.
- Literature and trials: Europe PMC, PubMed E-utilities, ClinicalTrials.gov API. Raw output: `data/raw/literature/literature_search_2026-11-13.json`.

### Data that could NOT be retrieved
The environment's network policy blocked these hosts (see decisions_log.md #1):
- **Brain eQTL:** MetaBrain, PsychENCODE.
- **Blood eQTL:** eQTLGen.
- **pQTL:** UKB-PPP, deCODE, Fenland. Whether CHRM1/CHRM4 are measured there is unknown.
- **Outcomes:** PGC summary statistics, OpenGWAS (no `OPENGWAS_JWT` either), GWAS Catalog FTP, eQTL Catalogue.
- **Outcomes with no endpoint:** Lewy body dementia, a Tourette-specific endpoint (tic disorders used), drinks per week/AUDIT (alcohol intake frequency used).
- The **MVP multi-ancestry sensitivity** was not run.

### Steps run (scripts in `scripts/`, analysis in `analysis.Rmd`)
1. Extracted QTL rows for CHRM1–5, DRD2 and HMGCR from every GTEx v8/v10 tissue, plus v8 sQTL (scripts 01–02).
2. Built a regional 1000G EUR LD reference (03).
3. Selected instruments (p < 5×10⁻⁶, gene ± 500 kb), applied allele QC (MAF ≥ 1%, ≥ 10 minor-allele copies, present in 1000G EUR) and clumped (r² < 0.1). Computed F (04).
4. Chose exposures with a pre-specified rule (05): 13 exposures.
5. Extracted 49 outcomes × 7 gene regions = 343 region files (06).
6. Listed the other genes each instrument regulates across all GTEx tissues (07).
7. In `analysis.Rmd`:
   - Harmonisation.
   - MR: Wald ratio or LD-aware generalised IVW, plus IVW. MR-Egger and weighted median only for ≥ 3 variants; leave-one-out for ≥ 2.
   - Steiger directionality.
   - coloc.abf, with a significant-pairs-only sensitivity, and outcome-side SuSiE + coloc.bf_bf.
   - Tissue consistency.
   - BH-FDR over all 637 tests.
   - Candidate rule; positive, mechanism, indication and negative controls.
   - Figures.
8. Specificity check (08 plus an Rmd block): colocalisation of the CHRM4-locus outcome signals with every gene's eQTL in the CHRM4 window (71 gene × tissue sets, GTEx v10 skin, blood and 13 brain tissues).
9. Wrote `feasibility.md` from the data (09). Ran the novelty searches.

### Problems found and fixed during the run
- Parallel remote tabix calls shared a cached index file, which can give partial reads. Fixed by using local indexes; all outcomes were re-extracted.
- Liftover chain naming made Pan-UKB extracts empty. Fixed; Pan-UKB outcomes were re-extracted.
- Allele alignment de-duplicated by variant only, which dropped 3 exposures that share variants with another exposure. Fixed; everything was re-run. The final run has 13 exposures × 49 outcomes = 637 tests, all with full instrument coverage.
- The first apparent CHRM4 brain instrument and the only CHRM1 instrument were allele-count artefacts. The QC rule above was added and they were excluded.

### Limitations that matter
- Full GTEx summary statistics are not public. Coloc therefore set eQTL z = 0 for variants outside the GTEx significant pairs; this is conservative for H4. A sensitivity restricted to significant pairs is reported.
- SuSiE was run on the outcome side only.
- LD comes from 503 Europeans while the outcomes are FinnGen/UK Biobank.
- All CHRM4 analyses are single-variant Wald ratios, so pleiotropy-robust methods were impossible.

---

## Part 2 – Paper-ready Methods and Results

### Methods
We used cis-acting expression quantitative trait loci (eQTLs) as proxies for lifelong differences in muscarinic receptor expression. Higher expression was taken as analogous to receptor agonism.

**Instruments.**
- **Sources:** GTEx v8 (European-ancestry and all-ancestry analyses) and GTEx v10, all brain tissues, whole blood and peripheral tissues; GTEx v8 splicing QTLs.
- **Selection:** variants within 500 kb of each gene (GRCh38) with p < 5×10⁻⁶.
- **QC:** minor allele frequency ≥ 1%, ≥ 10 minor-allele copies in the eQTL sample, and presence in the 1000 Genomes phase 3 European panel (n = 503) with MAF ≥ 1%.
- **Clumping:** r² < 0.1.
- **Strength:** F = (β/SE)² per variant.
- **Exposure choice:** for each gene, tissue class (brain, blood) and GTEx release, we pre-specified the tissue with the strongest lead eQTL. Peripheral tissues were used only for CHRM3 (mechanism control), CHRM4 (tissue consistency), DRD2 and HMGCR (method positive controls).

**Outcomes.**
- **Disease endpoints:** European-ancestry summary statistics from the FinnGen R12 + UK Biobank meta-analysis (or FinnGen R12 alone).
- **Continuous traits and some binary traits:** Pan-UK Biobank European-ancestry results (lifted to GRCh38).
- **Total:** 49 outcomes covering psychiatric, substance-use, cognitive, neurological, sleep, metabolic and peripheral-muscarinic safety traits, plus negative and positive controls.

**Estimation.**
- Wald ratios for single variants; LD-corrected generalised inverse-variance weighting for several variants.
- MR-Egger and weighted median for ≥ 3 variants; leave-one-out analysis.
- Steiger directionality tests.
- Bayesian colocalisation (coloc.abf, default priors, gene ± 500 kb). Because only significant GTEx pairs are public, the eQTL effect was set to zero for other variants (conservative). A sensitivity restricted to significant pairs was run. Where the outcome had a regional signal (p < 10⁻⁶), the outcome was fine-mapped with SuSiE and compared with coloc.bf_bf.
- False-discovery rate: Benjamini–Hochberg over all 637 gene × source × outcome tests.
- **Candidate rule:** q < 0.05, PP.H4 > 0.8, and directional consistency across methods and tissues.

**Specificity.** We tested colocalisation of each CHRM4 candidate outcome with the eQTLs of every gene in the CHRM4 cis window, in GTEx v10 skin, whole blood and 13 brain tissues.

### Results
**Feasibility.**
- **CHRM1:** no usable cis-instrument in any brain or blood source. The only brain signal (substantia nigra, all-ancestry GTEx v8, lead p = 4.6×10⁻⁶) was carried by 4 minor-allele copies, was absent from European reference data and did not replicate in GTEx v10.
- **CHRM4 brain:** the only brain signal (anterior cingulate, GTEx v8 European, p = 8.1×10⁻⁸) rested on a single allele copy and did not replicate in GTEx v10.
- **CHRM4 blood:** one usable instrument in GTEx v10 whole blood (N = 800; 11 variants at p < 5×10⁻⁶, 1 after clumping; F = 25.8; R² = 0.031).
- **CHRM4 skin:** a stronger skin eQTL (GTEx v10, N = 751; F = 46.6) was used as a secondary source.
- **sQTLs:** none for CHRM1 or CHRM4 in brain or blood.
- **Pleiotropy:** both CHRM4 instruments were also significant eQTLs for neighbouring genes. The blood variant: 9 other genes, including ATG13 (p = 2.6×10⁻²³) and PACSIN3 (p = 1.1×10⁻¹²). The skin variant: 18 other genes.

**Method controls.**
- **HMGCR → LDL:** reproduced. Higher skeletal-muscle HMGCR expression was associated with higher LDL cholesterol (GTEx v10: β = 0.395 SD per SD, p = 4.0×10⁻¹⁹⁴; PP.H4 = 0.98). It was also associated with lower type 2 diabetes risk (OR 0.854, 95% CI 0.811–0.900; PP.H4 = 0.87), which matches the known statin–diabetes effect.
- **HMGCR → coronary heart disease:** the eQTL estimate was directionally correct (OR 1.12, 1.05–1.18; q = 0.011) but did not colocalise (PP.H3 > 0.99). An LDL-GWAS-based HMGCR instrument (13 variants) gave OR 1.35 (1.10–1.64) per SD higher LDL for coronary heart disease (p = 0.004).
- **DRD2 → schizophrenia:** all four DRD2 instruments gave OR > 1 (higher expression, higher risk), but none reached FDR significance (best: cortex OR 1.13, 1.00–1.26, p = 0.046; PP.H4 = 0.05). Schizophrenia had only 7,859 cases in the available data.
- **CHRM3 mechanism control:** not confirmed. No peripheral outcome reached q < 0.05 for the thyroid CHRM3 instrument (best: urinary retention OR 0.94, 0.89–0.98, p = 0.010, q = 0.12, PP.H4 = 0.05).
- **Negative controls** (blonde hair, red hair, height, lactose intolerance): no association for any gene (all q > 0.17; for CHRM4 all p ≥ 0.059 and PP.H4 ≤ 0.05).
- **Steiger:** direction was correct for every test.

**Indication check.** Genetically higher CHRM4 expression was not associated with schizophrenia, and the direction was inconsistent:
- blood instrument OR 1.09 (0.84–1.41), p = 0.54;
- skin instrument OR 0.89 (0.67–1.19), p = 0.44;
- PP.H4 ≤ 0.03.

**Screen.** 29 of 637 tests reached q < 0.05: 12 CHRM4, 11 HMGCR, 6 DRD2. Eight met the full candidate rule: four HMGCR positive controls and four CHRM4 tests. The four CHRM4 tests are one skin variant used in two GTEx releases, tested against two outcomes. Higher CHRM4 expression was associated with:
- faster reaction time: β = −0.093 SD per SD, p = 1.2×10⁻¹¹, q = 1.3×10⁻⁹, PP.H4 = 0.86;
- higher fluid intelligence: β = +0.117 SD, p = 2.4×10⁻⁶, q = 1.3×10⁻⁴, PP.H4 = 0.86.

The blood instrument pointed the same way but was weaker: reaction time β = −0.030, p = 0.005, q = 0.09; fluid intelligence β = +0.028, p = 0.15.

The specificity analysis did not support CHRM4 as the responsible gene:
- Reaction time colocalised with 10 of 71 gene × tissue eQTL sets, several more strongly than with CHRM4: ARHGAP1 skin PP.H4 = 0.985, F2 cerebellum 0.984, ACP2 skin 0.980.
- Fluid intelligence colocalised about equally with MDK (skin 0.856), C11orf49 (0.813) and PACSIN3 (cortex 0.802).

Other CHRM4 results with q < 0.05 (BMI, chronotype, LDL, migraine) did not colocalise (PP.H4 ≤ 0.45).

**Novelty.** No published CHRM1/CHRM4 Mendelian randomisation or colocalisation study was found. Cognition is already being tested clinically: xanomeline–trospium is in Alzheimer's cognitive-impairment trials (NCT06976216, NCT06976203).

---

## Part 3 – Three-line recap
1. **Best genetic prediction:** genetically higher CHRM4 expression → faster reaction time and higher fluid intelligence (β −0.09 and +0.12 SD per SD; q < 10⁻³; PP.H4 = 0.86). This is a possible cognitive benefit of M4 agonism. No harm signal and no schizophrenia effect were detected. CHRM1 could not be tested.
2. **Strength: weak.** It rests on one skin-eQTL variant that also regulates 18 other genes. ARHGAP1, F2, ACP2 and MDK eQTLs colocalise with the same signal as well or better, so the effect cannot be pinned on M4. No usable brain instrument exists in GTEx, and the key brain, blood and pQTL resources (MetaBrain, eQTLGen, UKB-PPP) and PGC were unreachable.
3. **Novelty: partly known.** No CHRM4 MR or colocalisation paper exists, but muscarinic cognition benefit is already under trial (Cobenfy in Alzheimer's cognition, NCT06976216/NCT06976203). Overall, read this run as a near-negative feasibility result, not a discovery.

---

### Files
| File | Content |
|---|---|
| `feasibility.md` | Step 0 instrument tables |
| `mr_results.csv` | All 637 tests: estimates, CI, p, q, coloc, SuSiE, Steiger, robustness, specificity flags |
| `top_candidates.md` | Candidate details |
| `figures/forest_CHRM1_CHRM4.png` | CHRM4 effects across all outcomes (CHRM1 has no instrument) |
| `figures/locus_*.png` | LocusZoom-style plots for each candidate |
| `analysis.Rmd` / `analysis.html` | Analysis (house style) and knitted output |
| `scripts/01–09` | Data extraction and instrument selection |
| `decisions_log.md` | Every judgement call |
| `data/clean/` | Clean tables and workbook (`chrm_mr_clean.xlsx`) |
