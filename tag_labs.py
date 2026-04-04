# tag_labs.py
# Reads labs_raw.json and writes labs_tagged.json with normalized fields,
# topic tokens, and inferred fit signals.
# Run: python tag_labs.py

import json
import re
from pathlib import Path
from datetime import datetime, timezone

RAW = Path("labs_raw.json")
OUT = Path("labs_tagged.json")

TOPIC_MAP = {
    "proteomics": ["proteom", "mass spec", "lc-ms", "metabolom", "proteostasis"],
    "cancer biology": ["cancer", "oncol", "tumor", "carcinoma", "leukemia"],
    "aging": ["aging", "senescen", "longev", "neurodegenerat", "proteostasis"],
    "neuroscience": ["neuro", "brain", "synap", "axon", "cortex", "hippocamp"],
    "machine learning": ["machine learn", "deep learn", "neural net", "pytorch", "tensorflow"],
    "chemical biology": ["chemical biol", "organic synth", "pepti", "small molecule", "drug discov"],
    "structural biology": ["cryo-em", "x-ray crystal", "protein struct", "nmr struct"],
    "immunology": ["immun", "antibod", "t cell", "b cell", "cytokine"],
    "ecology": ["ecol", "evolutionar", "conservation", "trophic", "biodiversity"],
    "climate chemistry": ["climate", "atmospheric", "environmental chem", "carbon"],
    "public health": ["epidemiol", "public health", "surveil", "vaccine", "infectious dis"],
    "developmental biology": ["developm", "stem cell", "cell fate", "morphogen", "embryo"],
    "genomics": ["genom", "rna-seq", "crispr", "single-cell", "transcriptom"],
    "bioinformatics": ["bioinform", "sequence align", "variant call", "genome assemb"],
    "biosensors": ["biosensor", "diagnostic", "microfluid", "point-of-care", "lateral flow"],
    "economics": ["econom", "labor market", "causal infer", "policy eval", "inequality"],
}

METHOD_KEYS = [
    "mass spectrometry", "cell culture", "western blot", "CRISPR", "single-cell RNA-seq",
    "cryo-EM", "X-ray crystallography", "microscopy", "flow cytometry", "IHC",
    "mouse models", "LC-MS", "Python", "R", "MATLAB", "PyTorch", "TensorFlow",
    "Stata", "regression", "field surveys", "GIS", "microfabrication", "NMR",
    "HPLC", "organic synthesis", "image analysis", "deep learning", "MRI analysis",
]

WET_KEYS = ["cell culture", "western blot", "pcr", "immunostain", "mouse model",
            "surgery", "dissect", "bench", "wet lab", "synthesis", "hplc", "nmr",
            "microscop", "lc-ms", "mass spec", "ihc"]
COMP_KEYS = ["python", "r ", "matlab", "pytorch", "tensorflow", "bioinform",
             "machine learn", "deep learn", "sequen", "computational", "stata",
             "regression", "statistical model", "data analys"]


def infer_style(text):
    t = text.lower()
    wet = sum(1 for k in WET_KEYS if k in t)
    comp = sum(1 for k in COMP_KEYS if k in t)
    if wet > comp and wet > 0:
        return "wet_lab"
    if comp > wet and comp > 0:
        return "computational"
    if wet > 0 and comp > 0:
        return "hybrid"
    return "unknown"


def infer_topics(text):
    t = text.lower()
    matched = [topic for topic, keys in TOPIC_MAP.items() if any(k in t for k in keys)]
    return matched[:4]


def make_id(lab, idx):
    source = lab.get("source", "unknown")
    dept = re.sub(r'[^a-z]', '_', lab.get("department", "nd").lower())[:8]
    return f"{source}_{dept}_{idx:04d}"


def tag(raw_lab, idx):
    blob = json.dumps(raw_lab).lower()
    topics = infer_topics(blob)
    style = infer_style(blob)
    existing_raw = raw_lab.get("raw_keywords", []) + raw_lab.get("raw_topics", [])
    return {
        "id": raw_lab.get("id") or make_id(raw_lab, idx),
        "name": raw_lab.get("name", ""),
        "pi_name": raw_lab.get("pi_name", ""),
        "pi_title": raw_lab.get("pi_title", ""),
        "department": raw_lab.get("department", ""),
        "school": raw_lab.get("school", ""),
        "lab_url": raw_lab.get("lab_url", ""),
        "directory_url": raw_lab.get("directory_url", ""),
        "contact_email": raw_lab.get("yale_email", ""),
        "primary_topics": topics[:2],
        "secondary_topics": topics[2:],
        "methods": [m for m in METHOD_KEYS if m.lower() in blob][:6],
        "skills_preferred": raw_lab.get("raw_skills", [])[:3],
        "skills_optional": [],
        "working_style": style,
        "undergrad_friendly": "beginner_ok" if "undergrad" in blob or "beginner" in blob else "unknown",
        "openings_status": "actively_recruiting" if ("open" in blob and "undergrad" in blob) else "unknown",
        "openings_notes": raw_lab.get("undergrad_notes_raw", ""),
        "min_commitment_weeks": 10,
        "recommended_years": ["sophomore", "junior", "senior"],
        "campus_location": "",
        "tags": existing_raw[:5],
        "source_flags": {
            "yura_listed": raw_lab.get("source") == "yura",
            "ysm_listed": raw_lab.get("source") == "ysm_lab_index",
            "dept_listed": raw_lab.get("source") == "dept_listing",
        },
        "student_notes": [],
        "match_metadata": {
            "last_indexed": datetime.now(timezone.utc).isoformat(),
            "topic_tokens": topics,
            "skills_tokens": raw_lab.get("raw_skills", []),
        },
    }


def run():
    if not RAW.exists():
        print(f"{RAW} not found. Run scrape_yale_labs.py first.")
        return
    data = json.loads(RAW.read_text(encoding="utf-8"))
    raw_labs = data.get("labs", data) if isinstance(data, dict) else data
    tagged = [tag(l, i) for i, l in enumerate(raw_labs)]
    out = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "version": datetime.now(timezone.utc).strftime("%Y.%m.%d-1"),
        "sources": ["yura", "ysm_lab_index", "dept_listing"],
        "labs": tagged,
    }
    OUT.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Tagged {len(tagged)} labs -> {OUT}")


if __name__ == "__main__":
    run()
