"""
tag_labs.py
-----------
Converts labs_raw.json → labs_tagged.json by inferring structured metadata
fields from lab descriptions using keyword heuristics (no API calls required).

Output fields added / normalised per lab:
  working_style     : "wet" | "dry" | "mixed"
  undergrad_friendly: "yes" | "unlikely" | "unknown"
  openings_status   : "likely_open" | "selective" | "unknown"
  funding_level     : "high" | "medium" | "low" | "unknown"
  primary_topics    : list[str]  — 1-5 broad topic buckets
  tags              : list[str]  — kept / generated if missing
  skills            : list[str]  — kept / generated if missing

Usage:
  python tag_labs.py                         # labs_raw.json → labs_tagged.json
  python tag_labs.py --input my_raw.json --output my_tagged.json
"""

import json
import re
import argparse
from pathlib import Path

# ---------------------------------------------------------------------------
# Keyword tables
# ---------------------------------------------------------------------------

WET_KEYWORDS = [
    "mouse model", "cell culture", "flow cytometry", "pcr", "western blot",
    "immunofluorescence", "ihc", "elisa", "crispr", "cloning", "virus",
    "bacterial", "protein purification", "biochemistry", "cryo-em",
    "x-ray crystallography", "patch clamp", "electrophysiology",
    "confocal", "live-cell imaging", "tirf", "single-cell", "zebrafish",
    "drosophila", "organoid", "in vivo", "in vitro", "tissue", "animal model",
    "mouse genetics", "germ-free", "transgenic", "lentiviral", "retroviral",
    "mass spectrometry", "proteomics", "metabolomics", "nmr", "hplc",
    "organic synthesis", "total synthesis", "bench", "wet lab",
]

DRY_KEYWORDS = [
    "bioinformatics", "computational", "machine learning", "deep learning",
    "neural network", "python", "r statistical", "mathematical model",
    "simulation", "genome assembly", "phylogenomic", "genome sequencing",
    "whole-genome", "population genetics", "gwas", "rna-seq analysis",
    "atac-seq", "chip-seq", "single-cell rna-seq analysis", "image analysis",
    "algorithm", "software", "database", "statistics", "modeling",
    "remote sensing", "gis", "dry lab",
]

TOPIC_MAP = {
    "cancer": [
        "cancer", "tumor", "oncol", "melanoma", "glioma", "leukemia",
        "lymphoma", "myeloma", "carcinoma", "neoplasm", "metastasis",
        "oncogenesis", "checkpoint", "immunotherapy", "neoantigen",
    ],
    "neuroscience": [
        "neuron", "neural", "synapse", "cortex", "hippocamp", "cerebr",
        "brain", "spinal cord", "axon", "dendrit", "glia", "microglia",
        "astrocyte", "dopamin", "serotonin", "neurodegen", "alzheimer",
        "parkinson", "epilepsy", "stroke", "fmri", "eeg", "neuroimag",
        "psychiatr", "schizophreni", "bipolar", "autism", "adhd",
    ],
    "immunology": [
        "immun", "t cell", "b cell", "antibody", "antigen", "innate",
        "adaptive", "inflammat", "autoimmun", "vaccine", "pathogen",
        "virus", "bacterial", "infection", "toll-like", "cytokine",
        "interferon", "nlrp3", "macrophage", "dendritic", "nk cell",
    ],
    "aging_longevity": [
        "aging", "longevity", "lifespan", "healthspan", "senescen",
        "inflammaging", "caloric restriction", "mtor", "sirtu", "telomer",
        "age-related", "geroscience", "nlrp3 inflammasome",
    ],
    "structural_biology": [
        "cryo-em", "x-ray crystallography", "structural biology",
        "protein structure", "atomic resolution", "nmr spectroscopy",
        "single-particle", "crystal structure",
    ],
    "genomics_genetics": [
        "genomic", "genetic", "epigenom", "crispr", "gene expression",
        "transcription factor", "rna-seq", "atac-seq", "chip-seq",
        "whole-genome", "exome", "snp", "gwas", "single-cell rna",
        "chromatin", "histone", "methylation",
    ],
    "chemical_biology": [
        "chemical biology", "small molecule", "drug discovery", "organic synthesis",
        "natural product", "total synthesis", "catalysis", "proteomics",
        "mass spectrometry", "glyco", "microbiome chemical", "bioactive",
    ],
    "ecology_evolution": [
        "ecology", "evolution", "phylogen", "biodiversity", "population biology",
        "species", "habitat", "ecosystem", "food web", "climate change ecology",
        "biogeograph", "conservation", "field ecology",
    ],
    "computational_ml": [
        "machine learning", "deep learning", "neural network", "algorithm",
        "bioinformatics", "computational model", "mathematical model",
        "manifold learning", "graph neural", "transformer", "language model",
    ],
    "microbiology": [
        "microbiome", "gut bacteria", "microbial", "microorganism",
        "bacteriophage", "phage", "pathogen", "germ-free", "metagenom",
        "microbiota",
    ],
}

HIGH_FUNDING_SIGNALS = [
    "hhmi", "howard hughes", "r01", "u01", "p01", "dp1", "new innovator",
    "pioneer award", "prestigious", "highly funded", "multiple r01",
    "large grant", "nih director", "national institute",
]

UNDERGRAD_POSITIVE = [
    "undergraduate", "undergrad", "bachelor", "research experience for undergrad",
    "reu", "senior thesis", "first-year", "junior", "sophomore",
]
UNDERGRAD_NEGATIVE = [
    "phd only", "graduate student only", "postdoc only", "no undergrad",
    "not accepting undergrad", "graduate-level only",
]

