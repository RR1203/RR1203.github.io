# Step 0 – Feasibility of cis-instruments for CHRM1 and CHRM4 (and contrast genes)

All numbers below were computed from the downloaded GTEx files (scripts 01–05). Sources that could not be reached are listed at the end.

**Rules.**
- Selection: p < 5×10⁻⁶ within the gene ± 500 kb (GRCh38).
- Allele QC: MAF ≥ 1% and ≥ 10 minor-allele copies in the QTL sample, plus presence in 1000G phase 3 EUR with MAF ≥ 1%.
- Clumping: r² < 0.1 in 1000G EUR (n = 503), 1 Mb window.
- F = (β/SE)² per variant.

## Verdict

- **CHRM1: no usable instrument in any brain or blood source.** The only brain hit was the v8 all-ancestry substantia nigra set (lead p = 4.6e-06). It is carried by 4 minor-allele copies and is absent from 1000G EUR. It is not significant in GTEx v10. No sQTL or pQTL source was available.
- **CHRM4 brain: no usable instrument.** The single v8 EUR anterior-cingulate hit (p = 8.1e-08, F = 33.1) rests on 1 minor-allele copy. It is not significant in v10, which has more samples in the same tissue.
- **CHRM4 blood: one usable instrument.** GTEx v10 whole blood (N = 800): 11 variants at p < 5×10⁻⁶ → 1 after clumping, F = 25.8, variance explained R² = 0.031.
- Brain/blood CHRM1/CHRM4 sources passing the stop rule (F > 10): **1**. The analysis therefore continued, for CHRM4 only, using a blood instrument and, as a secondary tissue-consistency source, skin eQTLs.
- **Weakness, stated plainly.** The usable CHRM4 instrument is a single variant from an 800-sample blood eQTL map, for a receptor whose physiological site of action is the brain (striatum). Blood CHRM4 expression is low. The variant is also a stronger eQTL for neighbouring genes (table below). This is a weak and indirect proxy for M4 stimulation.
- **Direction assumption.** Higher receptor expression is taken as agonist-like (more receptor signalling). This is an approximation. An agonist acts acutely and on existing receptor protein, while lifelong higher expression may cause compensation (desensitisation). Expression in blood or skin need not track brain receptor density, and mRNA need not track protein.

## Target genes (CHRM1, CHRM4): every gene × release × tissue with ≥ 1 variant at p < 5×10⁻⁶

| Gene | GTEx release | Tissue | Class | QTL | N | Variants p<5e-6 (cis ±500 kb) | In 1000G EUR | Pass allele QC | Lead minor-allele copies | Lead p | After clumping (r²<0.1) | F (min) | F (mean) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| CHRM1 | v8_ALL | Brain_Substantia_nigra | brain | eQTL | 114 | 5 | 0 | 0 | 4 | 4.6e-06 | 0 | – | – |
| CHRM4 | v10 | Whole_Blood | blood | eQTL | 800 | 11 | 11 | 11 | 106 | 4.8e-07 | 1 | 25.8 | 25.8 |
| CHRM4 | v8_EUR | Brain_Anterior_cingulate_cortex_BA24 | brain | eQTL | 135 | 1 | 1 | 0 | 1 | 8.1e-08 | 0 | – | – |
| CHRM4 | v10 | Skin_Sun_Exposed_Lower_leg | peripheral | eQTL | 751 | 132 | 129 | 129 | 302 | 1.9e-11 | 1 | 46.6 | 46.6 |
| CHRM4 | v10 | Skin_Not_Sun_Exposed_Suprapubic | peripheral | eQTL | 649 | 126 | 123 | 123 | 305 | 2.4e-09 | 1 | 36.7 | 36.7 |
| CHRM4 | v8_ALL | Skin_Sun_Exposed_Lower_leg | peripheral | eQTL | 605 | 50 | 48 | 48 | 250 | 4.9e-08 | 1 | 30.6 | 30.6 |
| CHRM4 | v10 | Thyroid | peripheral | eQTL | 681 | 5 | 0 | 0 | 38 | 1.9e-06 | 0 | – | – |
| CHRM4 | v10 | Adipose_Subcutaneous | peripheral | eQTL | 711 | 2 | 2 | 2 | 332 | 3.5e-06 | 1 | 21.9 | 21.9 |
| CHRM4 | v8_ALL | Lung | peripheral | eQTL | 515 | 9 | 0 | 0 | 25 | 4.4e-06 | 0 | – | – |

Tissue classes with any GTEx significant pair (any p) for the target genes, within ± 500 kb:

