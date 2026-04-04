# tag_labs.py
# Reads labs_raw.json → writes labs_tagged.json
# Run: python tag_labs.py

import json
import re
from datetime import UTC, datetime
from pathlib import Path

RAW = Path("labs_raw.json")
OUT = Path("labs_tagged.json")

DEPARTMENT_ALIASES = {
    "bbs": "Biological & Biomedical Sciences",
    "mcb": "Molecular, Cellular & Developmental Biology",
    "eeb": "Ecology & Evolutionary Biology",
    "mb&b": "Molecular Biophysics & Biochemistry",
    "mb&amp;b": "Molecular Biophysics & Biochemistry",
    "neuroscience": "Neuroscience",
    "pharmacology": "Pharmacology",
    "genetics": "Genetics",
    "immunobiology": "Immunobiology",
    "pathology": "Pathology",
    "cell biology": "Cell Biology",
    "biomedical engineering": "Biomedical Engineering",
    "chemical engineering": "Chemical & Environmental Engineering",
    "computer science": "Computer Science",
    "statistics": "Statistics & Data Science",
    "chemistry": "Chemistry",
    "physics": "Physics",
    "applied physics": "Applied Physics",
    "math": "Mathematics",
    "mathematics": "Mathematics",
    "psychiatry": "Psychiatry",
    "internal medicine": "Internal Medicine",
    "surgery": "Surgery",
    "pediatrics": "Pediatrics",
    "ob/gyn": "Obstetrics, Gynecology & Reproductive Sciences",
    "epidemiology": "Epidemiology of Microbial Diseases",
    "public health": "Public Health",
    "environmental health": "Environmental Health Sciences",
    "biostatistics": "Biostatistics",
    "health policy": "Health Policy & Management",
    "anthropology": "Anthropology",
    "sociology": "Sociology",
    "psychology": "Psychology",
    "cognitive science": "Cognitive Science",
    "linguistics": "Linguistics",
}

SCHOOL_MAP = {
    "Biological & Biomedical Sciences": "Graduate School of Arts & Sciences",
    "Molecular, Cellular & Developmental Biology": "Graduate School of Arts & Sciences",
    "Ecology & Evolutionary Biology": "Graduate School of Arts & Sciences",
    "Molecular Biophysics & Biochemistry": "Graduate School of Arts & Sciences",
    "Neuroscience": "Graduate School of Arts & Sciences",
    "Pharmacology": "Yale School of Medicine",
    "Genetics": "Yale School of Medicine",
    "Immunobiology": "Yale School of Medicine",
    "Pathology": "Yale School of Medicine",
    "Cell Biology": "Yale School of Medicine",
    "Biomedical Engineering": "Yale School of Engineering & Applied Science",
    "Chemical & Environmental Engineering": "Yale School of Engineering & Applied Science",
    "Computer Science": "Yale School of Engineering & Applied Science",
    "Statistics & Data Science": "Yale School of Engineering & Applied Science",
    "Chemistry": "Yale Faculty of Arts & Sciences",
    "Physics": "Yale Faculty of Arts & Sciences",
    "Applied Physics": "Yale School of Engineering & Applied Science",
    "Mathematics": "Yale Faculty of Arts & Sciences",
    "Psychiatry": "Yale School of Medicine",
    "Internal Medicine": "Yale School of Medicine",
    "Surgery": "Yale School of Medicine",
    "Pediatrics": "Yale School of Medicine",
    "Obstetrics, Gynecology & Reproductive Sciences": "Yale School of Medicine",
    "Epidemiology of Microbial Diseases": "Yale School of Public Health",
    "Public Health": "Yale School of Public Health",
    "Environmental Health Sciences": "Yale School of Public Health",
    "Biostatistics": "Yale School of Public Health",
    "Health Policy & Management": "Yale School of Public Health",
    "Anthropology": "Yale Faculty of Arts & Sciences",
    "Sociology": "Yale Faculty of Arts & Sciences",
    "Psychology": "Yale Faculty of Arts & Sciences",
    "Cognitive Science": "Yale Faculty of Arts & Sciences",
    "Linguistics": "Yale Faculty of Arts & Sciences",
}

WORK_STYLE_KEYWORDS = {
    "wet": ["bench", "wet lab", "cell culture", "mouse model", "in vivo", "in vitro",
            "pcr", "western blot", "microscopy", "flow cytometry", "mass spec",
            "protein", "antibody", "biochemistry", "assay", "gel", "sequencing",
            "histology", "immunostaining", "organoid", "crispr", "cloning"],
    "dry": ["computational", "bioinformatics", "machine learning", "deep learning",
            "data analysis", "modeling", "simulation", "algorithm", "software",
            "python", "r programming", "statistics", "genomics pipeline",
            "image analysis", "natural language", "neural network"],
    "clinical": ["clinical", "patient", "trial", "cohort", "epidemiology",
                 "survey", "electronic health", "ehr", "chart review", "interview"],
}

