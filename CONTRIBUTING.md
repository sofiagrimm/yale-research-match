# Contributing to Yale Research Match

Thank you for helping build a better research discovery tool for Yale undergrads.

## Ways to contribute

- **Add a department** — open `scrape_yale_labs.py` and add an entry to `SOURCES` (template in the README). Run both scripts and open a PR with the updated `labs_tagged.json`.
- **Improve tag accuracy** — edit the `TOPIC_MAP` or `METHOD_KEYS` in `tag_labs.py` and re-run `python tag_labs.py`.
- **Fix a bug or UI issue** — open an issue first so we can discuss the approach, then submit a PR.
- **Suggest a feature** — open a GitHub Issue with the label `enhancement`.

## Development setup

```bash
git clone https://github.com/sofiagrimm/yale-research-match.git
cd yale-research-match
pip install -r requirements.txt
cp .env.example .env        # edit ADMIN_TOKEN
python api_server.py
# visit http://localhost:5000
```

## Pull request checklist

- [ ] `ruff check .` passes with no errors
- [ ] `labs_tagged.json` is updated if you changed scraper or tagger logic
- [ ] New endpoints include docstrings and are documented in the README API table
- [ ] No secrets or Yale NetIDs committed

## Code style

- Python: follow PEP 8; `ruff` is the linter (see `pyproject.toml`)
- JavaScript: vanilla ES2022 — no build step, no frameworks
- HTML/CSS: keep the existing design token system; don't hardcode colors or sizes

## Data ethics

All lab data is sourced from publicly available Yale websites. Do not add non-public contact information. Student annotations are moderated before display.
