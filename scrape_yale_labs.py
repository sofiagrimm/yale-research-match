import json
import re
from dataclasses import dataclass, asdict, field
from typing import List

import requests
from bs4 import BeautifulSoup


@dataclass
class LabRecord:
    id: str
    name: str
    pi: str
    dept: str
    url: str
    summary: str
    topics: List[str] = field(default_factory=list)
    methods: List[str] = field(default_factory=list)
    goals: List[str] = field(default_factory=list)
    mode: str = "hybrid"
    fit: int = 70
    contact: str = ""
    beginner: str = ""
    prereqs: str = ""


HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; YaleResearchMatch/0.1)"}
BASE_URLS = {
    "bme": "https://burd.yale.edu",
    "ysm": "https://medicine.yale.edu",
    "mcdb": "https://mcdb.yale.edu",
    "eeb": "https://eeb.yale.edu",
    "chem": "https://chemistry.yale.edu",
    "mbb": "https://mbb.yale.edu",
}


def fetch(url: str) -> str:
    resp = requests.get(url, headers=HEADERS, timeout=20)
    resp.raise_for_status()
    return resp.text


def clean(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def resolve_url(href: str, base: str) -> str:
    if not href:
        return ""
    if href.startswith("http"):
        return href
    return base.rstrip("/") + "/" + href.lstrip("/")


def parse_bme_labs() -> List[LabRecord]:
    url = "https://burd.yale.edu/labs"
    soup = BeautifulSoup(fetch(url), "html.parser")
    records = []
    for i, block in enumerate(soup.select(".views-row")):
        name_el = block.find(["h3", "h2", "a"])
        if not name_el:
            continue
        name = clean(name_el.get_text())
        link = resolve_url(name_el.get("href", ""), BASE_URLS["bme"])
        desc = clean((block.find("p") or block).get_text())
        records.append(LabRecord(id=f"bme-{i+1}", name=name, pi="", dept="Biomedical Engineering", url=link, summary=desc))
    return records


def parse_ysm_labs() -> List[LabRecord]:
    url = "https://medicine.yale.edu/about/a-to-z-index/atoz/lab-websites/"
    soup = BeautifulSoup(fetch(url), "html.parser")
    records = []
    for i, row in enumerate(soup.select("table tr")):
        cols = row.find_all("td")
        if not cols:
            continue
        name_el = cols[0].find("a") or cols[0]
        name = clean(name_el.get_text())
        if not name:
            continue
        link = resolve_url(name_el.get("href", ""), BASE_URLS["ysm"])
        records.append(LabRecord(id=f"ysm-{i+1}", name=name, pi="", dept="Yale School of Medicine", url=link, summary=name))
    return records


def parse_mcdb_labs() -> List[LabRecord]:
    url = "https://mcdb.yale.edu/undergraduate/undergraduate-research-opportunities"
    soup = BeautifulSoup(fetch(url), "html.parser")
    records = []
    for i, block in enumerate(soup.select(".views-row, .field-item, article")):
        name_el = block.find(["h3", "h2", "h4"])
        if not name_el:
            continue
        name = clean(name_el.get_text())
        link = resolve_url((block.find("a") or {}).get("href", ""), BASE_URLS["mcdb"])
        desc = clean((block.find("p") or block).get_text())
        records.append(LabRecord(id=f"mcdb-{i+1}", name=name, pi="", dept="Molecular, Cellular & Developmental Biology", url=link, summary=desc))
    return records


def parse_eeb_labs() -> List[LabRecord]:
    url = "https://eeb.yale.edu/academics/undergraduate-program/undergraduate-research-opportunities"
    soup = BeautifulSoup(fetch(url), "html.parser")
    records = []
    for i, block in enumerate(soup.select(".views-row, article, .faculty-item")):
        name_el = block.find(["h3", "h2", "h4"])
        if not name_el:
            continue
        name = clean(name_el.get_text())
        link = resolve_url((block.find("a") or {}).get("href", ""), BASE_URLS["eeb"])
        desc = clean((block.find("p") or block).get_text())
        records.append(LabRecord(id=f"eeb-{i+1}", name=name, pi="", dept="Ecology & Evolutionary Biology", url=link, summary=desc))
    return records


def parse_chem_labs() -> List[LabRecord]:
    url = "https://chemistry.yale.edu/research/research-groups"
    soup = BeautifulSoup(fetch(url), "html.parser")
    records = []
    for i, block in enumerate(soup.select(".views-row, .faculty-item, article")):
        name_el = block.find(["h3", "h2", "h4"])
        if not name_el:
            continue
        name = clean(name_el.get_text())
        link = resolve_url((block.find("a") or {}).get("href", ""), BASE_URLS["chem"])
        desc = clean((block.find("p") or block).get_text())
        records.append(LabRecord(id=f"chem-{i+1}", name=name, pi="", dept="Chemistry", url=link, summary=desc))
    return records


def parse_mbb_labs() -> List[LabRecord]:
    url = "https://mbb.yale.edu/research"
    soup = BeautifulSoup(fetch(url), "html.parser")
    records = []
    for i, block in enumerate(soup.select(".views-row, article, .faculty-item")):
        name_el = block.find(["h3", "h2", "h4"])
        if not name_el:
            continue
        name = clean(name_el.get_text())
        link = resolve_url((block.find("a") or {}).get("href", ""), BASE_URLS["mbb"])
        desc = clean((block.find("p") or block).get_text())
        records.append(LabRecord(id=f"mbb-{i+1}", name=name, pi="", dept="Molecular Biophysics & Biochemistry", url=link, summary=desc))
    return records


PARSERS = [
    ("BME", parse_bme_labs),
    ("YSM", parse_ysm_labs),
    ("MCDB", parse_mcdb_labs),
    ("EEB", parse_eeb_labs),
    ("Chemistry", parse_chem_labs),
    ("MB&B", parse_mbb_labs),
]


def main() -> None:
    all_labs = []
    for label, parser in PARSERS:
        try:
            print(f"Fetching {label}...")
            batch = parser()
            print(f"  -> {len(batch)} entries")
            all_labs.extend(batch)
        except Exception as e:
            print(f"  Warning: could not parse {label}: {e}")
    print(f"Total: {len(all_labs)} lab entries.")
    with open("labs_raw.json", "w", encoding="utf-8") as f:
        json.dump([asdict(l) for l in all_labs], f, indent=2, ensure_ascii=False)
    print("Wrote labs_raw.json")


if __name__ == "__main__":
    main()
