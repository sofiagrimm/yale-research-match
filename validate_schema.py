import json
import sys

with open("labs_tagged.json") as f:
    data = json.load(f)

labs = data.get("labs", data) if isinstance(data, dict) else data

if not isinstance(labs, list):
    print("ERROR: labs_tagged.json must be a JSON array (or object with 'labs' key)")
    sys.exit(1)

# --- Required fields ---
REQUIRED = {"name", "department", "working_style", "openings_status", "undergrad_friendly"}

# --- Allowed values ---
VALID_STYLE       = {"wet", "dry", "mixed", "field", "hybrid"}
VALID_STATUS      = {"likely_open", "selective", "unknown"}
VALID_FRIENDLY    = {"yes", "unlikely", "unknown"}

# --- New optional fields and their allowed values ---
VALID_COMMITMENT  = {"5-8", "8-12", "12+", "unknown"}
VALID_MENTORSHIP  = {"pi_direct", "postdoc_grad_student", "team_based", "unknown"}
VALID_INDEPENDENCE = {"fast", "moderate", "slow", "unknown"}
VALID_PUBLICATION = {"high", "medium", "unclear"}
VALID_IDEAL_FOR   = {"first_years", "premeds", "coders", "chemistry_students",
                     "bio_students", "physics_students", "advanced_students", "all"}
VALID_APPLICATION = {"email_pi", "lab_form", "yura_only", "unclear"}
VALID_RESPONSE    = {"high", "medium", "unclear"}
VALID_TRACKS      = {"neuroscience", "oncology_cancer_biology", "chemical_biology",
                     "ml_quant_bio", "public_health_epidemiology", "aging_longevity",
                     "ecology_climate", "structural_biology_biophysics"}

errors = []
for i, lab in enumerate(labs):
    label = f"Lab {i} ({lab.get('name', '?')})"

    missing = REQUIRED - lab.keys()
    if missing:
        errors.append(f"{label}: missing required fields {sorted(missing)}")
        continue

    # Required field validation
    if lab["working_style"] not in VALID_STYLE:
        errors.append(f"{label}: working_style={lab['working_style']!r} not in {VALID_STYLE}")
    if lab["openings_status"] not in VALID_STATUS:
        errors.append(f"{label}: openings_status={lab['openings_status']!r} not in {VALID_STATUS}")
    if lab["undergrad_friendly"] not in VALID_FRIENDLY:
        errors.append(f"{label}: undergrad_friendly={lab['undergrad_friendly']!r} not in {VALID_FRIENDLY}")

    # Optional new field validation (only validate if present)
    if "weekly_commitment_hours" in lab and lab["weekly_commitment_hours"] not in VALID_COMMITMENT:
        errors.append(f"{label}: weekly_commitment_hours={lab['weekly_commitment_hours']!r} not in {VALID_COMMITMENT}")

    if "mentorship_structure" in lab and lab["mentorship_structure"] not in VALID_MENTORSHIP:
        errors.append(f"{label}: mentorship_structure={lab['mentorship_structure']!r} not in {VALID_MENTORSHIP}")

    if "time_to_independence" in lab and lab["time_to_independence"] not in VALID_INDEPENDENCE:
        errors.append(f"{label}: time_to_independence={lab['time_to_independence']!r} not in {VALID_INDEPENDENCE}")

    if "publication_potential" in lab and lab["publication_potential"] not in VALID_PUBLICATION:
        errors.append(f"{label}: publication_potential={lab['publication_potential']!r} not in {VALID_PUBLICATION}")

    if "ideal_for" in lab:
        if not isinstance(lab["ideal_for"], list):
            errors.append(f"{label}: ideal_for must be a list")
        else:
            invalid = set(lab["ideal_for"]) - VALID_IDEAL_FOR
            if invalid:
                errors.append(f"{label}: ideal_for contains invalid values: {invalid}")

    if "application_process" in lab and lab["application_process"] not in VALID_APPLICATION:
        errors.append(f"{label}: application_process={lab['application_process']!r} not in {VALID_APPLICATION}")

    if "response_likelihood" in lab and lab["response_likelihood"] not in VALID_RESPONSE:
        errors.append(f"{label}: response_likelihood={lab['response_likelihood']!r} not in {VALID_RESPONSE}")

    if "hosted_yale_undergrads" in lab and not isinstance(lab["hosted_yale_undergrads"], bool):
        errors.append(f"{label}: hosted_yale_undergrads must be a boolean")

    if "tracks" in lab:
        if not isinstance(lab["tracks"], list):
            errors.append(f"{label}: tracks must be a list")
        else:
            invalid_tracks = set(lab["tracks"]) - VALID_TRACKS
            if invalid_tracks:
                errors.append(f"{label}: tracks contains invalid values: {invalid_tracks}")

if errors:
    print(f"Schema validation FAILED ({len(errors)} error(s)):")
    for e in errors:
        print(" ", e)
    sys.exit(1)

print(f"OK: validated {len(labs)} labs - all schema checks passed.")
