# Yale Research Match — Roadmap & Upgrade Plan

Yale Research Match should evolve from a searchable lab directory into a guided student decision tool with three layers: **Explore, Match, and Act**. The current product already supports topic search, filters, topic browsing, moderated notes, and outreach drafting — the highest-leverage improvements are now product architecture, richer metadata, and a more premium interface.

---

## Product direction

### Layer 1 — Explore
The homepage should begin with clear student-intent entry points rather than a generic dashboard:
- Find my first lab
- Find computational work
- Find beginner-friendly labs
- Browse by topic
- Explore by school or department

This helps first-years and non-STEM students who do not yet know Yale's departmental structure or which PIs exist.

### Layer 2 — Match
Add a short onboarding flow that asks:
- What topics are you excited about?
- Do you want wet lab, computational, field, or hybrid work?
- Are you looking for a first research experience or something advanced?
- How much time can you commit per week?
- Do you want publication potential, mentorship, flexibility, or skill-building?

Use answers to rank and surface 3–8 recommended lab matches.

### Layer 3 — Act
Each lab detail drawer should support action:
- Tailored outreach email draft
- "Before you email" checklist
- Suggested first paper or lab page to read
- Student notes and mentorship signals
- Next-step checklist: read one paper → review methods → email PI or postdoc → follow up

---

## New metadata fields

Extend `labs_tagged.json` with the following optional fields to make results genuinely useful for decision-making:

```json
{
  "weekly_commitment_hours": "5-8 | 8-12 | 12+ | unknown",
  "mentorship_structure": "pi_direct | postdoc_grad_student | team_based | unknown",
  "beginner_friendly_reason": "Short explanation of why a new student can succeed here",
  "time_to_independence": "fast | moderate | slow | unknown",
  "publication_potential": "high | medium | unclear",
  "hosted_yale_undergrads": true,
  "ideal_for": ["first_years", "premeds", "coders", "chemistry_students"],
  "application_process": "email_pi | lab_form | yura_only | unclear",
  "response_likelihood": "high | medium | unclear"
}
```

These are more decision-useful than department and methods alone because they help students judge fit, realistic entry points, and expected support.

---

## Curated research tracks

Add a track layer grouping labs into student-friendly journeys:

| Track | Description |
|-------|-------------|
| Neuroscience | Synaptic biology, imaging, circuits, neurodegeneration |
| Oncology & Cancer Biology | Tumor biology, immunotherapy, cancer genomics |
| Chemical Biology | Small molecules, drug discovery, synthesis |
| Machine Learning & Quant Bio | Computational methods, deep learning, data analysis |
| Public Health & Epidemiology | Infectious disease, global health, population science |
| Aging & Longevity | Proteostasis, senescence, neurodegeneration, lifespan |
| Ecology & Climate | Conservation, ecology, atmospheric chemistry |
| Structural Biology & Biophysics | Cryo-EM, NMR, protein structure |

Each track should include: description, common methods, recommended student background, starter labs, and a "what students usually do" explainer.

---

## UI redesign

### Visual direction
Aim for a premium academic-product aesthetic: more editorial and trustworthy than flashy, but still modern and interactive.

Design traits to aim for:
- Stronger type hierarchy and more whitespace
- Calmer, more intentional color usage
- Richer card layouts with metadata rows and intent labels
- Detail drawers with clear sections and action tools
- Deliberate motion only on transitions, hover, and panel opening

### Homepage structure
1. Hero with clear value proposition and search
2. Intent cards: first lab, computational, beginner-friendly, by topic
3. Track carousel / grid
4. Match quiz block
5. Featured labs or recently updated openings
6. Practical action section: outreach help, note sharing, how to get started

### Improved lab card fields
- Lab name and PI name
- Department and school
- Beginner-friendliness label with rationale
- Working style (wet / computational / hybrid / field)
- Estimated commitment
- Mentorship structure
- Recruiting status
- Top 2–3 methods
- One-line fit summary: e.g. "Good for first-years who want hands-on neuroscience work"

### Improved detail drawer sections
1. Overview
2. Why this lab may fit you
3. Methods and skills
4. Student experience notes
5. Outreach strategy
6. Practical next steps

---

## Data expansion priorities

### High-priority new departments to scrape

| Department / Center | URL |
|---------------------|-----|
| Immunobiology | https://medicine.yale.edu/immunobiology/research/ |
| Biomedical Informatics & Data Science | https://medicine.yale.edu/bids/ |
| Computer Science research groups | https://cpsc.yale.edu/research |
| Applied Physics | https://appliedphysics.yale.edu/research |
| Psychology / cognitive science labs | https://psychology.yale.edu/research |
| Pharmacology | https://medicine.yale.edu/pharmacology/research/ |
| Neuroscience (YSM) | https://medicine.yale.edu/neuroscience/research/ |
| Genetics | https://medicine.yale.edu/genetics/research/ |
| Sociology / policy / economics research centers | https://sociology.yale.edu/research |
| Environmental engineering / climate labs | https://seas.yale.edu/departments/chemical-environmental-engineering |

### Parser improvements
- Improve faculty directory parsing to extract PI names, titles, and lab URLs
- Parse research interest text from faculty profile pages
- Detect undergraduate opportunity phrases for `undergrad_friendly` signals
- Extract emails and lab page links when visible

---

## Ranking logic upgrades

Move beyond basic token matching. Add weighted scoring for:
- Topic similarity to student interests
- Undergrad friendliness signals
- Beginner fit (presence of hosted undergrads, explicit welcome language)
- Openings status
- Mentorship structure match
- Commitment level match
- Prior Yale undergrad hosting history

This allows queries like "best first lab for a first-year interested in cancer biology" to feel meaningfully smarter.

---

## Implementation order

1. Add new metadata fields to schema and surface them in the UI
2. Rebuild homepage around Explore / Match / Act layers
3. Add curated tracks and intent entry points
4. Improve lab detail drawer and outreach workflow
5. Expand scraper source list and lab count
6. Add ranking weights and onboarding quiz
7. Add saved lists / compare feature (later)

---

## GitHub issue breakdown

### Product
- [ ] Redesign information architecture around Explore / Match / Act
- [ ] Add onboarding quiz and ranking logic
- [ ] Add curated research tracks

### Data
- [ ] Expand Yale department source coverage
- [ ] Add student-oriented metadata fields to schema
- [ ] Improve tagging heuristics for track assignment and beginner fit

### UI
- [ ] Redesign homepage with intent entry points
- [ ] Improve lab cards with richer metadata
- [ ] Improve detail drawer with action sections
- [ ] Add premium motion and type hierarchy polish

---

## Success criteria

The upgraded product should let any Yale student answer these four questions quickly:

1. Where should I start if I've never done research?
2. Which labs fit my interests and working style?
3. Which labs are realistic for someone at my level?
4. What should I do next after finding a lab?

When the interface makes those four questions easy to answer, the product will feel much more useful and much more mature — and will stand out as serious campus infrastructure rather than a demo.