| Gene | Class | Tissue-release sets with any significant pair | Best p |
|---|---|---|---|
| CHRM1 | brain | 1 | 4.6e-06 |
| CHRM1 | peripheral | 3 | 1.4e-05 |
| CHRM4 | blood | 1 | 4.8e-07 |
| CHRM4 | brain | 2 | 8.1e-08 |
| CHRM4 | peripheral | 11 | 1.9e-11 |

## Contrast genes (CHRM2, CHRM3, CHRM5) and positive-control genes (DRD2, HMGCR): brain/blood sets, and the peripheral sets used

| Gene | GTEx release | Tissue | Class | QTL | N | Variants p<5e-6 (cis ±500 kb) | In 1000G EUR | Pass allele QC | Lead minor-allele copies | Lead p | After clumping (r²<0.1) | F (min) | F (mean) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| CHRM2 | v10 | Brain_Cerebellar_Hemisphere | brain | eQTL | 276 | 1 | 1 | 0 | 7 | 1.8e-06 | 0 | – | – |
| CHRM3 | v10 | Thyroid | peripheral | eQTL | 681 | 131 | 128 | 128 | 490 | 9.2e-21 | 2 | 23.4 | 58.7 |
| CHRM3 | v8_ALL | Thyroid | peripheral | eQTL | 574 | 124 | 123 | 123 | 423 | 1.6e-16 | 1 | 72.9 | 72.9 |
| CHRM3 | v8_EUR | Thyroid | peripheral | eQTL | 482 | 128 | 127 | 127 | 326 | 5.2e-14 | 1 | 60.8 | 60.8 |
| CHRM5 | v8_ALL | Brain_Spinal_cord_cervical_c-1 | brain | eQTL | 126 | 156 | 151 | 151 | 72 | 1.9e-31 | 2 | 33.8 | 65.9 |
| CHRM5 | v8_ALL | Brain_Putamen_basal_ganglia | brain | eQTL | 170 | 167 | 161 | 161 | 87 | 5.8e-29 | 2 | 26.8 | 57.6 |
| CHRM5 | v8_ALL | Brain_Caudate_basal_ganglia | brain | eQTL | 194 | 144 | 139 | 139 | 103 | 1.4e-28 | 1 | 63.5 | 63.5 |
| CHRM5 | v10 | Brain_Caudate_basal_ganglia | brain | eQTL | 298 | 250 | 238 | 238 | 242 | 8.4e-28 | 1 | 154.6 | 154.6 |
| CHRM5 | v10 | Brain_Spinal_cord_cervical_c-1 | brain | eQTL | 203 | 249 | 237 | 237 | 167 | 1.6e-27 | 1 | 174.3 | 174.3 |
| CHRM5 | v8_ALL | Brain_Cortex | brain | eQTL | 205 | 138 | 133 | 133 | 105 | 6.6e-27 | 2 | 34.7 | 47.1 |
| CHRM5 | v8_EUR | Brain_Spinal_cord_cervical_c-1 | brain | eQTL | 115 | 152 | 147 | 147 | 67 | 9.1e-27 | 2 | 23.9 | 54.6 |
| CHRM5 | v8_EUR | Brain_Putamen_basal_ganglia | brain | eQTL | 153 | 164 | 159 | 159 | 82 | 1.4e-25 | 2 | 24.8 | 55.2 |
| CHRM5 | v8_ALL | Brain_Hippocampus | brain | eQTL | 165 | 122 | 117 | 117 | 89 | 2.5e-25 | 1 | 65.6 | 65.6 |
| CHRM5 | v8_EUR | Brain_Caudate_basal_ganglia | brain | eQTL | 172 | 139 | 134 | 134 | 94 | 9.7e-25 | 1 | 75.8 | 75.8 |
| CHRM5 | v8_EUR | Brain_Hippocampus | brain | eQTL | 150 | 122 | 117 | 117 | 84 | 1.1e-24 | 1 | 65.5 | 65.5 |
| CHRM5 | v10 | Brain_Hippocampus | brain | eQTL | 254 | 205 | 197 | 197 | 219 | 1.3e-24 | 1 | 138.4 | 138.4 |
| CHRM5 | v10 | Brain_Putamen_basal_ganglia | brain | eQTL | 253 | 214 | 208 | 208 | 209 | 1.4e-23 | 2 | 25.3 | 78.1 |
| CHRM5 | v8_EUR | Brain_Cortex | brain | eQTL | 183 | 119 | 115 | 115 | 98 | 1.8e-20 | 1 | 48.4 | 48.4 |
| CHRM5 | v10 | Brain_Frontal_Cortex_BA9 | brain | eQTL | 268 | 160 | 154 | 154 | 139 | 2.5e-18 | 2 | 39.6 | 65.8 |
| CHRM5 | v10 | Brain_Substantia_nigra | brain | eQTL | 183 | 177 | 171 | 171 | 158 | 2.6e-18 | 1 | 101.0 | 101.0 |
| CHRM5 | v8_ALL | Brain_Substantia_nigra | brain | eQTL | 114 | 122 | 117 | 117 | 59 | 3.0e-18 | 1 | 59.6 | 59.6 |
| CHRM5 | v8_ALL | Brain_Frontal_Cortex_BA9 | brain | eQTL | 175 | 115 | 111 | 111 | 88 | 6.5e-18 | 2 | 31.6 | 35.5 |
| CHRM5 | v10 | Brain_Amygdala | brain | eQTL | 180 | 174 | 169 | 169 | 155 | 2.7e-17 | 1 | 93.9 | 93.9 |
| CHRM5 | v10 | Brain_Cortex | brain | eQTL | 268 | 141 | 136 | 136 | 113 | 4.7e-17 | 2 | 23.2 | 53.5 |
| CHRM5 | v8_EUR | Brain_Frontal_Cortex_BA9 | brain | eQTL | 157 | 119 | 115 | 115 | 79 | 2.4e-15 | 2 | 28.2 | 40.1 |
| CHRM5 | v8_EUR | Brain_Substantia_nigra | brain | eQTL | 100 | 121 | 117 | 117 | 52 | 2.5e-15 | 1 | 54.5 | 54.5 |
| CHRM5 | v8_ALL | Brain_Amygdala | brain | eQTL | 129 | 50 | 49 | 49 | 79 | 6.3e-15 | 1 | 48.6 | 48.6 |
| CHRM5 | v10 | Brain_Cerebellum | brain | eQTL | 264 | 122 | 119 | 119 | 219 | 9.6e-15 | 2 | 27.5 | 48.6 |
| CHRM5 | v8_ALL | Brain_Anterior_cingulate_cortex_BA24 | brain | eQTL | 147 | 58 | 54 | 54 | 75 | 1.7e-14 | 1 | 33.1 | 33.1 |
| CHRM5 | v10 | Brain_Hypothalamus | brain | eQTL | 256 | 135 | 132 | 132 | 97 | 1.2e-13 | 2 | 26.9 | 45.2 |
| CHRM5 | v8_EUR | Brain_Anterior_cingulate_cortex_BA24 | brain | eQTL | 135 | 69 | 65 | 65 | 72 | 1.2e-13 | 1 | 32.6 | 32.6 |
| CHRM5 | v8_EUR | Brain_Amygdala | brain | eQTL | 119 | 30 | 29 | 29 | 74 | 2.2e-12 | 1 | 40.3 | 40.3 |
| CHRM5 | v8_ALL | Brain_Cerebellum | brain | eQTL | 209 | 32 | 31 | 31 | 109 | 2.6e-12 | 1 | 34.1 | 34.1 |
| CHRM5 | v10 | Brain_Anterior_cingulate_cortex_BA24 | brain | eQTL | 233 | 135 | 130 | 130 | 89 | 1.0e-11 | 1 | 52.5 | 52.5 |
| CHRM5 | v10 | Brain_Cerebellar_Hemisphere | brain | eQTL | 276 | 72 | 70 | 70 | 229 | 7.7e-11 | 1 | 46.8 | 46.8 |
| CHRM5 | v8_ALL | Brain_Hypothalamus | brain | eQTL | 170 | 1 | 0 | 0 | 87 | 4.4e-10 | 0 | – | – |
| CHRM5 | v8_EUR | Brain_Cerebellum | brain | eQTL | 188 | 28 | 27 | 27 | 102 | 8.7e-10 | 1 | 26.9 | 26.9 |
| CHRM5 | v10 | Brain_Nucleus_accumbens_basal_ganglia | brain | eQTL | 284 | 113 | 110 | 110 | 252 | 8.3e-09 | 1 | 35.8 | 35.8 |
| CHRM5 | v8_ALL | Brain_Nucleus_accumbens_basal_ganglia | brain | eQTL | 202 | 1 | 0 | 0 | 107 | 2.1e-08 | 0 | – | – |
| CHRM5 | v8_EUR | Brain_Hypothalamus | brain | eQTL | 156 | 1 | 0 | 0 | 80 | 4.9e-08 | 0 | – | – |
| CHRM5 | v8_ALL | Brain_Cerebellar_Hemisphere | brain | eQTL | 175 | 21 | 20 | 20 | 48 | 1.3e-07 | 1 | 31.1 | 31.1 |
| CHRM5 | v8_EUR | Brain_Nucleus_accumbens_basal_ganglia | brain | eQTL | 181 | 1 | 0 | 0 | 98 | 3.0e-07 | 0 | – | – |
| CHRM5 | v10 | Nerve_Tibial | peripheral | eQTL | 667 | 222 | 211 | 211 | 151 | 4.3e-65 | 2 | 39.3 | 206.8 |
| CHRM5 | v8_ALL | Nerve_Tibial | peripheral | eQTL | 532 | 181 | 172 | 172 | 118 | 3.8e-49 | 2 | 34.8 | 156.2 |
| CHRM5 | v8_EUR | Nerve_Tibial | peripheral | eQTL | 438 | 170 | 163 | 163 | 73 | 1.5e-36 | 2 | 30.5 | 115.2 |
| CHRM5 | v10 | Thyroid | peripheral | eQTL | 681 | 74 | 72 | 72 | 313 | 4.3e-11 | 2 | 27.3 | 36.2 |
| CHRM5 | v8_ALL | Muscle_Skeletal | peripheral | eQTL | 706 | 59 | 58 | 58 | 298 | 8.8e-11 | 1 | 43.5 | 43.5 |
| CHRM5 | v8_ALL | Skin_Sun_Exposed_Lower_leg | peripheral | eQTL | 605 | 38 | 38 | 38 | 262 | 3.9e-10 | 1 | 40.6 | 40.6 |
| CHRM5 | v8_EUR | Skin_Sun_Exposed_Lower_leg | peripheral | eQTL | 508 | 57 | 57 | 57 | 220 | 3.1e-09 | 1 | 36.6 | 36.6 |
| CHRM5 | v8_EUR | Muscle_Skeletal | peripheral | eQTL | 588 | 45 | 44 | 44 | 248 | 6.1e-08 | 1 | 30.2 | 30.2 |
| CHRM5 | v8_ALL | Thyroid | peripheral | eQTL | 574 | 15 | 15 | 15 | 250 | 1.2e-07 | 1 | 28.9 | 28.9 |
| CHRM5 | v10 | Skin_Sun_Exposed_Lower_leg | peripheral | eQTL | 751 | 9 | 9 | 9 | 337 | 5.8e-07 | 1 | 25.5 | 25.5 |
| DRD2 | v10 | Brain_Cortex | brain | eQTL | 268 | 11 | 11 | 11 | 187 | 1.4e-08 | 1 | 34.8 | 34.8 |
| DRD2 | v8_ALL | Brain_Frontal_Cortex_BA9 | brain | eQTL | 175 | 1 | 1 | 1 | 116 | 3.9e-07 | 1 | 28.5 | 28.5 |
| DRD2 | v10 | Brain_Spinal_cord_cervical_c-1 | brain | eQTL | 203 | 1 | 1 | 1 | 140 | 8.6e-07 | 1 | 26.2 | 26.2 |
| DRD2 | v10 | Brain_Hippocampus | brain | eQTL | 254 | 7 | 6 | 6 | 104 | 1.2e-06 | 1 | 25.1 | 25.1 |
| DRD2 | v8_ALL | Brain_Cerebellar_Hemisphere | brain | eQTL | 175 | 2 | 2 | 2 | 137 | 1.9e-06 | 1 | 24.8 | 24.8 |
| DRD2 | v10 | Brain_Cerebellum | brain | eQTL | 264 | 2 | 2 | 2 | 214 | 2.6e-06 | 1 | 23.3 | 23.3 |
| DRD2 | v8_EUR | Brain_Cerebellum | brain | eQTL | 188 | 1 | 1 | 1 | 44 | 2.8e-06 | 1 | 23.7 | 23.7 |
| DRD2 | v8_ALL | Brain_Hippocampus | brain | eQTL | 165 | 2 | 2 | 2 | 47 | 3.5e-06 | 1 | 23.6 | 23.6 |
| DRD2 | v10 | Nerve_Tibial | peripheral | eQTL | 667 | 348 | 338 | 338 | 443 | 2.4e-37 | 6 | 23.5 | 68.9 |
| DRD2 | v8_ALL | Nerve_Tibial | peripheral | eQTL | 532 | 316 | 308 | 308 | 348 | 1.2e-28 | 4 | 24.2 | 72.2 |
| DRD2 | v8_EUR | Nerve_Tibial | peripheral | eQTL | 438 | 298 | 292 | 292 | 322 | 8.9e-25 | 3 | 32.6 | 73.9 |
| DRD2 | v10 | Skin_Sun_Exposed_Lower_leg | peripheral | eQTL | 751 | 253 | 246 | 246 | 502 | 3.6e-24 | 4 | 23.5 | 53.4 |
| DRD2 | v10 | Muscle_Skeletal | peripheral | eQTL | 816 | 192 | 185 | 185 | 482 | 9.9e-23 | 4 | 24.8 | 45.2 |
| DRD2 | v8_ALL | Muscle_Skeletal | peripheral | eQTL | 706 | 190 | 186 | 186 | 402 | 4.3e-21 | 4 | 21.6 | 42.0 |
| DRD2 | v8_EUR | Muscle_Skeletal | peripheral | eQTL | 588 | 185 | 181 | 181 | 337 | 6.5e-19 | 3 | 27.0 | 47.5 |
| DRD2 | v8_ALL | Skin_Sun_Exposed_Lower_leg | peripheral | eQTL | 605 | 223 | 218 | 218 | 396 | 2.3e-18 | 2 | 38.7 | 60.5 |
| DRD2 | v8_EUR | Skin_Sun_Exposed_Lower_leg | peripheral | eQTL | 508 | 180 | 176 | 176 | 370 | 3.5e-17 | 2 | 28.7 | 53.0 |
| HMGCR | v8_ALL_sQTL | Brain_Cerebellar_Hemisphere | brain | sQTL | 175 | 5 | 5 | 5 | 12 | 3.7e-09 | 1 | 39.3 | 39.3 |
| HMGCR | v10 | Brain_Anterior_cingulate_cortex_BA24 | brain | eQTL | 233 | 1 | 0 | 0 | 1 | 5.4e-09 | 0 | – | – |
| HMGCR | v8_ALL | Brain_Substantia_nigra | brain | eQTL | 114 | 1 | 1 | 0 | 2 | 3.2e-06 | 0 | – | – |
| HMGCR | v10 | Muscle_Skeletal | peripheral | eQTL | 816 | 305 | 292 | 292 | 782 | 1.1e-11 | 1 | 47.7 | 47.7 |
| HMGCR | v8_ALL | Muscle_Skeletal | peripheral | eQTL | 706 | 65 | 63 | 63 | 690 | 6.4e-10 | 1 | 39.4 | 39.4 |
| HMGCR | v8_ALL_sQTL | Muscle_Skeletal | peripheral | sQTL | 706 | 13 | 12 | 12 | 538 | 2.3e-08 | 1 | 32.0 | 32.0 |
| HMGCR | v8_EUR | Muscle_Skeletal | peripheral | eQTL | 588 | 46 | 45 | 45 | 463 | 3.2e-08 | 1 | 31.5 | 31.5 |

