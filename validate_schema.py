import json
import sys

with open("labs_tagged.json") as f:
    data = json.load(f)

labs = data.get("labs", data) if isinstance(data, dict) else data

if not isinstance(labs, list):
    print("ERROR: labs_tagged.json must be a JSON array (or object with 'labs' key)")
    sys.exit(1)

REQUIRED = {"name", "department", "working_style", "openings_status", "undergrad_friendly"}
VALID_STYLE    = {"wet", "dry", "mixed"}
VALID_STATUS   = {"likely_open", "selective", "unknown"}
VALID_FRIENDLY = {"yes", "unlikely", "unknown"}

errors = []
for i, lab in enumerate(labs):
    label = f"Lab {i} ({lab.get('name', '?')})"

    missing = REQUIRED - lab.keys()
    if missing:
        errors.append(f"{label}: missing required fields {sorted(missing)}")
        continue

    if lab["working_style"] not in VALID_STYLE:
        errors.append(f"{label}: working_style={lab['working_style']!r} not in {VALID_STYLE}")
    if lab["openings_status"] not in VALID_STATUS:
        errors.append(f"{label}: openings_status={lab['openings_status']!r} not in {VALID_STATUS}")
    if lab["undergrad_friendly"] not in VALID_FRIENDLY:
        errors.append(f"{label}: undergrad_friendly={lab['undergrad_friendly']!r} not in {VALID_FRIENDLY}")

if errors:
    print(f"Schema validation FAILED ({len(errors)} error(s)):")
    for e in errors:
        print(" ", e)
    sys.exit(1)

print(f"OK: validated {len(labs)} labs - all schema checks passed.")
