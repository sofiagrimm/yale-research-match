# Yale Research Match

A student-built research discovery tool for Yale undergrads. It roughly follows the judging criteria on ycctech.org: community impact, usability and polish, openness and extensibility, and technical quality.

## What it does

- Topic-first lab search (no more guessing department names)
- Method and work-style filters, quick tracks, and live fit ranking
- Lab brief with prerequisites, beginner-fit notes, and a shortlist drawer
- Generates outreach drafts for each lab, copyable in one click
- API preview panel showing the JSON data model for future campus integrations
- Loads real lab data from `labs_tagged.json` if available; falls back to sample labs

## Run locally

```bash
python3 -m http.server 8000
# open http://localhost:8000/yale-research-match.html
```

## Data pipeline

```bash
pip install requests beautifulsoup4
python3 scrape_yale_labs.py   # -> labs_raw.json
python3 tag_labs.py           # -> labs_tagged.json
```

Place `labs_tagged.json` in the same folder as the HTML file and the app will load it automatically.

## Source pages (public Yale lab listings)

- BME Undergraduate Research Day labs: https://burd.yale.edu/labs
- Yale School of Medicine A–Z lab websites: https://medicine.yale.edu/about/a-to-z-index/atoz/lab-websites/

## Extension ideas

- Add more department pages to the scraper
- Add faculty-maintained availability and openings
- Add student annotations with moderation
- Expose `labs_tagged.json` as a public API endpoint