The full table across all 49 GTEx tissues (169 gene × release × tissue × QTL-type sets) is in `data/clean/feasibility_all_tissues.tsv`.

## Exposures carried into MR (pre-specified choice rule, see decisions_log.md #13)

| Exposure | Role | Class | N | Variants | F (min) | F (mean) |
|---|---|---|---|---|---|---|
| CHRM3|v10|Thyroid|eQTL | contrast/mechanism control | peripheral | 681 | 2 | 23.4 | 58.7 |
| CHRM3|v8_EUR|Thyroid|eQTL | contrast/mechanism control | peripheral | 482 | 1 | 60.8 | 60.8 |
| CHRM4|v10|Whole_Blood|eQTL | target | blood | 800 | 1 | 25.8 | 25.8 |
| CHRM4|v10|Skin_Sun_Exposed_Lower_leg|eQTL | target | peripheral | 751 | 1 | 46.6 | 46.6 |
| CHRM4|v8_ALL|Skin_Sun_Exposed_Lower_leg|eQTL | target | peripheral | 605 | 1 | 30.6 | 30.6 |
| CHRM5|v10|Brain_Caudate_basal_ganglia|eQTL | contrast | brain | 298 | 1 | 154.6 | 154.6 |
| CHRM5|v8_EUR|Brain_Spinal_cord_cervical_c-1|eQTL | contrast | brain | 115 | 2 | 23.9 | 54.6 |
| DRD2|v10|Brain_Cortex|eQTL | positive control | brain | 268 | 1 | 34.8 | 34.8 |
| DRD2|v8_EUR|Brain_Cerebellum|eQTL | positive control | brain | 188 | 1 | 23.7 | 23.7 |
| DRD2|v10|Nerve_Tibial|eQTL | positive control | peripheral | 667 | 6 | 23.5 | 68.9 |
| DRD2|v8_EUR|Nerve_Tibial|eQTL | positive control | peripheral | 438 | 3 | 32.6 | 73.9 |
| HMGCR|v10|Muscle_Skeletal|eQTL | positive control | peripheral | 816 | 1 | 47.7 | 47.7 |
| HMGCR|v8_EUR|Muscle_Skeletal|eQTL | positive control | peripheral | 588 | 1 | 31.5 | 31.5 |

