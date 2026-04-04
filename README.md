# Yale Research Match

A student-built research discovery tool for Yale undergraduates. Search labs across Yale College, FAS, YSM, and SEAS by topic, department, methods, and skill level. Built for the YCC Tech Developer Prize.

## What it does

Yale Research Match brings together lab data from the YURA Research Database and Yale departmental directories so undergrads can find real research openings without relying on insider knowledge or cold Googling.

- Topic-first search (type "aging" or "proteomics", not just "Chemistry")
- Filters by department, working style (wet lab / computational / hybrid), and experience level
- Lab cards with PI info, methods, prereqs, openings status, and student notes
- Outreach helper that generates a tailored email draft
- Public JSON API at `/api/labs` and `/api/labs_tagged.json`

## Quickstart

```bash
pip install -r requirements.txt
python scrape_yale_labs.py     # builds labs_raw.json
python tag_labs.py             # builds labs_tagged.json
python api_server.py           # serves API on port 5000
```

Open `index.html` in your browser, or point the frontend at the running API.

## Public API

```
GET /api/labs                          all labs
GET /api/labs?q=proteomics&dept=Chemistry   filtered
GET /api/labs/<id>                     single lab with notes
GET /api/labs_tagged.json              full static export
POST /api/labs/<id>/annotations        submit a student note
POST /api/labs/<id>/availability       faculty update openings
```

## For developers

`labs_tagged.json` is a public, versioned index of Yale labs with topics, methods, skills, openings status, and moderated student notes. Other YCC Tech projects are welcome to build on it. See the schema in `docs/schema.md`.

## Stack

- Frontend: plain HTML/CSS/JS, no build step required
- Backend: Python + Flask
- Deployment: Railway (Procfile included)

## License

MIT
