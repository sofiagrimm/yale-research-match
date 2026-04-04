# scrape_yale_labs.py
# Fetches lab listings from Yale directories and writes labs_raw.json.
# Departments covered: YSM A-Z, Chemistry, MB&B, MCDB, EEB, BME, YSPH.
# Run: python scrape_yale_labs.py

import json
import time
from datetime import datetime, timezone
from pathlib import Path

import requests
from bs4 import BeautifulSoup

OUT = Path("labs_raw.json")
HEADERS = {"User-Agent": "yale-research-match/2.0 (student project; contact: research-match@yale.edu)"}
DELAY = 1.2

SOURCES = [
    {
        "source": "ysm_lab_index",
        "school": "Yale School of Medicine",
        "url": "https://medicine.yale.edu/about/a-to-z-index/atoz/lab-websites/",
        "parser": "ysm_az",
    },
    {
        "source": "dept_listing",
        "school": "Faculty of Arts and Sciences",
        "url": "https://chem.yale.edu/research/faculty",
        "dept": "Chemistry",
        "parser": "generic_faculty",
    },
    {
        "source": "dept_listing",
        "school": "Faculty of Arts and Sciences",
        "url": "https://mbb.yale.edu/people/faculty",
        "dept": "Molecular Biophysics and Biochemistry",
        "parser": "generic_faculty",
    },
    {
        "source": "dept_listing",
        "school": "Faculty of Arts and Sciences",
        "url": "https://mcdb.yale.edu/undergraduate/undergraduate-research-opportunities",
        "dept": "Molecular, Cellular, and Developmental Biology",
        "parser": "mcdb_opps",
    },
    {
        "source": "dept_listing",
        "school": "Faculty of Arts and Sciences",
        "url": "https://eeb.yale.edu/academics/undergraduate-program/undergraduate-research-opportunities",
        "dept": "Ecology and Evolutionary Biology",
        "parser": "generic_faculty",
    },
    {
        "source": "dept_listing",
        "school": "Yale School of Engineering and Applied Science",
        "url": "https://seas.yale.edu/departments/biomedical-engineering/undergraduate-research",
        "dept": "Biomedical Engineering",
        "parser": "generic_faculty",
    },
    {
        "source": "dept_listing",
        "school": "Faculty of Arts and Sciences",
        "url": "https://physics.yale.edu/research",
        "dept": "Physics",
        "parser": "generic_faculty",
    },
    {
        "source": "dept_listing",
        "school": "Faculty of Arts and Sciences",
        "url": "https://geology.yale.edu/people/faculty",
        "dept": "Earth and Planetary Sciences",
        "parser": "generic_faculty",
    },
    {
        "source": "dept_listing",
        "school": "Yale School of Public Health",
        "url": "https://ysph.yale.edu/epidemiology-of-microbial-diseases/research/",
        "dept": "Epidemiology of Microbial Diseases",
        "parser": "generic_faculty",
    },
    {
        "source": "dept_listing",
        "school": "Faculty of Arts and Sciences",
        "url": "https://statistics.yale.edu/research",
        "dept": "Statistics and Data Science",
        "parser": "generic_faculty",
    },
    {
        "source": "yura",
        "school": "Yale College",
        "url": "https://www.yura.yale.edu/ylabs",
        "dept": None,
        "parser": "yura_ylabs",
    },
]


def fetch(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=12)
        r.raise_for_status()
        return BeautifulSoup(r.text, "html.parser")
    except Exception as e:
        print(f"  [warn] fetch failed {url}: {e}")
        return None


def parse_ysm_az(soup, src):
    labs = []
    for a in soup.select("a[href]"):
        text = a.get_text(strip=True)
        href = a["href"]
        if "lab" in text.lower() or "laboratory" in text.lower():
            labs.append({
                "id": f"ysm_{len(labs):04d}",
                "source": src["source"],
                "school": src["school"],
                "name": text,
                "lab_url": href if href.startswith("http") else "https://medicine.yale.edu" + href,
                "department": "Yale School of Medicine",
                "raw_topics": [],
                "raw_description": "",
                "raw_keywords": [],
                "last_seen": datetime.now(timezone.utc).isoformat(),
            })
    return labs


def parse_generic_faculty(soup, src):
    labs = []
    for el in soup.select("h2, h3, h4, .faculty-name, .person-name, .views-row"):
        name = el.get_text(strip=True)
        if len(name) < 4 or len(name) > 80:
            continue
        labs.append({
            "id": f"{src['source']}_{src.get('dept','')[:8].replace(' ','_').lower()}_{len(labs):04d}",
            "source": src["source"],
            "school": src["school"],
            "name": name + " Lab",
            "department": src.get("dept", ""),
            "lab_url": src["url"],
            "raw_topics": [],
            "raw_description": "",
            "raw_keywords": [],
            "last_seen": datetime.now(timezone.utc).isoformat(),
        })
    return labs


def parse_mcdb_opps(soup, src):
    labs = []
    for p in soup.select("p, li"):
        text = p.get_text(strip=True)
        if "lab" in text.lower() and len(text) > 20:
            labs.append({
                "id": f"mcdb_{len(labs):04d}",
                "source": src["source"],
                "school": src["school"],
                "name": text[:80],
                "department": src.get("dept", ""),
                "lab_url": src["url"],
                "raw_topics": [],
                "raw_description": text[:300],
                "raw_keywords": [],
                "last_seen": datetime.now(timezone.utc).isoformat(),
            })
    return labs


def parse_yura_ylabs(soup, src):
    labs = []
    for el in soup.select(".lab-title, h2, h3, .title"):
        name = el.get_text(strip=True)
        if len(name) < 4 or len(name) > 100:
            continue
        labs.append({
            "id": f"yura_{len(labs):04d}",
            "source": "yura",
            "school": "Yale College",
            "name": name,
            "department": "",
            "lab_url": "https://www.yura.yale.edu/ylabs",
            "raw_topics": [],
            "raw_description": "",
            "raw_keywords": [],
            "last_seen": datetime.now(timezone.utc).isoformat(),
        })
    return labs


PARSERS = {
    "ysm_az": parse_ysm_az,
    "generic_faculty": parse_generic_faculty,
    "mcdb_opps": parse_mcdb_opps,
    "yura_ylabs": parse_yura_ylabs,
}


def run():
    all_labs = []
    for src in SOURCES:
        print(f"Fetching {src['url']} ...")
        soup = fetch(src["url"])
        if not soup:
            continue
        fn = PARSERS.get(src["parser"])
        if fn:
            batch = fn(soup, src)
            print(f"  found {len(batch)} entries")
            all_labs.extend(batch)
        time.sleep(DELAY)

    seen = set()
    deduped = []
    for lab in all_labs:
        key = lab["id"]
        if key not in seen:
            seen.add(key)
            deduped.append(lab)

    out = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_descriptions": {
            "yura": "Records from the YURA Research Database.",
            "ysm_lab_index": "Records from Yale School of Medicine lab directories.",
            "dept_listing": "Records from Yale departmental research pages.",
        },
        "labs": deduped,
    }
    OUT.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Done. Wrote {len(deduped)} labs to {OUT}")


if __name__ == "__main__":
    run()
