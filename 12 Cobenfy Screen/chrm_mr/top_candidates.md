# Top candidates

**Formal candidate rule** (from the brief): q < 0.05 AND coloc PP.H4 > 0.8 AND consistent direction across sensitivity methods and tissues.

8 of 637 tests met the rule:
- 4 are the HMGCR positive control (muscle eQTL → LDL and T2D, GTEx v8 and v10).
- 4 are CHRM4. These are one variant (chr11:46,356,220 T>C, GRCh38) used as a skin eQTL in GTEx v8 and v10, tested against two outcomes: reaction time and fluid intelligence.

**Bottom line: no candidate can be attributed to CHRM4.** The CHRM4 pair passes the formal rule. However, the same cognition signals colocalise as strongly or more strongly with eQTLs for other genes at the locus (specificity check below). For CHRM1, nothing could be tested (no instrument).

---

## 1. Genetically higher CHRM4 (skin eQTL) → faster reaction time

| Item | Value |
|---|---|
| Direction | Genetically higher CHRM4 expression → **lower (faster) reaction time** |
| Effect (GTEx v10 skin, N = 751; Wald ratio) | β = −0.093 SD of reaction time per 1 SD higher CHRM4 expression (SE 0.014), p = 1.2×10⁻¹¹, q = 1.3×10⁻⁹ |
| Same variant, GTEx v8 skin (all ancestry) | β = −0.098 (SE 0.015), p = 1.2×10⁻¹¹ |
| Blood instrument (different variant, chr11:46,478,978 C>T, v10 whole blood) | β = −0.030 (SE 0.011), p = 0.005, q = 0.092; PP.H4 = 0.47 (same direction, not significant after FDR, no coloc) |
| Colocalisation (skin) | PP.H4 = 0.86, PP.H3 = 0.14. Restricted to significant-pair variants: PP.H4 = 0.96. SuSiE (outcome side): max PP.H4 = 0.89 |
| Instrument strength | F = 46.6 (v10), 30.6 (v8). Single variant, so no Egger, weighted median or leave-one-out |
| Steiger | Correct direction |
| Outcome | UK Biobank field 20023, mean time to correctly identify matches (inverse-normal), Pan-UKB EUR, N = 417,660 |
| **Specificity check** | Reaction time colocalises with 10 of 71 gene × tissue eQTLs at the locus at PP.H4 > 0.8. Several are **higher than CHRM4**: ARHGAP1 skin 0.985, F2 cerebellum 0.984, ACP2 skin 0.980, ARHGAP1 blood 0.978. MDK (cortex 0.80) also passes. The signal sits on a ~350 kb LD block (figure). |
| Neighbouring-gene pleiotropy | The instrument is a significant eQTL for 18 other genes, e.g. ATG13 (p = 6.6×10⁻¹⁸), ARHGAP1 (2.7×10⁻¹²), MDK (2.0×10⁻¹¹), C11orf49, LRP4, PACSIN3, MADD, DDB2, F2, ACP2 |
| Tissue | Skin (peripheral). Not brain. CHRM4 has no QC-passing brain eQTL |
| Implication for Cobenfy | If causal through M4, it would suggest a cognitive **benefit** (faster processing speed). The genetic data cannot say whether the effect runs through CHRM4 or a neighbouring gene, so treat this as **not attributable** to M4. |
| Novelty | **Partly known.** No published CHRM1/CHRM4 MR or colocalisation paper was found (Europe PMC, PubMed, 2026-11-13). Cognition is already a clinical target: KarXT/KarXT+KarX-EC trials in Alzheimer's cognitive impairment (NCT06976216, NCT06976203, recruiting); a schizophrenia cognitive-impairment trial (NCT07084831, withdrawn); and a 2026 systematic review of xanomeline in cognitive impairment (PMID 41418563). |
| Suggested next test | Re-run with brain eQTL/pQTL resources that were unreachable here (MetaBrain cortex/basal ganglia, PsychENCODE, eQTLGen, UKB-PPP if CHRM4 is measured). Use multi-trait colocalisation (e.g. HyPrColoc) across CHRM4, ARHGAP1, F2, ACP2 and MDK to see whether any gene is preferred. Test the cognitive endpoints of the ongoing Alzheimer's cognition trials. |

Figure: `figures/locus_CHRM4_v10_Skin_Sun_Exposed_Lower_leg_eQTL__RT.png` (also the v8 version).

## 2. Genetically higher CHRM4 (skin eQTL) → higher fluid intelligence

| Item | Value |
|---|---|
| Direction | Genetically higher CHRM4 expression → **higher fluid intelligence score** |
| Effect (GTEx v10 skin; Wald ratio) | β = +0.117 SD per 1 SD higher CHRM4 expression (SE 0.025), p = 2.4×10⁻⁶, q = 1.3×10⁻⁴ |
| Same variant, v8 skin | β = +0.124 (SE 0.026) |
| Blood instrument | β = +0.028 (SE 0.019), p = 0.15; PP.H4 = 0.55 (same direction, not significant) |
| Colocalisation (skin) | PP.H4 = 0.86, PP.H3 = 0.13. Restricted to significant-pair variants: 0.93. SuSiE not run (outcome min p > 10⁻⁶ in window) |
| Outcome | UK Biobank field 20016 (inverse-normal), Pan-UKB EUR, N = 135,088 |
| **Specificity check** | 7 of 71 gene × tissue eQTLs colocalise at PP.H4 > 0.8. CHRM4 skin 0.860 is matched by MDK (skin 0.856, cortex 0.837, hippocampus 0.811, caudate 0.803), C11orf49 skin 0.813 and PACSIN3 cortex 0.802. |
| Implication for Cobenfy | Same as above: a possible cognitive benefit, **not attributable** to M4 with these data |
| Novelty | Partly known (same evidence as #1) |
| Next test | Same as #1 |

Figure: `figures/locus_CHRM4_v10_Skin_Sun_Exposed_Lower_leg_eQTL__FI.png`.

## Positive-control "candidates" (method check, not Cobenfy predictions)

| Exposure | Outcome | Estimate | p | PP.H4 | Reading |
|---|---|---|---|---|---|
| HMGCR, v10 muscle | LDL | β = +0.395 SD per SD expression (SE 0.013) | 4.0×10⁻¹⁹⁴ | 0.98 | Higher HMGCR → higher LDL: **reproduces** the statin target |
| HMGCR, v8 EUR muscle | LDL | β = +0.424 (SE 0.015) | 1.3×10⁻¹⁸⁰ | 0.99 | Same |
| HMGCR, v10 muscle | T2D | OR 0.854 (0.811–0.900) | 3.0×10⁻⁹ | 0.87 | Lower HMGCR → higher T2D. Same direction as the known statin–diabetes effect |
| HMGCR, v8 EUR muscle | T2D | OR 0.844 (0.797–0.895) | 9.4×10⁻⁹ | 0.90 | Same |

## Results with q < 0.05 for CHRM4 that failed colocalisation (not candidates)

| Outcome | Skin v10 estimate | q | PP.H4 / PP.H3 |
|---|---|---|---|
| BMI | β = −0.076 (SE 0.016) | 1.1×10⁻⁴ | 0.45 / 0.55 |
| Chronotype (UKB 1180) | β = +0.052 (SE 0.015) | 0.013 | 0.14 / 0.77 |
| LDL | β = +0.052 (SE 0.015) | 0.017 | 0.45 / 0.12 |
| Migraine | OR 1.20 (1.07–1.33) | 0.029 | 0.31 / 0.07 |

All of these use the same pleiotropic skin variant.
