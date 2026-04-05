# Yale Research Match — Lab Schema Reference

This document describes all fields in `labs_tagged.json`. Required fields are marked **bold**. Optional fields are marked with their roadmap issue.

---

## Required Fields

| Field | Type | Allowed Values |
|-------|------|----------------|
| **`name`** | string | Lab or PI name |
| **`department`** | string | Yale department name |
| **`working_style`** | string | `wet` \| `dry` \| `mixed` \| `field` \| `hybrid` |
| **`openings_status`** | string | `likely_open` \| `selective` \| `unknown` |
| **`undergrad_friendly`** | string | `yes` \| `unlikely` \| `unknown` |

---

## Optional Fields — Added in Roadmap

All new fields are optional. Labs without them should use `"unknown"` for string fields, `false` for booleans, and omit array fields.

| Field | Type | Allowed Values | Issue |
|-------|------|----------------|-------|
| `weekly_commitment_hours` | string | `5-8` \| `8-12` \| `12+` \| `unknown` | #5 |
| `mentorship_structure` | string | `pi_direct` \| `postdoc_grad_student` \| `team_based` \| `unknown` | #5 |
| `beginner_friendly_reason` | string | Free text, 1–2 sentences | #5 |
| `time_to_independence` | string | `fast` \| `moderate` \| `slow` \| `unknown` | #5 |
| `publication_potential` | string | `high` \| `medium` \| `unclear` | #5 |
| `hosted_yale_undergrads` | boolean | `true` \| `false` | #5 |
| `ideal_for` | array of strings | `first_years` \| `premeds` \| `coders` \| `chemistry_students` \| `bio_students` \| `physics_students` \| `advanced_students` \| `all` | #5 |
| `application_process` | string | `email_pi` \| `lab_form` \| `yura_only` \| `unclear` | #5 |
| `response_likelihood` | string | `high` \| `medium` \| `unclear` | #5 |
| `tracks` | array of strings | See track values below | #3 |
| `pi_name` | string | Full PI name | #4 |
| `pi_email` | string | PI email if publicly listed | #4 |
| `lab_url` | string | Lab homepage URL | #4 |
| `fit_summary` | string | One-line student fit blurb | #7 |

---

## Track Values

Used in the `tracks` array field.

| Value | Display Name |
|-------|--------------|
| `neuroscience` | Neuroscience |
| `oncology_cancer_biology` | Oncology & Cancer Biology |
| `chemical_biology` | Chemical Biology |
| `ml_quant_bio` | Machine Learning & Quant Bio |
| `public_health_epidemiology` | Public Health & Epidemiology |
| `aging_longevity` | Aging & Longevity |
| `ecology_climate` | Ecology & Climate |
| `structural_biology_biophysics` | Structural Biology & Biophysics |

---

## Example Lab Entry (Fully Populated)

```json
{
  "name": "Bhatt Lab",
  "pi_name": "Dileep Bhatt",
  "pi_email": "dileep.bhatt@yale.edu",
  "lab_url": "https://bhattlab.yale.edu",
  "department": "Neuroscience",
  "working_style": "wet",
  "openings_status": "likely_open",
  "undergrad_friendly": "yes",
  "weekly_commitment_hours": "8-12",
  "mentorship_structure": "postdoc_grad_student",
  "beginner_friendly_reason": "Structured onboarding with grad student mentors; first-years have contributed to imaging projects.",
  "time_to_independence": "moderate",
  "publication_potential": "medium",
  "hosted_yale_undergrads": true,
  "ideal_for": ["first_years", "bio_students"],
  "application_process": "email_pi",
  "response_likelihood": "high",
  "tracks": ["neuroscience"],
  "fit_summary": "Good for first-years who want hands-on neuroscience imaging with strong grad student mentorship.",
  "topics": ["synaptic plasticity", "in vivo imaging", "calcium imaging"],
  "methods": ["two-photon microscopy", "mouse surgery", "data analysis"]
}
```
