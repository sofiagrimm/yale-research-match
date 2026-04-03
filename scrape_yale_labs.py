import json
import re
from dataclasses import dataclass, asdict
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


HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; YaleResearchMatch/0.1)"}


def fetch(url: str) -> str:
    resp = requests.get(url, headers=HEADERS, timeout=20)
    resp.raise_for_status()
    return resp.text


def clean(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def parse_bme_labs() -> List[LabRecord]:
    """BME Undergraduate Research Day labs list."""
    url = "https://burd.yale.edu/labs"
    html = fetch(url)
    soup = BeautifulSoup(html, "html.parser")
    records: List[LabRecord] = []
    for i, block in enumerate(soup.select(".view-content .views-row, .views-row")):
        name_el = block.find(["h3", "h2"]) or block.find("a")
        if not name_el:
            continue
        name = clean(name_el.get_text())
        link = name_el.get("href") or ""
        if link and link.startswith("/"):
            link = "https://burd.yale.edu" + link
        desc_el = block.find("p") or block
        summary = clean(desc_el.get_text())
        records.append(LabRecord(id=f"bme-{i+1}", name=name, pi="", dept="Biomedical Engineering", url=link, summary=summary))
    return records


def parse_ysm_labs() -> List[LabRecord]:
    """Yale School of Medicine A-Z lab websites list."""
    url = "https://medicine.yale.edu/about/a-to-z-index/atoz/lab-websites/"
    html = fetch(url)
    soup = BeautifulSoup(html, "html.parser")
    records: List[LabRecord] = []
    for i, row in enumerate(soup.select("table tr")):
        cols = row.find_all("td")
        if not cols:
            continue
        name_el = cols[0].find("a") or cols[0]
        name = clean(name_el.get_text())
        if not name:
            continue
        link = name_el.get("href") or ""
        if link and link.startswith("/"):
            link = "https://medicine.yale.edu" + link
        summary = clean(cols[0].get_text())
        records.append(LabRecord(id=f"ysm-{i+1}", name=name, pi="", dept="Yale School of Medicine", url=link, summary=summary))
    return records


def main() -> None:
    all_labs: List[LabRecord] = []
    try:
        print("Fetching BME labs...")
        all_labs.extend(parse_bme_labs())
    except Exception as e:
        print("Warning: could not parse BME labs:", e)
    try:
        print("Fetching YSM labs...")
        all_labs.extend(parse_ysm_labs())
    except Exception as e:
        print("Warning: could not parse YSM labs:", e)
    print(f"Collected {len(all_labs)} lab entries.")
    out_path = "labs_raw.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump([asdict(l) for l in all_labs], f, indent=2, ensure_ascii=False)
    print("Wrote", out_path)


if __name__ == "__main__":
    main()
