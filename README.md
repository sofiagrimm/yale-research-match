# Yale Research Match

A student-built research discovery tool for Yale undergraduates. Search labs by topic, methods, and experience level across Yale College, YSM, FAS, SEAS, and YSPH. Built for the YCC Tech Developer Prize.

**Live site:** deploy via Railway (Procfile included) or any Python host.

## What it does

- Topic-first lab search: type "proteomics", "aging", "machine learning" instead of guessing department names
- Filter by working style (wet lab, computational, hybrid, field), school, and undergrad-friendliness
- Lab cards with PI, methods, skills, openings status, and a tailored outreach draft
- Moderated student annotations per lab
- Faculty-maintained openings via POST /api/labs/<id>/availability
- Public JSON API at /api/labs_tagged.json for other Yale developers to build on

## Data sources

- YURA Research Database (yura.yale.edu/ylabs)
- Yale School of Medicine A-Z lab index
- Departmental pages: Chemistry, MB&B, MCDB, EEB, BME, Physics, Earth Sciences, Statistics, YSPH

## Run locally

```bash
pip install -r requirements.txt
python api_server.py
# open http://localhost:5000
```

## Refresh lab data

```bash
python scrape_yale_labs.py   # writes labs_raw.json
python tag_labs.py           # writes labs_tagged.json
```

## API

```
GET  /api/labs                         all labs, supports ?q= ?dept= ?mode= ?friendly=
GET  /api/labs/<id>                    single lab with approved annotations
GET  /api/labs_tagged.json             full static export (public API)
POST /api/labs/<id>/availability       faculty updates openings
POST /api/labs/<id>/annotations        student submits note
GET  /api/labs/<id>/annotations        approved notes for a lab
GET  /api/annotations/pending          moderation queue
POST /api/annotations/<id>/approve
POST /api/annotations/<id>/reject
GET  /api/status                       health check
```

## Schema overview (labs_tagged.json)

Each lab record includes:
- `id`, `name`, `pi_name`, `pi_title`, `department`, `school`, `lab_url`, `contact_email`
- `primary_topics`, `secondary_topics`, `tags`, `methods`
- `skills_preferred`, `skills_optional`
- `working_style`: wet_lab | computational | hybrid | field | unknown
- `undergrad_friendly`: beginner_ok | experience_preferred | upper_level_only | unknown
- `openings_status`: actively_recruiting | summer_only | not_recruiting | unknown
- `openings_notes`, `min_commitment_weeks`, `recommended_years`, `campus_location`
- `student_notes[]`: id, text, category, status (approved only surfaced in API)
- `source_flags`: yura_listed, ysm_listed, dept_listed
- `match_metadata`: topic_tokens, skills_tokens, last_indexed

## Adding departments

Open scrape_yale_labs.py and add an entry to the SOURCES list:

```python
{
    "source": "dept_listing",
    "school": "Faculty of Arts and Sciences",
    "url": "https://yourdept.yale.edu/research",
    "dept": "Your Department",
    "parser": "generic_faculty",
}
```

Run the two scripts and the new labs appear in the API.

## Deploy (Railway)

1. Push to GitHub
2. Connect repo to Railway
3. Railway uses Procfile: `web: python api_server.py`
4. Set PORT env var if needed (defaults to 5000)

## License

MIT. Use it, extend it, build on top of it.
