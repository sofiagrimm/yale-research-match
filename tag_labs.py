import json
from pathlib import Path

KEYWORDS_TO_TOPIC = {
    "cancer": "cancer",
    "aging": "aging",
    "neuro": "neuroscience",
    "alzheimer": "neurodegeneration",
    "protein": "protein biology",
    "proteomic": "proteomics",
    "mass spectrometry": "proteomics",
    "microbiome": "microbiome",
    "immuno": "immunology",
    "metaboli": "metabolism",
    "genome": "genomics",
    "epigenet": "epigenetics",
    "climate": "climate",
    "drug": "drug discovery",
    "therapeutic": "therapeutics",
    "stem cell": "stem cells",
    "develop": "developmental biology",
    "evolution": "evolutionary biology",
    "ecology": "ecology",
    "structural": "structural biology",
    "chemical biology": "chemical biology",
}

KEYWORDS_TO_METHOD = {
    "sequencing": "sequencing",
    "imaging": "imaging",
    "microscopy": "imaging",
    "mouse": "mouse models",
    "cell culture": "cell culture",
    "python": "data analysis",
    "computational": "data analysis",
    "machine learning": "machine learning",
    "mass spec": "mass spec",
    "western blot": "western blot",
    "synthesis": "organic synthesis",
    "sensor": "instrumentation",
    "cryo": "cryo-EM",
    "crystallography": "crystallography",
    "flow cytometry": "flow cytometry",
    "single cell": "single-cell",
    "omics": "omics",
    "crispr": "CRISPR",
}


def infer_mode(text: str) -> str:
    comps = ["computational", "bioinformatics", "python", "modeling", "simulation", "machine learning"]
    wets = ["cell culture", "western blot", "mouse", "bench", "protocol", "assay", "microscopy", "cryo"]
    c = sum(1 for k in comps if k in text)
    w = sum(1 for k in wets if k in text)
    if c > 0 and w == 0:
        return "comp"
    if w > 0 and c == 0:
        return "wet"
    return "hybrid"


def infer_goals(text: str) -> list:
    goals = []
    if any(k in text for k in ["beginner", "no experience", "welcome undergrad", "training"]):
        goals.append("beginner-friendly")
    if any(k in text for k in ["clinic", "translat", "patient", "disease", "therapeutic"]):
        goals.append("translational")
    if any(k in text for k in ["cell culture", "bench", "wet", "mouse", "western"]):
        goals.append("wet-lab")
    if any(k in text for k in ["computational", "python", "bioinformatics", "modeling"]):
        goals.append("computational")
    return goals


def tag_record(rec: dict) -> dict:
    text = " ".join([rec.get("name", ""), rec.get("summary", "")]).lower()
    rec["topics"] = sorted({topic for kw, topic in KEYWORDS_TO_TOPIC.items() if kw in text})
    rec["methods"] = sorted({method for kw, method in KEYWORDS_TO_METHOD.items() if kw in text})
    rec["goals"] = infer_goals(text)
    rec["mode"] = infer_mode(text)
    if not rec.get("fit"):
        rec["fit"] = 70
    return rec


def main() -> None:
    path = Path("labs_raw.json")
    if not path.exists():
        raise SystemExit("Run scrape_yale_labs.py first.")
    data = json.loads(path.read_text(encoding="utf-8"))
    tagged = [tag_record(rec) for rec in data]
    out = Path("labs_tagged.json")
    out.write_text(json.dumps(tagged, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Tagged {len(tagged)} records -> {out}")


if __name__ == "__main__":
    main()