FRIENDLY_KEYWORDS = [
    "undergraduate", "undergrad", "bachelor", "reu", "summer research",
    "mentoring undergrad", "welcome undergraduate",
]

TOPIC_KEYWORDS = {
    "cancer": ["cancer", "tumor", "oncology", "carcinoma", "malignancy", "metastasis"],
    "neuroscience": ["neuro", "brain", "neuron", "synapse", "cognition", "alzheimer",
                     "parkinson", "circuit", "cortex", "hippocampus"],
    "immunology": ["immune", "immunology", "inflammation", "t cell", "b cell",
                   "antibody", "cytokine", "innate", "adaptive", "vaccine"],
    "genetics": ["gene", "genome", "genomic", "epigenetic", "crispr", "mutation",
                 "variant", "snp", "rna", "transcription"],
    "structural_biology": ["structure", "cryo-em", "crystallography", "protein folding",
                            "alphafold", "nmr", "structural"],
    "metabolism": ["metabol", "lipid", "mitochondria", "diabetes", "obesity",
                   "insulin", "nutrient", "energy"],
    "microbiology": ["bacteria", "virus", "pathogen", "infection", "microbiome",
                     "antibiotic", "fungal", "parasit"],
    "computational": ["machine learning", "deep learning", "neural network", "algorithm",
                      "bioinformatics", "computational", "data science"],
    "development": ["development", "stem cell", "differentiation", "embryo", "organoid",
                    "morphogen", "regeneration"],
    "aging": ["aging", "longevity", "senescence", "lifespan", "age-related", "geroscience"],
    "cardiovascular": ["heart", "cardiac", "vascular", "blood pressure", "atherosclerosis"],
    "public_health": ["epidemiology", "population health", "disparities", "health equity",
                      "surveillance", "global health"],
}


def normalize_dept(raw: str) -> str:
    if not raw:
        return "Unknown"
    key = raw.strip().lower().rstrip(".")
    return DEPARTMENT_ALIASES.get(key, raw.strip().title())


def infer_school(dept: str) -> str:
    return SCHOOL_MAP.get(dept, "Yale University")


def score_style(text: str) -> str:
    text_l = text.lower()
    scores = {k: sum(1 for kw in kws if kw in text_l) for k, kws in WORK_STYLE_KEYWORDS.items()}
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "mixed"


def score_friendly(text: str) -> str:
    text_l = text.lower()
    return "yes" if any(kw in text_l for kw in FRIENDLY_KEYWORDS) else "unknown"


def extract_topics(text: str) -> list:
    text_l = text.lower()
    return [topic for topic, kws in TOPIC_KEYWORDS.items() if any(kw in text_l for kw in kws)]


def make_id(name: str, index: int) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")[:40]
    return f"{slug}-{index:03d}"


def tag(raw_lab: dict, index: int) -> dict:
    name = raw_lab.get("name", "").strip()
    dept_raw = raw_lab.get("department", raw_lab.get("dept", ""))
    dept = normalize_dept(dept_raw)
    school = raw_lab.get("school") or infer_school(dept)
    pi = raw_lab.get("pi", raw_lab.get("pi_name", "")).strip()
    blob = " ".join([
        name, dept, pi,
        raw_lab.get("raw_description", ""),
        " ".join(raw_lab.get("raw_keywords", [])),
    ])
    topics = extract_topics(blob)
    return {
        "id": raw_lab.get("id") or make_id(name, index),
        "name": name,
        "pi": pi,
        "department": dept,
        "school": school,
        "description": raw_lab.get("raw_description", "")[:500],
        "keywords": raw_lab.get("raw_keywords", [])[:10],
        "topics": topics,
        "working_style": raw_lab.get("working_style") or score_style(blob),
        "undergrad_friendly": raw_lab.get("undergrad_friendly") or score_friendly(blob),
        "contact_email": raw_lab.get("contact_email", ""),
        "lab_url": raw_lab.get("lab_url", ""),
        "openings_status": raw_lab.get("openings_status", "unknown"),
        "student_notes": [],
        "match_metadata": {
            "last_indexed": datetime.now(UTC).isoformat(),
            "topic_tokens": topics,
            "skills_tokens": raw_lab.get("raw_skills", []),
        },
    }


def main():
    data = json.loads(RAW.read_text(encoding="utf-8"))
    raw_labs = data.get("labs", data) if isinstance(data, dict) else data
    tagged = [tag(raw, i) for i, raw in enumerate(raw_labs)]
    out = {
        "generated_at": datetime.now(UTC).isoformat(),
        "version": datetime.now(UTC).strftime("%Y.%m.%d-1"),
        "sources": ["yura", "ysm_lab_index", "dept_listing"],
        "labs": tagged,
    }
    OUT.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Tagged {len(tagged)} labs → {OUT}")


if __name__ == "__main__":
    main()
