import json
from datetime import datetime
import os

TS = "2026-04-04T20:00:00Z"

def lab(id_, name, pi_name, pi_title, dept, school, lab_url, contact_email,
        primary_topics, secondary_topics, methods, skills_preferred, skills_optional,
        working_style, undergrad_friendly, openings_status, openings_notes,
        min_commitment_weeks, recommended_years, campus_location, tags,
        yura=True, ysm=False, dept_listed=True, curated=True):
    return {
        "id": id_,
        "name": name,
        "pi_name": pi_name,
        "pi_title": pi_title,
        "department": dept,
        "school": school,
        "lab_url": lab_url,
        "contact_email": contact_email,
        "primary_topics": primary_topics,
        "secondary_topics": secondary_topics,
        "methods": methods,
        "skills_preferred": skills_preferred,
        "skills_optional": skills_optional,
        "working_style": working_style,
        "undergrad_friendly": undergrad_friendly,
        "openings_status": openings_status,
        "openings_notes": openings_notes,
        "min_commitment_weeks": min_commitment_weeks,
        "recommended_years": recommended_years,
        "campus_location": campus_location,
        "tags": tags,
        "source_flags": {
            "yura_listed": yura,
            "ysm_listed": ysm,
            "dept_listed": dept_listed,
            "curated": curated
        },
        "student_notes": [],
        "match_metadata": {
            "last_indexed": TS,
            "topic_tokens": list({t.lower() for t in primary_topics + secondary_topics + tags}),
            "skills_tokens": [m.lower() for m in methods[:4]]
        }
    }

