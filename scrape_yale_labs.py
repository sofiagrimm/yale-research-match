"""
scrape_yale_labs.py

Fetches lab listings from Yale department pages and the YSM A-Z lab index,
then writes labs_raw.json for downstream tagging.

Sources:
  - Yale School of Medicine A-Z lab websites
  - Yale Chemistry department research groups
  - Yale MB&B research labs
  - Yale MCDB research labs
  - Yale EEB research labs
  - Yale BME research groups
  - Yale Pharmacology labs
  - Yale Immunobiology labs
  - Yale Neuroscience labs

Usage:
  python scrape_yale_labs.py
"""

import json
import re
import time
from datetime import datetime, timezone
from pathlib import Path

import requests
from bs4 import BeautifulSoup

OUTFILE = Path("labs_raw.json")
HEADERS = {"User-Agent": "YaleResearchMatch/1.0 (student project; yale.edu)"}
DELAY = 1.2  # seconds between requests


def fetch(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        r.raise_for_status()
        return r.text
    except Exception as e:
        print(f"  skip {url}: {e}")
        return ""


def slug(text):
    return re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")


# --- scraper: YSM A-Z lab websites ---
def scrape_ysm_labs():
    html = fetch("https://medicine.yale.edu/about/a-to-z-index/atoz/lab-websites/")
    if not html:
        return []
    soup = BeautifulSoup(html, "html.parser")
    labs = []
    for a in soup.select("a[href]"):
        text = a.get_text(strip=True)
        href = a["href"]
        if not text or len(text) < 4:
            continue
        if not re.search(r"lab|group|center|program", text, re.I):
            continue
        if not href.startswith("http"):
            href = "https://medicine.yale.edu" + href
        labs.append({
            "id": "ysm_" + slug(text)[:40],
            "source": "ysm_lab_index",
            "name": text,
            "pi_name": "",
            "department": "Yale School of Medicine",
            "school": "Yale School of Medicine",
            "lab_url": href,
            "raw_topics": [],
            "raw_description": "",
            "raw_keywords": [],
            "raw_skills": [],
            "accepts_undergrads": None,
            "last_seen": datetime.now(timezone.utc).isoformat(),
        })
    seen = set()
    deduped = []
    for lab in labs:
        if lab["id"] not in seen:
            seen.add(lab["id"])
            deduped.append(lab)
    print(f"  YSM: {len(deduped)} labs")
    return deduped


# --- scraper: generic Yale department page ---
def scrape_dept(dept_name, school, url, link_pattern=None):
    html = fetch(url)
    if not html:
        return []
    soup = BeautifulSoup(html, "html.parser")
    labs = []
    for a in soup.select("a[href]"):
        text = a.get_text(strip=True)
        href = a["href"]
        if not text or len(text) < 5:
            continue
        if link_pattern and not re.search(link_pattern, href):
            continue
        if not href.startswith("http"):
            base = "/".join(url.split("/")[:3])
            href = base + "/" + href.lstrip("/")
        labs.append({
            "id": slug(dept_name)[:12] + "_" + slug(text)[:36],
            "source": "dept_listing",
            "name": text,
            "pi_name": "",
            "department": dept_name,
            "school": school,
            "lab_url": href,
            "raw_topics": [],
            "raw_description": "",
            "raw_keywords": [],
            "raw_skills": [],
            "accepts_undergrads": None,
            "last_seen": datetime.now(timezone.utc).isoformat(),
        })
    print(f"  {dept_name}: {len(labs)} entries")
    return labs


DEPT_SOURCES = [
    {
        "dept": "Chemistry",
        "school": "Faculty of Arts and Sciences",
        "url": "https://chem.yale.edu/research/research-groups",
        "pattern": r"chem\.yale\.edu",
    },
    {
        "dept": "Molecular Biophysics and Biochemistry",
        "school": "Faculty of Arts and Sciences",
        "url": "https://mbb.yale.edu/research/labs",
        "pattern": r"mbb\.yale\.edu",
    },
    {
        "dept": "Molecular, Cellular and Developmental Biology",
        "school": "Faculty of Arts and Sciences",
        "url": "https://mcdb.yale.edu/research/labs-and-groups",
        "pattern": r"mcdb\.yale\.edu",
    },
    {
        "dept": "Ecology and Evolutionary Biology",
        "school": "Faculty of Arts and Sciences",
        "url": "https://eeb.yale.edu/research/research-labs",
        "pattern": r"eeb\.yale\.edu",
    },
    {
        "dept": "Biomedical Engineering",
        "school": "School of Engineering and Applied Science",
        "url": "https://bme.yale.edu/research",
        "pattern": r"bme\.yale\.edu",
    },
    {
        "dept": "Pharmacology",
        "school": "Yale School of Medicine",
        "url": "https://medicine.yale.edu/lab/",
        "pattern": r"medicine\.yale\.edu/lab",
    },
    {
        "dept": "Immunobiology",
        "school": "Yale School of Medicine",
        "url": "https://medicine.yale.edu/immunobiology/labs/",
        "pattern": r"medicine\.yale\.edu",
    },
    {
        "dept": "Neuroscience",
        "school": "Yale School of Medicine",
        "url": "https://medicine.yale.edu/neuroscience/labs/",
        "pattern": r"medicine\.yale\.edu",
    },
    {
        "dept": "Cell Biology",
        "school": "Yale School of Medicine",
        "url": "https://medicine.yale.edu/cellbio/research/labs/",
        "pattern": r"medicine\.yale\.edu",
    },
    {
        "dept": "Genetics",
        "school": "Yale School of Medicine",
        "url": "https://medicine.yale.edu/genetics/labs/",
        "pattern": r"medicine\.yale\.edu",
    },
    {
        "dept": "Pathology",
        "school": "Yale School of Medicine",
        "url": "https://medicine.yale.edu/pathology/labs/",
        "pattern": r"medicine\.yale\.edu",
    },
    {
        "dept": "Physics",
        "school": "Faculty of Arts and Sciences",
        "url": "https://physics.yale.edu/research/research-groups",
        "pattern": r"physics\.yale\.edu",
    },
    {
        "dept": "Computer Science",
        "school": "School of Engineering and Applied Science",
        "url": "https://cpsc.yale.edu/research/research-groups",
        "pattern": r"cpsc\.yale\.edu",
    },
    {
        "dept": "Environmental Studies",
        "school": "Yale School of the Environment",
        "url": "https://environment.yale.edu/research/labs",
        "pattern": r"environment\.yale\.edu",
    },
]


def run():
    all_labs = []
    print("Scraping YSM lab index...")
    all_labs.extend(scrape_ysm_labs())
    time.sleep(DELAY)

    print("Scraping department pages...")
    for src in DEPT_SOURCES:
        labs = scrape_dept(src["dept"], src["school"], src["url"], src.get("pattern"))
        all_labs.extend(labs)
        time.sleep(DELAY)

    # deduplicate by lab_url
    seen_urls = set()
    deduped = []
    for lab in all_labs:
        key = lab["lab_url"].rstrip("/")
        if key not in seen_urls:
            seen_urls.add(key)
            deduped.append(lab)

    out = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total": len(deduped),
        "labs": deduped,
    }
    OUTFILE.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nWrote {len(deduped)} labs to {OUTFILE}")


if __name__ == "__main__":
    run()
