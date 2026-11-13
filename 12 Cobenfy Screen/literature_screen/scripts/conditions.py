# Condition list: key -> (label, group, PubMed term)
BENEFIT = {
 # psychiatric
 "bipolar_mania": ("Bipolar mania","psychiatric",'(mania[tiab] OR manic[tiab] OR "Bipolar Disorder"[mh])'),
 "bipolar_depression": ("Bipolar depression","psychiatric",'("bipolar depression"[tiab] OR (bipolar[tiab] AND depressive episode*[tiab]))'),
 "mdd": ("Major depressive disorder","psychiatric",'("Depressive Disorder, Major"[mh] OR "major depression"[tiab] OR "major depressive"[tiab])'),
 "ocd": ("OCD","psychiatric",'("Obsessive-Compulsive Disorder"[mh] OR obsessive-compulsive[tiab])'),
 "tourette": ("Tourette / tics","psychiatric",'("Tourette Syndrome"[mh] OR tourette*[tiab] OR "tic disorder*"[tiab])'),
 "autism_irritability": ("Autism (irritability)","psychiatric",'("Autism Spectrum Disorder"[mh] OR autis*[tiab])'),
 "adhd": ("ADHD","psychiatric",'("Attention Deficit Disorder with Hyperactivity"[mh] OR ADHD[tiab])'),
 "ptsd": ("PTSD","psychiatric",'("Stress Disorders, Post-Traumatic"[mh] OR PTSD[tiab] OR posttraumatic stress[tiab])'),
 "cocaine": ("Cocaine use disorder","psychiatric",'(cocaine[tiab] OR "Cocaine-Related Disorders"[mh])'),
 "methamphetamine": ("Methamphetamine use disorder","psychiatric",'(methamphetamine[tiab] OR amphetamine-related[tiab])'),
 "alcohol": ("Alcohol use disorder","psychiatric",'("Alcoholism"[mh] OR "alcohol use disorder"[tiab] OR "alcohol dependence"[tiab])'),
 "nicotine": ("Nicotine dependence","psychiatric",'("Tobacco Use Disorder"[mh] OR "nicotine dependence"[tiab] OR "smoking cessation"[tiab])'),
 "delirium": ("Delirium","psychiatric",'("Delirium"[mh] OR delirium[tiab])'),
 "catatonia": ("Catatonia","psychiatric",'(catatoni*[tiab])'),
 "anorexia": ("Anorexia nervosa","psychiatric",'("Anorexia Nervosa"[mh] OR "anorexia nervosa"[tiab])'),
 "binge_eating": ("Binge eating / obesity","other",'("Binge-Eating Disorder"[mh] OR "binge eating"[tiab] OR obesity[tiab])'),
 "borderline": ("Borderline personality","psychiatric",'("Borderline Personality Disorder"[mh] OR "borderline personality"[tiab])'),
 # neurologic
 "ad_psychosis": ("Alzheimer psychosis/agitation","neurologic",'("Alzheimer Disease"[mh] OR alzheimer*[tiab]) AND (psychosis[tiab] OR psychotic[tiab] OR agitation[tiab] OR hallucinat*[tiab] OR delusion*[tiab])'),
 "dementia_cognition": ("Alzheimer cognition","neurologic",'("Alzheimer Disease"[mh] OR alzheimer*[tiab]) AND (cognit*[tiab] OR memory[tiab])'),
 "dlb": ("Lewy body dementia","neurologic",'("Lewy Body Disease"[mh] OR "lewy bod*"[tiab])'),
 "pd_psychosis": ("Parkinson psychosis","neurologic",'("Parkinson Disease"[mh] OR parkinson*[tiab]) AND (psychosis[tiab] OR hallucinat*[tiab])'),
 "pd_cognition": ("Parkinson cognitive impairment","neurologic",'("Parkinson Disease"[mh] OR parkinson*[tiab]) AND (cognit*[tiab] OR dementia[tiab])'),
 "huntington": ("Huntington disease","neurologic",'("Huntington Disease"[mh] OR huntington*[tiab])'),
 "tardive": ("Tardive dyskinesia","neurologic",'("Tardive Dyskinesia"[mh] OR "tardive dyskinesia"[tiab])'),
 "migraine": ("Migraine","neurologic",'("Migraine Disorders"[mh] OR migraine[tiab])'),
 "epilepsy": ("Epilepsy","neurologic",'("Epilepsy"[mh] OR epilep*[tiab] OR seizure*[tiab])'),
 "chronic_pain": ("Chronic pain","neurologic",'("Chronic Pain"[mh] OR "neuropathic pain"[tiab] OR "chronic pain"[tiab] OR analges*[tiab])'),
 "sleep": ("Sleep disorders / narcolepsy","neurologic",'("Narcolepsy"[mh] OR narcolep*[tiab] OR insomnia[tiab] OR "REM sleep"[tiab])'),
 "post_stroke": ("Post-stroke cognition","neurologic",'(stroke[tiab] AND (cognit*[tiab] OR aphasia[tiab] OR dementia[tiab]))'),
 "long_covid": ("Long-COVID brain fog","neurologic",'(("post-COVID"[tiab] OR "long COVID"[tiab] OR "post-acute sequelae"[tiab]) AND (cognit*[tiab] OR "brain fog"[tiab]))'),
 "chemo_brain": ("Chemotherapy-related cognitive impairment","neurologic",'(chemotherapy[tiab] AND (cognit*[tiab] OR "chemo brain"[tiab]))'),
 "gastroparesis": ("Gastroparesis","other",'(gastroparesis[tiab])'),
 # added during screen (see decisions_log)
 "schizophrenia_cog": ("Cognitive impairment in schizophrenia","psychiatric",'(schizophreni*[tiab] AND cognit*[tiab])'),
 "tbi": ("Traumatic brain injury cognition","neurologic",'("Brain Injuries, Traumatic"[mh] OR "traumatic brain injury"[tiab]) AND (cognit*[tiab] OR memory[tiab])'),
 "down_syndrome": ("Down syndrome cognition","neurologic",'("Down Syndrome"[mh]) AND (cognit*[tiab] OR dementia[tiab])'),
 "sjogren": ("Sjogren dry mouth (peripheral)","other",'("Sjogren\'s Syndrome"[mh] OR xerostomia[tiab])'),
 # negative controls
 "psoriasis": ("Psoriasis (neg. control)","control",'("Psoriasis"[mh] OR psoriasis[tiab])'),
 "hypothyroidism": ("Hypothyroidism (neg. control)","control",'("Hypothyroidism"[mh] OR hypothyroid*[tiab])'),
 "gout": ("Gout (neg. control)","control",'("Gout"[mh] OR gout[tiab])'),
}
HARM = {
 "dystonia": ("Dystonia","harm",'("Dystonia"[mh] OR dystoni*[tiab])'),
 "pd_tremor": ("Parkinson tremor / motor","harm",'("Parkinson Disease"[mh] OR parkinson*[tiab]) AND (tremor[tiab] OR motor[tiab] OR parkinsonism[tiab])'),
 "drug_parkinsonism": ("Antipsychotic-induced parkinsonism/EPS","harm",'(extrapyramidal[tiab] OR "drug-induced parkinsonism"[tiab] OR akathisia[tiab])'),
 "asthma": ("Asthma","harm",'("Asthma"[mh] OR asthma[tiab])'),
 "copd": ("COPD","harm",'("Pulmonary Disease, Chronic Obstructive"[mh] OR COPD[tiab])'),
 "bradycardia": ("Bradycardia / conduction","harm",'("Bradycardia"[mh] OR bradycardia[tiab] OR "heart block"[tiab] OR syncope[tiab])'),
 "peptic_ulcer": ("Peptic ulcer / GERD","harm",'("Peptic Ulcer"[mh] OR "peptic ulcer"[tiab] OR "gastroesophageal reflux"[tiab])'),
 "sialorrhea": ("Sialorrhea / hypersecretion","harm",'(sialorrhea[tiab] OR hypersalivation[tiab] OR drooling[tiab])'),
 "hyperhidrosis": ("Hyperhidrosis","harm",'(hyperhidrosis[tiab])'),
 "myasthenia": ("Myasthenia gravis (cholinergic crisis)","harm",'("Myasthenia Gravis"[mh])'),
}
AGONISTS = '(xanomeline[tiab] OR KarXT[tiab] OR cobenfy[tiab] OR emraclidine[tiab] OR "NBI-1117568"[tiab] OR cevimeline[tiab] OR pilocarpine[tiab] OR bethanechol[tiab] OR "muscarinic agonist*"[tiab] OR "M1 positive allosteric"[tiab] OR "M4 positive allosteric"[tiab] OR "muscarinic receptor agonist*"[tiab])'
CHEI = '(donepezil[tiab] OR rivastigmine[tiab] OR galantamine[tiab] OR physostigmine[tiab] OR "cholinesterase inhibitor*"[tiab])'
SCOP = '(scopolamine[tiab] OR "anticholinergic challenge"[tiab])'
QUERIES_BENEFIT = {
 "1a_human_agonist": lambda c: f'{c} AND {AGONISTS} AND humans[mh] NOT (animals[mh] NOT humans[mh])',
 "1b_human_chei": lambda c: f'{c} AND {CHEI} AND (clinical trial[pt] OR randomized[tiab] OR open-label[tiab] OR trial[tiab]) AND humans[mh]',
 "1c_scopolamine": lambda c: f'{c} AND {SCOP} AND humans[mh]',
 "2_anticholinergic_burden": lambda c: f'{c} AND ("anticholinergic burden"[tiab] OR "anticholinergic load"[tiab] OR "anticholinergic drug*"[tiab] OR "anticholinergic medication*"[tiab] OR "anticholinergic exposure"[tiab])',
 "3_genetics": lambda c: f'{c} AND (CHRM1[tiab] OR CHRM2[tiab] OR CHRM3[tiab] OR CHRM4[tiab] OR CHRM5[tiab] OR "muscarinic receptor gene"[tiab] OR ("muscarinic"[tiab] AND "mendelian randomization"[tiab]))',
 "4_postmortem_imaging": lambda c: f'{c} AND (muscarinic[tiab] OR "choline acetyltransferase"[tiab] OR "vesicular acetylcholine transporter"[tiab] OR "cholinergic denervation"[tiab] OR FEOBV[tiab] OR "basal forebrain"[tiab]) AND (postmortem[tiab] OR post-mortem[tiab] OR autopsy[tiab] OR PET[tiab] OR SPECT[tiab] OR autoradiograph*[tiab] OR "receptor binding"[tiab]) AND humans[mh]',
 "5_animal": lambda c: f'{c} AND (xanomeline[tiab] OR "M4 positive allosteric"[tiab] OR "M1 positive allosteric"[tiab] OR "M1 agonist"[tiab] OR "M4 agonist"[tiab] OR VU0467154[tiab] OR VU0152100[tiab] OR "muscarinic agonist*"[tiab] OR "M4 PAM"[tiab] OR "M1 PAM"[tiab]) AND (animals[mh] NOT humans[mh])',
 "6_clinical_obs": lambda c: f'{c} AND (xanomeline[tiab] OR KarXT[tiab] OR cobenfy[tiab] OR "xanomeline-trospium"[tiab] OR "xanomeline and trospium"[tiab])',
}
ANTICHOL = '(anticholinergic*[tiab] OR antimuscarinic*[tiab] OR trihexyphenidyl[tiab] OR benztropine[tiab] OR biperiden[tiab] OR tiotropium[tiab] OR ipratropium[tiab] OR glycopyrr*[tiab] OR atropine[tiab] OR scopolamine[tiab] OR botulinum[tiab])'
QUERIES_HARM = {
 "H1_anticholinergic_helps": lambda c: f'{c} AND {ANTICHOL} AND (clinical trial[pt] OR randomized[tiab] OR systematic review[pt] OR meta-analysis[pt]) AND humans[mh]',
 "H2_cholinergic_worsens": lambda c: f'{c} AND ({CHEI} OR {AGONISTS}) AND (adverse[tiab] OR induced[tiab] OR worsen*[tiab] OR exacerbat*[tiab] OR risk[tiab]) AND humans[mh]',
 "6_clinical_obs": QUERIES_BENEFIT["6_clinical_obs"],
}
