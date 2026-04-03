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
    "climate": "climate",
    "drug": "drug discovery",
    "therapeutic": "therapeutics",
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
}


def tag_record(rec: dict) -> dict:
    text = " ".join([rec.get("name", ""), rec.get("summary", "")]).lower()
    rec["topics"] = sorted({topic for kw, topic in KEYWORDS_TO_TOPIC.items() if kw in text})
    rec["methods"] = sorted({method for kw, method in KEYWORDS_TO_METHOD.items() if kw in text})
    rec["goals"] = []
    rec["mode"] = "hybrid"
    rec["fit"] = 70
    return rec


def main() -> None:
    path = Path("labs_raw.json")
    if not path.exists():
        raise SystemExit("Run scrape_yale_labs.py first.")
    data = json.loads(path.read_text(encoding="utf-8"))
    tagged = [tag_record(rec) for rec in data]
    out_path = Path("labs_tagged.json")
    out_path.write_text(json.dumps(tagged, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Tagged {len(tagged)} records -> {out_path}")


if __name__ == "__main__":
    main()