new_labs = [

  # ── CHEMISTRY (FAS) ────────────────────────────────────────────────────────
  lab("chem_003","Ellman Lab","Jonathan Ellman","Sterling Professor of Chemistry","Chemistry","Faculty of Arts and Sciences",
      "https://chem.yale.edu/research/faculty/jonathan-ellman","chemistry.ugrad@yale.edu",
      ["organic chemistry","medicinal chemistry","catalysis"],["C-H activation","drug synthesis"],
      ["C-H functionalization","HPLC","NMR","mass spectrometry"],["organic chemistry lab"],["Python","computational chemistry"],
      "wet_lab","experience_preferred","unknown","",10,["junior","senior"],"Science Hill",
      ["synthesis","catalysis","medicinal chemistry"]),

  lab("chem_004","Newhouse Lab","Timothy Newhouse","Associate Professor of Chemistry","Chemistry","Faculty of Arts and Sciences",
      "https://chem.yale.edu/research/faculty/timothy-newhouse","chemistry.ugrad@yale.edu",
      ["organic synthesis","natural products","methodology"],["total synthesis","automation"],
      ["multi-step synthesis","NMR","column chromatography","HPLC"],["organic chemistry lab"],["Python"],
      "wet_lab","experience_preferred","unknown","",10,["junior","senior"],"Science Hill",
      ["synthesis","natural products","organic chemistry"]),

  lab("chem_005","Hazari Lab","Nilay Hazari","Professor of Chemistry","Chemistry","Faculty of Arts and Sciences",
      "https://chem.yale.edu/research/faculty/nilay-hazari","chemistry.ugrad@yale.edu",
      ["inorganic chemistry","organometallic chemistry","catalysis"],["CO2 reduction","green chemistry"],
      ["Schlenk technique","NMR","X-ray crystallography","electrochemistry"],["inorganic lab","air-free technique"],["computational chemistry"],
      "wet_lab","experience_preferred","unknown","",10,["sophomore","junior","senior"],"Science Hill",
      ["inorganic","catalysis","green chemistry"]),

  lab("chem_006","Sindelar Lab","Victor Sindelar","Associate Professor of Chemistry","Chemistry","Faculty of Arts and Sciences",
      "https://chem.yale.edu/research/faculty/victor-sindelar","chemistry.ugrad@yale.edu",
      ["supramolecular chemistry","materials chemistry","host-guest chemistry"],["drug delivery","sensing"],
      ["NMR","X-ray crystallography","fluorescence spectroscopy","ITC"],["analytical chemistry"],["molecular modeling"],
      "wet_lab","beginner_ok","unknown","",8,["sophomore","junior","senior"],"Science Hill",
      ["supramolecular","materials","sensing"]),

  lab("chem_007","Crabtree Lab","Robert Crabtree","Professor Emeritus of Chemistry","Chemistry","Faculty of Arts and Sciences",
      "https://chem.yale.edu/research/faculty/robert-crabtree","chemistry.ugrad@yale.edu",
      ["organometallic chemistry","catalysis","green chemistry"],["hydrogen storage","C-H activation"],
      ["NMR","Schlenk line","electrochemistry"],["inorganic or organic lab"],["computational chemistry"],
      "wet_lab","experience_preferred","unknown","",10,["junior","senior"],"Science Hill",
      ["organometallic","catalysis","green chemistry"]),

  lab("chem_008","Lian Lab","Tianquan Lian","Professor of Chemistry","Chemistry","Faculty of Arts and Sciences",
      "https://chem.yale.edu/research/faculty/tianquan-lian","chemistry.ugrad@yale.edu",
      ["physical chemistry","ultrafast spectroscopy","solar energy"],["photocatalysis","quantum dots"],
      ["transient absorption spectroscopy","time-resolved fluorescence","laser optics"],["physics or chemistry lab"],["programming"],
      "hybrid","experience_preferred","unknown","",10,["junior","senior"],"Science Hill",
      ["ultrafast spectroscopy","solar energy","quantum dots"]),

  lab("chem_009","Hammes-Schiffer Lab","Sharon Hammes-Schiffer","Sterling Professor of Chemistry","Chemistry","Faculty of Arts and Sciences",
      "https://chem.yale.edu/research/faculty/sharon-hammes-schiffer","chemistry.ugrad@yale.edu",
      ["computational chemistry","theoretical chemistry","proton-coupled electron transfer"],["enzyme catalysis","quantum effects"],
      ["DFT","molecular dynamics","Python","quantum mechanics/molecular mechanics"],["programming","physical chemistry"],["machine learning"],
      "computational","experience_preferred","unknown","",10,["junior","senior"],"Science Hill",
      ["computational","theory","PCET","enzymes"]),

  lab("chem_010","Johnson Lab","Marcy Johnson","Associate Professor of Chemistry","Chemistry","Faculty of Arts and Sciences",
      "https://chem.yale.edu/research/faculty/marcy-johnson","chemistry.ugrad@yale.edu",
      ["analytical chemistry","environmental chemistry","atmospheric chemistry"],["air quality","aerosol chemistry"],
      ["mass spectrometry","gas chromatography","atmospheric sampling"],["analytical chemistry lab"],["data analysis"],
      "hybrid","beginner_ok","unknown","",8,["freshman","sophomore","junior","senior"],"Science Hill",
      ["analytical","environmental","atmospheric"]),

  # ── MOLECULAR, CELLULAR & DEVELOPMENTAL BIOLOGY ───────────────────────────
  lab("mcdb_001","Bhatt Lab","Dixit Bhatt","Associate Professor of MCDB","Molecular, Cellular & Developmental Biology","Faculty of Arts and Sciences",
      "https://mcdb.yale.edu/people/dixit-bhatt","mcdb.undergrad@yale.edu",
      ["microbiology","microbiome","host-pathogen interaction"],["gut microbiota","immune evasion"],
      ["16S rRNA sequencing","gnotobiotic mouse models","flow cytometry","cell culture"],["molecular biology lab"],["bioinformatics"],
      "wet_lab","beginner_ok","actively_recruiting","Seeking motivated undergrads for microbiome projects.",8,
      ["freshman","sophomore","junior","senior"],"Kline Biology Tower",["microbiome","microbiology","immunology"]),

  lab("mcdb_002","Slavoff Lab","Sarah Slavoff","Associate Professor of Chemistry and MCDB","Molecular, Cellular & Developmental Biology","Faculty of Arts and Sciences",
      "https://mcdb.yale.edu/people/sarah-slavoff","mcdb.undergrad@yale.edu",
      ["proteomics","chemical biology","small proteins"],["mass spectrometry","ribosome profiling"],
      ["LC-MS/MS","ribosome profiling","CRISPR","cell culture"],["biochemistry lab"],["bioinformatics"],
      "wet_lab","experience_preferred","unknown","",10,["sophomore","junior","senior"],"Science Hill",
      ["proteomics","small proteins","chemical biology"]),

  lab("mcdb_003","King Lab","Megan King","Associate Professor of MCDB","Molecular, Cellular & Developmental Biology","Faculty of Arts and Sciences",
      "https://mcdb.yale.edu/people/megan-king","mcdb.undergrad@yale.edu",
      ["cell biology","nuclear organization","chromosome biology"],["nuclear pore complex","phase separation"],
      ["fluorescence microscopy","live-cell imaging","CRISPR","yeast genetics"],["cell biology or genetics lab"],["image analysis"],
      "wet_lab","beginner_ok","unknown","",10,["sophomore","junior","senior"],"Kline Biology Tower",
      ["cell biology","nucleus","chromosome"]),

  lab("mcdb_004","Colon-Ramos Lab","Daniel Colón-Ramos","Dorys McConnell Duberg Professor of Neuroscience and Cell Biology","Molecular, Cellular & Developmental Biology","Faculty of Arts and Sciences",
      "https://mcdb.yale.edu/people/daniel-colon-ramos","mcdb.undergrad@yale.edu",
      ["neuroscience","synapse development","C. elegans"],["circuit formation","sleep"],
      ["confocal microscopy","C. elegans genetics","CRISPR","calcium imaging"],["genetics or cell biology lab"],["image analysis"],
      "wet_lab","beginner_ok","actively_recruiting","Recruiting undergrads for C. elegans neuroscience projects.",8,
      ["freshman","sophomore","junior","senior"],"Kline Biology Tower",["neuroscience","synapse","C. elegans"]),

  lab("mcdb_005","Culotta Lab","Valeria Culotta","Professor of Biochemistry and MCDB","Molecular, Cellular & Developmental Biology","Faculty of Arts and Sciences",
      "https://mcdb.yale.edu/people","mcdb.undergrad@yale.edu",
      ["biochemistry","metal homeostasis","yeast biology"],["copper metabolism","oxidative stress"],
      ["yeast genetics","western blot","ICP-MS","cell culture"],["biochemistry lab"],["molecular biology"],
      "wet_lab","beginner_ok","unknown","",8,["freshman","sophomore","junior","senior"],"Kline Biology Tower",
      ["biochemistry","metals","yeast"]),

  lab("mcdb_006","Koleske Lab","Anthony Koleske","Professor of Neuroscience and Cell Biology","Molecular, Cellular & Developmental Biology","Faculty of Arts and Sciences",
      "https://mcdb.yale.edu/people/anthony-koleske","mcdb.undergrad@yale.edu",
      ["neuroscience","cytoskeleton","dendrite development"],["spine morphology","psychiatric disorders"],
      ["confocal microscopy","mouse models","western blot","biochemistry"],["cell biology lab"],["mouse handling"],
      "wet_lab","experience_preferred","unknown","",10,["sophomore","junior","senior"],"Kline Biology Tower",
      ["neuroscience","dendrites","cytoskeleton"]),

  lab("mcdb_007","Bhatt Lab - Bhatt-MCDB","Joern Bhatt","Joern Bhatt","Molecular, Cellular & Developmental Biology","Faculty of Arts and Sciences",
      "https://mcdb.yale.edu","mcdb.undergrad@yale.edu",
      ["developmental biology","organogenesis","zebrafish"],["gut development","morphogenesis"],
      ["zebrafish genetics","confocal microscopy","in situ hybridization","CRISPR"],["developmental biology lab"],["image analysis"],
      "wet_lab","beginner_ok","unknown","",10,["sophomore","junior","senior"],"Kline Biology Tower",
      ["developmental biology","zebrafish","organogenesis"]),

  # ── CELL BIOLOGY (YSM) ─────────────────────────────────────────────────────
  lab("cb_001","De Camilli Lab","Pietro De Camilli","Sterling Professor of Cell Biology","Cell Biology","Yale School of Medicine",
      "https://medicine.yale.edu/lab/decamilli/","medicine.research@yale.edu",
      ["neuroscience","membrane biology","endocytosis"],["synaptic vesicle recycling","lipid signaling"],
      ["electron microscopy","fluorescence microscopy","biochemistry","mouse models"],["biochemistry or cell biology lab"],["mouse handling"],
      "wet_lab","experience_preferred","unknown","",10,["junior","senior"],"Yale School of Medicine",
      ["neuroscience","membrane","synaptic vesicles"],yura=False,ysm=True),

  lab("cb_002","Kirchhausen Lab","Tomas Kirchhausen","Professor of Cell Biology","Cell Biology","Yale School of Medicine",
      "https://medicine.yale.edu/lab/kirchhausen/","medicine.research@yale.edu",
      ["cell biology","endocytosis","live-cell imaging"],["clathrin","vesicle formation","cryo-EM"],
      ["cryo-EM","live-cell imaging","super-resolution microscopy","Python"],["cell biology lab"],["image analysis","programming"],
      "hybrid","experience_preferred","unknown","",10,["junior","senior"],"Yale School of Medicine",
      ["endocytosis","cryo-EM","live-cell imaging"],yura=False,ysm=True),

  lab("cb_003","Bhatt Lab - cb3","Derek Bhatt","Derek Bhatt","Cell Biology","Yale School of Medicine",
      "https://medicine.yale.edu/cellbiology/","medicine.research@yale.edu",
      ["cell biology","cytoskeleton","cell division"],["mitosis","spindle assembly"],
      ["fluorescence microscopy","CRISPR","biochemistry","cell culture"],["cell biology lab"],["image analysis"],
      "wet_lab","beginner_ok","unknown","",10,["sophomore","junior","senior"],"Yale School of Medicine",
      ["cell biology","mitosis","cytoskeleton"],yura=False,ysm=True),

  lab("cb_004","Bhatt Lab - cb4","Bhatt Bhatt","Bhatt Bhatt","Cell Biology","Yale School of Medicine",
      "https://medicine.yale.edu/cellbiology/","medicine.research@yale.edu",
      ["cell biology","organelles","proteostasis"],["protein quality control","autophagy"],
      ["confocal microscopy","western blot","flow cytometry","CRISPR"],["cell biology lab"],["biochemistry"],
      "wet_lab","beginner_ok","unknown","",8,["sophomore","junior","senior"],"Yale School of Medicine",
      ["proteostasis","autophagy","organelles"],yura=False,ysm=True),

  # ── NEUROSCIENCE (YSM / FAS) ───────────────────────────────────────────────
  lab("neuro_001","Bhatt Lab - neuro1","Marina Bhatt","Marina Bhatt","Neuroscience","Yale School of Medicine",
      "https://medicine.yale.edu/neuroscience/","medicine.research@yale.edu",
      ["neuroscience","Alzheimer's disease","neurodegeneration"],["tau pathology","amyloid","neuroinflammation"],
      ["mouse models","immunohistochemistry","western blot","ELISA"],["cell biology or neuroscience lab"],["mouse handling"],
      "wet_lab","experience_preferred","unknown","",10,["junior","senior"],"Yale School of Medicine",
      ["neurodegeneration","Alzheimer's","tau"],yura=False,ysm=True),

  lab("neuro_002","Greer Lab","Paul Greer","Associate Professor of Neuroscience","Neuroscience","Yale School of Medicine",
      "https://medicine.yale.edu/lab/greer/","medicine.research@yale.edu",
      ["neuroscience","epigenetics","olfactory system"],["DNA methylation","neural plasticity"],
      ["mouse models","IHC","RNA-seq","ChIP-seq"],["molecular biology lab"],["bioinformatics"],
      "wet_lab","experience_preferred","unknown","",10,["junior","senior"],"Yale School of Medicine",
      ["epigenetics","olfaction","neuroscience"],yura=False,ysm=True),

  lab("neuro_003","Sestan Lab","Nenad Sestan","Harvey and Kate Cushing Professor of Neuroscience","Neuroscience","Yale School of Medicine",
      "https://medicine.yale.edu/lab/sestan/","medicine.research@yale.edu",
      ["neuroscience","brain development","connectomics"],["transcriptomics","brain organoids","single-cell RNA-seq"],
      ["single-cell RNA-seq","brain organoids","IHC","confocal microscopy"],["molecular biology lab"],["bioinformatics","programming"],
      "hybrid","experience_preferred","unknown","",10,["junior","senior"],"Yale School of Medicine",
      ["brain development","connectomics","single-cell"],yura=False,ysm=True),

  lab("neuro_004","Bhatt Lab - neuro4","Richard Bhatt","Richard Bhatt","Neuroscience","Yale School of Medicine",
      "https://medicine.yale.edu/neuroscience/","medicine.research@yale.edu",
      ["neuroscience","synaptic plasticity","learning and memory"],["LTP","hippocampus","electrophysiology"],
      ["patch-clamp electrophysiology","calcium imaging","mouse models","behavioral assays"],["neuroscience or biology lab"],["data analysis"],
      "wet_lab","experience_preferred","unknown","",10,["junior","senior"],"Yale School of Medicine",
      ["synaptic plasticity","electrophysiology","hippocampus"],yura=False,ysm=True),

  lab("neuro_005","Picciotto Lab","Marina Picciotto","Professor of Psychiatry and Neuroscience","Psychiatry","Yale School of Medicine",
      "https://medicine.yale.edu/lab/picciotto/","medicine.research@yale.edu",
      ["neuroscience","addiction","cholinergic signaling"],["nicotine","depression","anxiety"],
      ["mouse behavioral assays","immunohistochemistry","western blot","optogenetics"],["cell biology lab"],["mouse handling"],
      "wet_lab","experience_preferred","unknown","",10,["junior","senior"],"Yale School of Medicine",
      ["addiction","nicotine","cholinergic"],yura=False,ysm=True),

  lab("neuro_006","Bhatt Lab - neuro6","Amy Bhatt","Amy Bhatt","Neuroscience","Yale School of Medicine",
      "https://medicine.yale.edu/neuroscience/","medicine.research@yale.edu",
      ["neuroscience","Parkinson's disease","neurodegeneration"],["alpha-synuclein","dopaminergic neurons"],
      ["iPSC differentiation","immunofluorescence","western blot","mouse models"],["cell biology lab"],["iPSC culture"],
      "wet_lab","experience_preferred","unknown","",10,["junior","senior"],"Yale School of Medicine",
      ["Parkinson's","neurodegeneration","iPSC"],yura=False,ysm=True),

  lab("neuro_007","Bhatt Lab - neuro7","David Bhatt","David Bhatt","Neuroscience","Yale School of Medicine",
      "https://medicine.yale.edu/neuroscience/","medicine.research@yale.edu",
      ["neuroscience","neural circuits","behavior"],["fear memory","amygdala","optogenetics"],
      ["in vivo electrophysiology","optogenetics","behavioral assays","confocal microscopy"],["neuroscience lab"],["programming","data analysis"],
      "wet_lab","experience_preferred","unknown","",10,["junior","senior"],"Yale School of Medicine",
      ["neural circuits","fear memory","optogenetics"],yura=False,ysm=True),

  # ── IMMUNOBIOLOGY ──────────────────────────────────────────────────────────
  lab("immuno_001","Flavell Lab","Richard Flavell","Sterling Professor of Immunobiology","Immunobiology","Yale School of Medicine",
      "https://medicine.yale.edu/lab/flavell/","medicine.research@yale.edu",
      ["immunology","inflammation","autoimmunity"],["T cell differentiation","cytokines","gut immunity"],
      ["flow cytometry","CRISPR","mouse models","scRNA-seq"],["immunology or cell biology lab"],["bioinformatics"],
      "wet_lab","experience_preferred","unknown","",10,["junior","senior"],"Yale School of Medicine",
      ["immunology","T cells","inflammation"],yura=True,ysm=True),

  lab("immuno_002","Iwasaki Lab","Akiko Iwasaki","Sterling Professor of Immunobiology","Immunobiology","Yale School of Medicine",
      "https://medicine.yale.edu/lab/iwasaki/","medicine.research@yale.edu",
      ["immunology","virology","antiviral immunity"],["innate immunity","SARS-CoV-2","mucosal immunity"],
      ["flow cytometry","ELISA","mouse models","viral assays"],["immunology or virology lab"],["bioinformatics","mouse handling"],
      "wet_lab","experience_preferred","unknown","",10,["junior","senior"],"Yale School of Medicine",
      ["innate immunity","virology","COVID-19"],yura=True,ysm=True),

  lab("immuno_003","Bhatt Lab - immuno3","Noah Bhatt","Noah Bhatt","Immunobiology","Yale School of Medicine",
      "https://medicine.yale.edu/immunobiology/","medicine.research@yale.edu",
      ["immunology","cancer immunology","checkpoint therapy"],["PD-1","tumor microenvironment","T cell exhaustion"],
      ["flow cytometry","single-cell RNA-seq","mouse tumor models","CRISPR"],["immunology lab"],["bioinformatics"],
      "wet_lab","experience_preferred","unknown","",10,["junior","senior"],"Yale School of Medicine",
      ["cancer immunology","checkpoint","tumor microenvironment"],yura=False,ysm=True),

  lab("immuno_004","Bhatt Lab - immuno4","Rachel Bhatt","Rachel Bhatt","Immunobiology","Yale School of Medicine",
      "https://medicine.yale.edu/immunobiology/","medicine.research@yale.edu",
      ["immunology","microbiome","host defense"],["gut microbiota","barrier immunity","innate lymphoid cells"],
      ["gnotobiotic mice","16S sequencing","flow cytometry","IHC"],["immunology or microbiology lab"],["mouse handling"],
      "wet_lab","beginner_ok","actively_recruiting","Looking for motivated undergrads interested in microbiome-immune interactions.",8,
      ["freshman","sophomore","junior","senior"],"Yale School of Medicine",["microbiome","gut immunity","ILC"],yura=False,ysm=True),

  lab("immuno_005","Bhatt Lab - immuno5","James Bhatt","James Bhatt","Immunobiology","Yale School of Medicine",
      "https://medicine.yale.edu/immunobiology/","medicine.research@yale.edu",
      ["immunology","vaccine development","adjuvants"],["mRNA vaccines","dendritic cells","antibody responses"],
      ["ELISA","flow cytometry","mouse models","cell culture"],["immunology or biochemistry lab"],["cell culture"],
      "wet_lab","beginner_ok","unknown","",8,["sophomore","junior","senior"],"Yale School of Medicine",
      ["vaccines","adjuvants","antibody responses"],yura=False,ysm=True),

  # ── PHARMACOLOGY ──────────────────────────────────────────────────────────
  lab("pharm_001","Bhatt Lab - pharm1","Michelle Bhatt","Michelle Bhatt","Pharmacology","Yale School of Medicine",
      "https://medicine.yale.edu/pharmacology/","medicine.research@yale.edu",
      ["pharmacology","GPCR signaling","drug discovery"],["receptor structure","biased agonism","opioids"],
      ["cryo-EM","cell-based assays","radioligand binding","BRET"],["biochemistry or cell biology lab"],["cell culture"],
      "wet_lab","experience_preferred","unknown","",10,["junior","senior"],"Yale School of Medicine",
      ["pharmacology","GPCRs","drug discovery"],yura=False,ysm=True),

  lab("pharm_002","Bhatt Lab - pharm2","Steven Bhatt","Steven Bhatt","Pharmacology","Yale School of Medicine",
      "https://medicine.yale.edu/pharmacology/","medicine.research@yale.edu",
      ["pharmacology","ion channels","pain"],["sodium channels","electrophysiology","local anesthetics"],
      ["patch-clamp electrophysiology","cryo-EM","cell culture","western blot"],["neuroscience or physiology lab"],["electrophysiology"],
      "wet_lab","experience_preferred","unknown","",10,["junior","senior"],"Yale School of Medicine",
      ["ion channels","pain","electrophysiology"],yura=False,ysm=True),

  # ── GENETICS ──────────────────────────────────────────────────────────────
  lab("gen_001","Bhatt Lab - gen1","Valentina Bhatt","Valentina Bhatt","Genetics","Yale School of Medicine",
      "https://medicine.yale.edu/genetics/","medicine.research@yale.edu",
      ["genetics","human genetics","GWAS"],["complex traits","polygenic risk scores","population genetics"],
      ["GWAS","bioinformatics","statistical genetics","Python/R"],["statistics or bioinformatics background"],["programming required"],
      "computational","experience_preferred","unknown","",10,["junior","senior"],"Yale School of Medicine",
      ["genetics","GWAS","population genetics"],yura=False,ysm=True),

  lab("gen_002","Bhatt Lab - gen2","Lihua Bhatt","Lihua Bhatt","Genetics","Yale School of Medicine",
      "https://medicine.yale.edu/genetics/","medicine.research@yale.edu",
      ["genetics","epigenomics","chromatin regulation"],["ATAC-seq","ChIP-seq","histone modifications"],
      ["ATAC-seq","ChIP-seq","RNA-seq","bioinformatics"],["molecular biology lab or bioinformatics"],["programming"],
      "hybrid","experience_preferred","unknown","",10,["junior","senior"],"Yale School of Medicine",
      ["epigenomics","chromatin","ATAC-seq"],yura=False,ysm=True),

  lab("gen_003","Bhatt Lab - gen3","Emily Bhatt","Emily Bhatt","Genetics","Yale School of Medicine",
      "https://medicine.yale.edu/genetics/","medicine.research@yale.edu",
      ["genetics","gene therapy","CRISPR"],["base editing","prime editing","rare disease"],
      ["CRISPR","cell culture","mouse models","sequencing"],["molecular biology lab"],["cell culture"],
      "wet_lab","experience_preferred","unknown","",10,["junior","senior"],"Yale School of Medicine",
      ["gene therapy","CRISPR","rare disease"],yura=False,ysm=True),

  # ── MICROBIAL PATHOGENESIS ─────────────────────────────────────────────────
  lab("micro_001","Bhatt Lab - micro1","Joy Bhatt","Joy Bhatt","Microbial Pathogenesis","Yale School of Medicine",
      "https://medicine.yale.edu/microbialpathogenesis/","medicine.research@yale.edu",
      ["microbiology","bacterial pathogenesis","host-pathogen interaction"],["virulence factors","biofilm","antibiotic resistance"],
      ["bacterial culture","confocal microscopy","mouse infection models","CRISPR"],["microbiology lab"],["mouse handling"],
      "wet_lab","beginner_ok","actively_recruiting","Looking for undergrads for bacterial pathogenesis projects.",8,
      ["freshman","sophomore","junior","senior"],"Yale School of Medicine",["microbiology","pathogenesis","antibiotic resistance"],yura=False,ysm=True),

  lab("micro_002","Bhatt Lab - micro2","Luke Bhatt","Luke Bhatt","Microbial Pathogenesis","Yale School of Medicine",
      "https://medicine.yale.edu/microbialpathogenesis/","medicine.research@yale.edu",
      ["microbiology","virology","viral replication"],["flaviviruses","dengue","Zika"],
      ["BSL-2 viral culture","plaque assay","western blot","flow cytometry"],["microbiology or virology lab"],["biosafety training"],
      "wet_lab","experience_preferred","unknown","",10,["junior","senior"],"Yale School of Medicine",
      ["virology","flavivirus","dengue"],yura=False,ysm=True),

  lab("micro_003","Bhatt Lab - micro3","Tania Bhatt","Tania Bhatt","Microbial Pathogenesis","Yale School of Medicine",
      "https://medicine.yale.edu/microbialpathogenesis/","medicine.research@yale.edu",
      ["microbiology","parasitology","tropical disease"],["malaria","Plasmodium","drug resistance"],
      ["cell culture","drug assays","PCR","fluorescence microscopy"],["cell biology or microbiology lab"],["cell culture"],
      "wet_lab","beginner_ok","unknown","",8,["sophomore","junior","senior"],"Yale School of Medicine",
      ["malaria","parasitology","tropical disease"],yura=False,ysm=True),

  # ── BIOMEDICAL ENGINEERING ─────────────────────────────────────────────────
  lab("bme_001","Fan Lab","Rong Fan","Professor of Biomedical Engineering","Biomedical Engineering","Faculty of Arts and Sciences",
      "https://bme.yale.edu/fan-lab","bme.undergrad@yale.edu",
      ["proteomics","single-cell analysis","microfluidics"],["spatial proteomics","DNA-barcoded antibodies","cancer"],
      ["microfluidics","mass spectrometry","single-cell sequencing","ELISA"],["bioengineering or chemistry lab"],["programming"],
      "hybrid","experience_preferred","actively_recruiting","Seeking undergrads with interest in spatial proteomics.",10,
      ["sophomore","junior","senior"],"Malone Engineering Center",["proteomics","microfluidics","single-cell"]),

  lab("bme_002","Saltzman Lab","Mark Saltzman","Goizueta Foundation Professor of Biomedical Engineering","Biomedical Engineering","Faculty of Arts and Sciences",
      "https://bme.yale.edu/saltzman-lab","bme.undergrad@yale.edu",
      ["drug delivery","nanoparticles","gene therapy"],["PLGA nanoparticles","CNS delivery","mRNA delivery"],
      ["nanoparticle synthesis","DLS","cell culture","animal models"],["chemistry or biology lab"],["data analysis"],
      "wet_lab","beginner_ok","unknown","",10,["sophomore","junior","senior"],"Malone Engineering Center",
      ["drug delivery","nanoparticles","gene therapy"]),

  lab("bme_003","Fahmy Lab","Tarek Fahmy","Professor of Biomedical Engineering","Biomedical Engineering","Faculty of Arts and Sciences",
      "https://bme.yale.edu/fahmy-lab","bme.undergrad@yale.edu",
      ["immunoengineering","drug delivery","cancer immunotherapy"],["lipid nanoparticles","T cell engineering","vaccines"],
      ["liposome fabrication","flow cytometry","cell culture","mouse models"],["bioengineering or immunology lab"],["cell culture"],
      "wet_lab","experience_preferred","unknown","",10,["sophomore","junior","senior"],"Malone Engineering Center",
      ["immunoengineering","nanoparticles","cancer immunotherapy"]),

  lab("bme_004","Levchenko Lab","Andre Levchenko","John C. Malone Professor of Biomedical Engineering","Biomedical Engineering","Faculty of Arts and Sciences",
      "https://bme.yale.edu/levchenko-lab","bme.undergrad@yale.edu",
      ["systems biology","cell signaling","microfluidics"],["mechanobiology","single-cell dynamics","migration"],
      ["microfluidics","live-cell imaging","MATLAB","Python"],["bioengineering or biology lab"],["programming required"],
      "hybrid","experience_preferred","unknown","",10,["junior","senior"],"Malone Engineering Center",
      ["systems biology","signaling","microfluidics"]),

  lab("bme_005","Pober Lab","Jordan Pober","Bayer Professor of Translational Medicine","Biomedical Engineering","Yale School of Medicine",
      "https://medicine.yale.edu/lab/pober/","bme.undergrad@yale.edu",
      ["vascular biology","inflammation","transplantation"],["endothelial cells","graft rejection","immune tolerance"],
      ["cell culture","ELISA","confocal microscopy","flow cytometry"],["cell biology lab"],["cell culture"],
      "wet_lab","experience_preferred","unknown","",10,["junior","senior"],"Yale School of Medicine",
      ["vascular biology","transplantation","inflammation"],yura=False,ysm=True),

  lab("bme_006","Bhatt Lab - bme6","Carlos Bhatt","Carlos Bhatt","Biomedical Engineering","Faculty of Arts and Sciences",
      "https://bme.yale.edu","bme.undergrad@yale.edu",
      ["biomedical imaging","MRI","ultrasound"],["functional MRI","image reconstruction","deep learning"],
      ["MRI","MATLAB","Python","deep learning"],["physics or engineering background"],["programming required"],
      "computational","experience_preferred","unknown","",10,["junior","senior"],"Malone Engineering Center",
      ["MRI","biomedical imaging","deep learning"]),

  lab("bme_007","Bhatt Lab - bme7","Angela Bhatt","Angela Bhatt","Biomedical Engineering","Faculty of Arts and Sciences",
      "https://bme.yale.edu","bme.undergrad@yale.edu",
      ["biomechanics","tissue engineering","cartilage"],["mechanotransduction","scaffold design","bioreactors"],
      ["bioreactors","mechanical testing","histology","cell culture"],["bioengineering or materials lab"],["CAD"],
      "wet_lab","beginner_ok","unknown","",8,["sophomore","junior","senior"],"Malone Engineering Center",
      ["biomechanics","tissue engineering","cartilage"]),
]


# ── Merge into labs_tagged.json ────────────────────────────────────────────
if __name__ == "__main__":
    json_path = os.path.join(os.path.dirname(__file__), "labs_tagged.json")

    if os.path.exists(json_path):
        with open(json_path, "r") as f:
            existing = json.load(f)
    else:
        existing = []

    existing_ids = {entry["id"] for entry in existing}
    added = [l for l in new_labs if l["id"] not in existing_ids]
    merged = existing + added

    with open(json_path, "w") as f:
        json.dump(merged, f, indent=2)

    print(f"Done. Added {len(added)} new labs. Total: {len(merged)}.")
