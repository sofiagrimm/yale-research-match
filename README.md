# Yale Research Match

[![CI](https://github.com/sofiagrimm/yale-research-match/actions/workflows/ci.yml/badge.svg)](https://github.com/sofiagrimm/yale-research-match/actions/workflows/ci.yml)

A student-built research discovery tool for Yale undergraduates. Search labs by topic, methods, and experience level across Yale College, YSM, FAS, SEAS, and YSPH. Built for the YCC Tech Developer Prize.

**Live site:** deploy via Railway (Procfile included) or any Python host.

## What it does

- Topic-first lab search: type `proteomics`, `aging`, `machine learning` instead of guessing department names
- Filter by working style (wet lab, computational, hybrid, field), school, and undergrad-friendliness
- Lab cards with PI, methods, skills, openings status, and a tailored outreach draft
- Moderated student annotations per lab
- Faculty-maintained openings via `POST /api/labs/<id>/availability` (admin token required)
- Public JSON API at `/api/labs_tagged.json` for other Yale developers to build on

## Data sources

- YURA Research Database (yura.yale.edu/ylabs)
- Yale School of Medicine A-Z lab index
- Departmental pages: Chemistry, MB&B, MCDB, EEB, BME, Physics, Earth Sciences, Statistics, YSPH

## Run locally

```bash
git clone https://github.com/sofiagrimm/yale-research-match.git
cd yale-research-match
pip install -r requirements.txt
cp .env.example .env          # set ADMIN_TOKEN
python api_server.py
# visit http://localhost:5000
```

## Refresh lab data

```bash
python scrape_yale_labs.py    # writes labs_raw.json
python tag_labs.py            # writes labs_tagged.json
```

## API

Public endpoints (no auth required):

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/labs` | All labs. Supports `?q=` `?dept=` `?mode=` `?friendly=` `?school=` `?status=` |
| GET | `/api/labs/<id>` | Single lab with approved annotations |
| GET | `/api/labs_tagged.json` | Full static export (public API) |
| GET | `/api/labs/<id>/annotations` | Approved student notes for a lab |
| POST | `/api/labs/<id>/annotations` | Submit a student note (goes to moderation) |
| GET | `/api/status` | Health check |

Admin endpoints — require `Authorization: Bearer <ADMIN_TOKEN>` header:

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/labs/<id>/availability` | Faculty updates openings status and notes |
| GET | `/api/annotations/pending` | Moderation queue |
| POST | `/api/annotations/<id>/approve` | Approve a pending note |
| POST | `/api/annotations/<id>/reject` | Reject a pending note |

## Environment variables

See [`.env.example`](.env.example) for a full list. The only required variable in production is `ADMIN_TOKEN`.

```bash
ADMIN_TOKEN=<your-secret-token>   # protects moderation and availability endpoints
PORT=5000                          # set automatically by Railway
```

Generate a token: `python -c "import secrets; print(secrets.token_hex(32))"`

## Schema overview (labs_tagged.json)

Each lab record includes:
- `id`, `name`, `pi_name`, `pi_title`, `department`, `school`, `lab_url`, `contact_email`
- `primary_topics`, `secondary_topics`, `tags`, `methods`
- `skills_preferred`, `skills_optional`
- `working_style`: `wet_lab` | `computational` | `hybrid` | `field` | `unknown`
- `undergrad_friendly`: `beginner_ok` | `experience_preferred` | `upper_level_only` | `unknown`
- `openings_status`: `actively_recruiting` | `summer_only` | `not_recruiting` | `unknown`
- `openings_notes`, `min_commitment_weeks`, `recommended_years`, `campus_location`
- `student_notes[]`: id, text, category, status (approved only surfaced in API)
- `source_flags`: yura_listed, ysm_listed, dept_listed
- `match_metadata`: topic_tokens, skills_tokens, last_indexed

## Adding departments

Open `scrape_yale_labs.py` and add an entry to the `SOURCES` list:

```python
{
    "source": "dept_listing",
    "school": "Faculty of Arts and Sciences",
    "url": "https://yourdept.yale.edu/research",
    "dept": "Your Department",
    "parser": "generic_faculty",
}
```

Run both scripts and open a PR with the updated `labs_tagged.json`. See [CONTRIBUTING.md](CONTRIBUTING.md) for full instructions.

## Deploy (Railway)

1. Push to GitHub
2. Connect repo to Railway
3. Railway uses `Procfile`: `web: python api_server.py`
4. Set `ADMIN_TOKEN` in Railway environment variables
5. Set `PORT` if needed (Railway sets this automatically)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). All contributions welcome — new departments, tag improvements, UI fixes, and more.

## License

MIT. Use it, extend it, build on top of it.
