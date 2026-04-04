"""
tag_labs.py

Reads labs_raw.json and writes labs_tagged.json with enriched fields:
topics, methods, skills, working_style, undergrad_friendly, openings_status.

Usage:
  python scrape_yale_labs.py   # first
  python tag_labs.py
"""

import json
import re
from datetime import datetime, timezone
from pathlib import Path

IN_FILE = Path("labs_raw.json")
OUT_FILE = Path("labs_tagged.json")

TOPIC_MAP = {
    "proteomics": ["proteom", "protein", "mass spec", "lc-ms", "lc/ms"],
    "aging": ["aging", "ageing", "longevity", "senescen", "lifespan"],
    "cancer biology": ["cancer", "oncol", "tumor", "tumour", "leukemi", "lymphoma", "carcinoma"],
    "neuroscience": ["neuro", "brain", "synap", "axon", "cognit", "alzheimer", "neurodegenerat"],
    "immunology": ["immun", "t cell", "b cell", "antibody", "inflamm", "cytokine"],
    "genetics and genomics": ["genom", "genetic", "crispr", "sequenc", "snp", "epigenet"],
    "cell biology": ["cell biol", "organelle", "mitochond", "cytoskel", "membrane"],
    "structural biology": ["structural", "cryo-em", "x-ray crystal", "nmr", "protein struct"],
    "chemical biology": ["chemical biol", "small molecule", "drug discov", "medicinal chem"],
    "computational biology": ["computat", "bioinformat", "machine learn", "deep learn", "model"],
    "ecology": ["ecol", "evolution", "biodiversity", "ecosyst", "phylogenet"],
    "climate and environment": ["climate", "environment", "atmospher", "carbon", "sustainab"],
    "public health": ["public health", "epidemiol", "clinical trial", "biostatist"],
    "metabolism": ["metabol", "metabolom", "lipid", "glucose", "insulin"],
    "microbiology": ["microb", "bacteria", "virus", "pathogen", "infect"],
    "stem cell and development": ["stem cell", "differentiat", "embryo", "developm"],
    "imaging": ["microscop", "imaging", "fluorescen", "confocal", "mri"],
    "bioengineering": ["bioeng", "biomaterial", "tissue eng", "synthetic biol"],
    "physics and biophysics": ["biophys", "physics", "quantum", "optical", "single molecul"],
}

METHOD_MAP = {
    "mass spectrometry": ["mass spec", "lc-ms", "lc/ms", "maldi", "proteom"],
    "CRISPR": ["crispr", "cas9", "gene edit"],
    "cell culture": ["cell culture", "in vitro", "tissue culture"],
    "mouse models": ["mouse model", "in vivo", "animal model"],
    "single-cell RNA-seq": ["scrna", "single.cell rna", "single-cell seq"],
    "cryo-EM": ["cryo-em", "cryo em", "electron microscop"],
    "flow cytometry": ["flow cytom", "facs"],
    "IHC / imaging": ["immunohistochem", "ihc", "confocal", "fluorescence microscop"],
    "Western blot": ["western blot", "immunoblot"],
    "Python / R": ["python", " r ", "bioinformat", "rstudio"],
    "NMR": ["nmr", "nuclear magnetic"],
    "X-ray crystallography": ["x-ray crystal", "crystallograph"],
    "electrophysiology": ["electrophysiol", "patch clamp", "ephys"],
    "organic synthesis": ["organic synth", "total synth"],
    "clinical datasets": ["clinical data", "ehr", "electronic health", "patient data"],
}

SKILL_MAP = {
    "wet lab basics": ["cell culture", "pipett", "bench", "wet lab"],
    "Python": ["python"],
    "R": [" r ", "rstudio", "bioconductor"],
    "statistics": ["statistic", "biostatistic"],
    "organic chemistry": ["organic chem", "synthesis"],
    "animal handling": ["mouse", "animal", "in vivo"],
    "microscopy": ["microscop", "imaging"],
}


def match_keys(text, mapping):
    text_low = text.lower()
    return [k for k, patterns in mapping.items() if any(p in text_low for p in patterns)]


def infer_style(text):
    text_low = text.lower()
    comp = any(w in text_low for w in ["computational", "bioinformat", "python", "model", "machine learn"])
    wet = any(w in text_low for w in ["cell culture", "mouse", "bench", "wet lab", "in vivo", "organic synth"])
    if comp and wet:
        return "hybrid"
    if comp:
        return "computational"
    if wet:
        return "wet_lab"
    return "unknown"


def infer_friendly(text):
    text_low = text.lower()
    if any(w in text_low for w in ["undergrad", "first year", "beginner", "no experience", "welcome"]):
        return "beginner_ok"
    if any(w in text_low for w in ["experience required", "prior experience", "graduate"]):
        return "experience_preferred"
    return "unknown"


def tag_lab(raw):
    blob = " ".join([
        raw.get("name", ""),
        raw.get("raw_description", ""),
        " ".join(raw.get("raw_topics", [])),
        " ".join(raw.get("raw_keywords", [])),
        " ".join(raw.get("raw_skills", [])),
    ])
    topics = match_keys(blob, TOPIC_MAP)
    methods = match_keys(blob, METHOD_MAP)
    skills = match_keys(blob, SKILL_MAP)
    style = infer_style(blob)
    friendly = infer_friendly(raw.get("undergrad_notes_raw", "") + " " + blob)
    accepts = raw.get("accepts_undergrads")
    if accepts is True:
        openings = "unknown"
    elif accepts is False:
        openings = "not_recruiting"
    else:
        openings = "unknown"
    return {
        "id": raw["id"],
        "name": raw["name"],
        "pi_name": raw.get("pi_name", ""),
        "pi_title": raw.get("pi_title", ""),
        "department": raw.get("department", ""),
        "school": raw.get("school", ""),
        "lab_url": raw.get("lab_url", ""),
        "directory_url": raw.get("directory_url", ""),
        "contact_email": raw.get("yale_email", ""),
        "primary_topics": topics[:3],
        "secondary_topics": topics[3:],
        "methods": methods,
        "skills_preferred": skills[:2],
        "skills_optional": skills[2:],
        "working_style": style,
        "undergrad_friendly": friendly,
        "openings_status": openings,
        "openings_notes": raw.get("undergrad_notes_raw", ""),
        "student_notes": [],
        "source": raw.get("source", ""),
        "last_indexed": datetime.now(timezone.utc).isoformat(),
        "topic_tokens": list(set(re.findall(r"\b\w{4,}\b", blob.lower())))[:80],
    }


def run():
    if not IN_FILE.exists():
        print(f"{IN_FILE} not found. Run scrape_yale_labs.py first.")
        return
    raw_data = json.loads(IN_FILE.read_text(encoding="utf-8"))
    tagged = [tag_lab(lab) for lab in raw_data["labs"]]
    out = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "version": datetime.now(timezone.utc).strftime("%Y.%m.%d-1"),
        "total": len(tagged),
        "sources": ["yura", "ysm_lab_index", "dept_listing"],
        "labs": tagged,
    }
    OUT_FILE.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {len(tagged)} tagged labs to {OUT_FILE}")


if __name__ == "__main__":
    run()