## Other genes regulated by each instrument (any GTEx v8/v10 tissue; first 12 by p shown)

| Exposure | Variant | No. other genes | Other genes (tissue, release, p, β) |
|---|---|---|---|
| CHRM3|v10|Thyroid|eQTL | chr1_239165662_A_G_b38 | 0 |  |
| CHRM3|v10|Thyroid|eQTL | chr1_239287532_G_A_b38 | 0 |  |
| CHRM3|v8_EUR|Thyroid|eQTL | chr1_239287532_G_A_b38 | 0 |  |
| CHRM4|v10|Skin_Sun_Exposed_Lower_leg|eQTL | chr11_46356220_T_C_b38 | 18 | ATG13(Cells_Cultured_fibroblasts,v10,p=6.6e-18,b=-0.19); ARHGAP1(Pancreas,v10,p=2.7e-12,b=-0.28); MDK(Esophagus_Muscularis,v10,p=2.0e-11,b=-0.21); C11orf49(Testis,v10,p=3.2e-10,b=-0.31); LRP4(Pancreas,v10,p=8.4e-09,b=-0.34); PACSIN3(Thyroid,v8_ALL,p=8.0e-08,b=+0.17); MADD(Muscle_Skeletal,v10,p=2.7e-07,b=+0.15); DDB2(Skin_Not_Sun_Exposed_Suprapubic,v8_EUR,p=7.8e-07,b=+0.16); ENSG00000270060(Adipose_Visceral_Omentum,v10,p=2.6e-06,b=+0.21); F2(Artery_Tibial,v10,p=2.8e-06,b=-0.23); ENSG00000271350(Testis,v10,p=4.4e-06,b=+0.41); ACP2(Brain_Spinal_cord_cervical_c-1,v10,p=4.4e-06,b=-0.25) |
| CHRM4|v10|Whole_Blood|eQTL | chr11_46478978_C_T_b38 | 9 | ATG13(Cells_Cultured_fibroblasts,v10,p=2.6e-23,b=-0.34); PACSIN3(Skin_Not_Sun_Exposed_Suprapubic,v8_EUR,p=1.1e-12,b=+0.33); MDK(Lung,v10,p=1.1e-07,b=-0.28); DGKZ(Whole_Blood,v10,p=5.3e-06,b=+0.12); MADD(Muscle_Skeletal,v10,p=1.8e-05,b=+0.20); ACP2(Skin_Sun_Exposed_Lower_leg,v8_EUR,p=7.7e-05,b=-0.22); C11orf49(Nerve_Tibial,v10,p=1.3e-04,b=+0.18); F2(Brain_Nucleus_accumbens_basal_ganglia,v10,p=2.2e-04,b=-0.39); ARFGAP2(Cells_EBV-transformed_lymphocytes,v10,p=3.1e-04,b=+0.17) |
| CHRM4|v8_ALL|Skin_Sun_Exposed_Lower_leg|eQTL | chr11_46356220_T_C_b38 | 18 | ATG13(Cells_Cultured_fibroblasts,v10,p=6.6e-18,b=-0.19); ARHGAP1(Pancreas,v10,p=2.7e-12,b=-0.28); MDK(Esophagus_Muscularis,v10,p=2.0e-11,b=-0.21); C11orf49(Testis,v10,p=3.2e-10,b=-0.31); LRP4(Pancreas,v10,p=8.4e-09,b=-0.34); PACSIN3(Thyroid,v8_ALL,p=8.0e-08,b=+0.17); MADD(Muscle_Skeletal,v10,p=2.7e-07,b=+0.15); DDB2(Skin_Not_Sun_Exposed_Suprapubic,v8_EUR,p=7.8e-07,b=+0.16); ENSG00000270060(Adipose_Visceral_Omentum,v10,p=2.6e-06,b=+0.21); F2(Artery_Tibial,v10,p=2.8e-06,b=-0.23); ENSG00000271350(Testis,v10,p=4.4e-06,b=+0.41); ACP2(Brain_Spinal_cord_cervical_c-1,v10,p=4.4e-06,b=-0.25) |
| CHRM5|v10|Brain_Caudate_basal_ganglia|eQTL | chr15_33985176_A_G_b38 | 10 | ENSG00000287840(Testis,v10,p=2.9e-51,b=+0.96); AVEN(Cells_Cultured_fibroblasts,v10,p=6.9e-40,b=-0.31); ENSG00000259505(Testis,v10,p=1.1e-26,b=+0.70); RPL32P2(Brain_Spinal_cord_cervical_c-1,v10,p=3.6e-14,b=+0.68); RYR3(Cells_Cultured_fibroblasts,v10,p=5.4e-12,b=-0.30); ENSG00000259287(Cells_Cultured_fibroblasts,v8_ALL,p=2.2e-07,b=-0.27); PGBD4(Nerve_Tibial,v8_ALL,p=2.3e-07,b=+0.18); EMC7(Nerve_Tibial,v8_ALL,p=2.7e-07,b=+0.08); ENSG00000259408(Brain_Cerebellar_Hemisphere,v10,p=5.1e-07,b=-0.29); ENSG00000278472(Testis,v10,p=3.1e-05,b=+0.30) |
| CHRM5|v8_EUR|Brain_Spinal_cord_cervical_c-1|eQTL | chr15_33986401_G_A_b38 | 8 | AVEN(Nerve_Tibial,v10,p=1.0e-20,b=+0.36); ENSG00000287840(Testis,v10,p=5.4e-14,b=+0.91); ENSG00000259505(Testis,v10,p=5.2e-12,b=+0.80); ENSG00000259408(Nerve_Tibial,v10,p=3.9e-10,b=+0.41); ENSG00000259287(Nerve_Tibial,v8_ALL,p=6.9e-07,b=+0.41); PGBD4(Nerve_Tibial,v8_ALL,p=2.5e-05,b=+0.24); NOP10(Nerve_Tibial,v8_EUR,p=7.8e-05,b=+0.13); EMC7(Nerve_Tibial,v10,p=1.0e-04,b=+0.08) |
| CHRM5|v8_EUR|Brain_Spinal_cord_cervical_c-1|eQTL | chr15_34056771_C_T_b38 | 9 | AVEN(Cells_Cultured_fibroblasts,v10,p=3.5e-40,b=-0.34); ENSG00000287840(Testis,v10,p=2.2e-31,b=+0.85); ENSG00000259505(Testis,v8_EUR,p=5.1e-17,b=+0.80); ENSG00000259408(Skin_Not_Sun_Exposed_Suprapubic,v10,p=2.4e-10,b=-0.25); RYR3(Cells_Cultured_fibroblasts,v10,p=1.0e-07,b=-0.25); ENSG00000259287(Thyroid,v10,p=1.6e-07,b=-0.25); RPL32P2(Brain_Spinal_cord_cervical_c-1,v10,p=3.7e-07,b=+0.56); ENSG00000278472(Testis,v10,p=3.7e-07,b=+0.39); GOLGA8B(Artery_Tibial,v8_ALL,p=2.4e-05,b=+0.19) |
| DRD2|v10|Brain_Cortex|eQTL | chr11_113695485_C_A_b38 | 5 | LRRC37A13P(Testis,v10,p=1.7e-21,b=+0.62); ATF4P4(Testis,v10,p=4.4e-21,b=+0.68); TMPRSS5(Muscle_Skeletal,v8_ALL,p=9.4e-08,b=+0.16); TTC12(Muscle_Skeletal,v10,p=2.8e-05,b=-0.17); USP28(Muscle_Skeletal,v10,p=8.5e-05,b=-0.08) |
| DRD2|v10|Nerve_Tibial|eQTL | chr11_113466435_G_GC_b38 | 1 | ANKK1(Muscle_Skeletal,v10,p=9.8e-06,b=+0.27) |
| DRD2|v10|Nerve_Tibial|eQTL | chr11_113652008_C_T_b38 | 3 | USP28(Skin_Sun_Exposed_Lower_leg,v10,p=4.2e-05,b=+0.28); LRRC37A13P(Testis,v10,p=9.6e-05,b=-0.54); TMPRSS5(Esophagus_Muscularis,v10,p=1.4e-04,b=-0.33) |
| DRD2|v10|Nerve_Tibial|eQTL | chr11_113699683_T_C_b38 | 7 | LRRC37A13P(Testis,v10,p=2.3e-25,b=+0.65); ATF4P4(Testis,v10,p=6.5e-24,b=+0.70); TMPRSS5(Brain_Caudate_basal_ganglia,v10,p=3.1e-12,b=+0.38); USP28(Cells_EBV-transformed_lymphocytes,v10,p=3.7e-10,b=-0.27); ENSG00000256757(Minor_Salivary_Gland,v10,p=8.5e-09,b=+0.49); MTRF1LP1(Skin_Not_Sun_Exposed_Suprapubic,v8_ALL,p=5.0e-05,b=+0.24); ZW10(Skin_Not_Sun_Exposed_Suprapubic,v10,p=6.9e-05,b=+0.07) |
| DRD2|v10|Nerve_Tibial|eQTL | chr11_113713455_G_A_b38 | 1 | TMPRSS5(Muscle_Skeletal,v8_ALL,p=4.8e-09,b=+0.24) |
| DRD2|v10|Nerve_Tibial|eQTL | chr11_113889946_TA_T_b38 | 6 | TMPRSS5(Brain_Spinal_cord_cervical_c-1,v10,p=4.3e-13,b=+0.95); LRRC37A13P(Testis,v10,p=7.8e-10,b=-0.55); ANKK1(Muscle_Skeletal,v10,p=1.0e-08,b=+0.34); ATF4P4(Testis,v10,p=1.4e-08,b=-0.56); ZW10(Muscle_Skeletal,v10,p=8.2e-05,b=+0.10); MTRF1LP1(Skin_Sun_Exposed_Lower_leg,v10,p=1.0e-04,b=+0.26) |
| DRD2|v10|Nerve_Tibial|eQTL | chr11_113975284_T_C_b38 | 4 | ATF4P4(Testis,v8_EUR,p=2.9e-12,b=-0.72); LRRC37A13P(Testis,v8_EUR,p=3.3e-12,b=-0.64); TTC12(Muscle_Skeletal,v8_EUR,p=2.6e-05,b=+0.22); TMPRSS5(Muscle_Skeletal,v10,p=1.2e-04,b=-0.12) |
| DRD2|v8_EUR|Brain_Cerebellum|eQTL | chr11_113713455_G_A_b38 | 1 | TMPRSS5(Muscle_Skeletal,v8_ALL,p=4.8e-09,b=+0.24) |
| DRD2|v8_EUR|Nerve_Tibial|eQTL | chr11_113699683_T_C_b38 | 7 | LRRC37A13P(Testis,v10,p=2.3e-25,b=+0.65); ATF4P4(Testis,v10,p=6.5e-24,b=+0.70); TMPRSS5(Brain_Caudate_basal_ganglia,v10,p=3.1e-12,b=+0.38); USP28(Cells_EBV-transformed_lymphocytes,v10,p=3.7e-10,b=-0.27); ENSG00000256757(Minor_Salivary_Gland,v10,p=8.5e-09,b=+0.49); MTRF1LP1(Skin_Not_Sun_Exposed_Suprapubic,v8_ALL,p=5.0e-05,b=+0.24); ZW10(Skin_Not_Sun_Exposed_Suprapubic,v10,p=6.9e-05,b=+0.07) |
| DRD2|v8_EUR|Nerve_Tibial|eQTL | chr11_113713455_G_A_b38 | 1 | TMPRSS5(Muscle_Skeletal,v8_ALL,p=4.8e-09,b=+0.24) |
| DRD2|v8_EUR|Nerve_Tibial|eQTL | chr11_113975284_T_C_b38 | 4 | ATF4P4(Testis,v8_EUR,p=2.9e-12,b=-0.72); LRRC37A13P(Testis,v8_EUR,p=3.3e-12,b=-0.64); TTC12(Muscle_Skeletal,v8_EUR,p=2.6e-05,b=+0.22); TMPRSS5(Muscle_Skeletal,v10,p=1.2e-04,b=-0.12) |
| HMGCR|v10|Muscle_Skeletal|eQTL | chr5_75355259_A_G_b38 | 7 | ANKDD1B(Nerve_Tibial,v10,p=8.8e-19,b=-0.27); GCNT4(Testis,v10,p=1.2e-15,b=+0.42); POLK(Brain_Cerebellar_Hemisphere,v10,p=7.2e-10,b=+0.18); CERT1(Esophagus_Mucosa,v8_ALL,p=1.5e-07,b=-0.13); CTD-2235C13.3(Skin_Sun_Exposed_Lower_leg,v8_ALL,p=2.6e-05,b=-0.20); LINC01336(Testis,v8_ALL,p=2.9e-05,b=+0.28); ENSG00000272040(Adipose_Subcutaneous,v10,p=8.0e-05,b=-0.14) |
| HMGCR|v8_EUR|Muscle_Skeletal|eQTL | chr5_75321437_G_A_b38 | 7 | ANKDD1B(Nerve_Tibial,v10,p=3.6e-18,b=-0.26); GCNT4(Testis,v10,p=9.6e-16,b=+0.42); CERT1(Esophagus_Mucosa,v8_ALL,p=2.4e-10,b=-0.15); POLK(Brain_Cerebellar_Hemisphere,v10,p=1.7e-08,b=+0.17); LINC01336(Testis,v8_ALL,p=9.2e-06,b=+0.31); POC5(Brain_Cerebellar_Hemisphere,v10,p=5.8e-05,b=+0.22); CTD-2235C13.3(Skin_Sun_Exposed_Lower_leg,v8_EUR,p=1.1e-04,b=-0.20) |

## Sources not checked (unreachable from this environment)

- MetaBrain, PsychENCODE (brain eQTL); eQTLGen (blood eQTL); UKB-PPP, deCODE, Fenland (pQTL); eQTL Catalogue.
- Whether CHRM1/CHRM4 are measured on those protein panels, and whether they carry stronger instruments, **is unknown**. A larger brain or blood eQTL resource could change this verdict.