OPEN_SIGNALS = [
    "actively recruit", "accepting student", "open position", "we welcome",
    "interested student", "contact us", "join the lab", "applications open",
    "hiring", "openings", "new students", "prospective student",
]
SELECTIVE_SIGNALS = [
    "highly competitive", "very selective", "limited position",
    "rarely accept", "not currently recruiting", "full at this time",
    "no current openings",
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _lower(text: str) -> str:
    return text.lower()


def infer_working_style(lab: dict) -> str:
    desc = _lower(lab.get("raw_description", "") + " " + " ".join(lab.get("skills", [])))
    wet_score = sum(1 for kw in WET_KEYWORDS if kw in desc)
    dry_score = sum(1 for kw in DRY_KEYWORDS if kw in desc)

    if wet_score == 0 and dry_score == 0:
        return lab.get("working_style", "mixed") or "mixed"
    if wet_score > 0 and dry_score == 0:
        return "wet"
    if dry_score > 0 and wet_score == 0:
        return "dry"
    # both present
    if wet_score >= dry_score * 2:
        return "wet"
    if dry_score >= wet_score * 2:
        return "dry"
    return "mixed"


def infer_undergrad_friendly(lab: dict) -> str:
    desc = _lower(
        lab.get("raw_description", "")
        + " "
        + lab.get("lab_url", "")
    )
    if any(kw in desc for kw in UNDERGRAD_NEGATIVE):
        return "unlikely"
    if any(kw in desc for kw in UNDERGRAD_POSITIVE):
        return "yes"
    # Fall back to existing value if present
    existing = lab.get("undergrad_friendly", "")
    if existing in ("yes", "unlikely", "unknown"):
        return existing
    return "unknown"


def infer_openings_status(lab: dict) -> str:
    desc = _lower(lab.get("raw_description", ""))
    if any(kw in desc for kw in SELECTIVE_SIGNALS):
        return "selective"
    if any(kw in desc for kw in OPEN_SIGNALS):
        return "likely_open"
    existing = lab.get("openings_status", "")
    if existing in ("likely_open", "selective", "unknown"):
        return existing
    return "unknown"


def infer_funding_level(lab: dict) -> str:
    desc = _lower(lab.get("raw_description", ""))
    if any(kw in desc for kw in HIGH_FUNDING_SIGNALS):
        return "high"
    existing = lab.get("funding_level", "")
    if existing in ("high", "medium", "low"):
        return existing
    # Rough heuristic: longer, richer descriptions tend to correlate with
    # well-funded labs that have had time to build a web presence.
    word_count = len(lab.get("raw_description", "").split())
    if word_count > 80:
        return "medium"
    return "low"


def infer_primary_topics(lab: dict) -> list:
    desc = _lower(lab.get("raw_description", "") + " " + " ".join(lab.get("tags", [])))
    matched = []
    for topic, keywords in TOPIC_MAP.items():
        if any(kw in desc for kw in keywords):
            matched.append(topic)
    # Limit to top 5; sort for determinism
    return sorted(matched)[:5] if matched else ["other"]


def infer_tags(lab: dict) -> list:
    """Return existing tags or generate a minimal set from the description."""
    if lab.get("tags"):
        return lab["tags"]
    desc = lab.get("raw_description", "")
    # Extract capitalised noun phrases as a rough proxy for tags
    words = re.findall(r'\b[A-Z][a-z]{2,}\b', desc)
    return list(dict.fromkeys(words))[:8]  # dedup, max 8


def infer_skills(lab: dict) -> list:
    """Return existing skills or extract tool/method names from description."""
    if lab.get("skills"):
        return lab["skills"]
    desc = lab.get("raw_description", "")
    candidates = []
    for kw in WET_KEYWORDS + DRY_KEYWORDS:
        if kw in desc.lower():
            candidates.append(kw.replace("-", " ").title())
    return list(dict.fromkeys(candidates))[:6]


# ---------------------------------------------------------------------------
# Main transform
# ---------------------------------------------------------------------------

def tag_lab(lab: dict) -> dict:
    out = dict(lab)  # shallow copy preserves all original fields

    out["working_style"] = infer_working_style(lab)
    out["undergrad_friendly"] = infer_undergrad_friendly(lab)
    out["openings_status"] = infer_openings_status(lab)
    out["funding_level"] = infer_funding_level(lab)
    out["primary_topics"] = infer_primary_topics(lab)
    out["tags"] = infer_tags(lab)
    out["skills"] = infer_skills(lab)
    out["metadata_estimated"] = True

    return out


def tag_all(input_path: Path, output_path: Path) -> None:
    with open(input_path, "r", encoding="utf-8") as f:
        raw: list = json.load(f)

    if not isinstance(raw, list):
        raise ValueError("Input JSON must be a list of lab objects.")

    tagged = [tag_lab(lab) for lab in raw]

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(tagged, f, indent=2, ensure_ascii=False)

    print(f"✓  Tagged {len(tagged)} labs → {output_path}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Tag Yale lab data for yale-research-match.")
    parser.add_argument(
        "--input", "-i",
        default="labs_raw.json",
        help="Path to raw labs JSON file (default: labs_raw.json)",
    )
    parser.add_argument(
        "--output", "-o",
        default="labs_tagged.json",
        help="Path to write tagged labs JSON (default: labs_tagged.json)",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)

    if not input_path.exists():
        print(f"⚠  Input file '{input_path}' not found.")
        print("   If you haven't generated raw lab data yet, run:  python gen_labs.py")
        raise SystemExit(1)

    tag_all(input_path, output_path)
