"""
api_server.py

Flask API for Yale Research Match.

Endpoints:
    GET  /api/labs                       all labs, supports ?q= ?dept= ?mode= ?friendly=
    GET  /api/labs/<id>                  single lab with approved annotations
    GET  /api/labs_tagged.json           full static export (public API)
    POST /api/labs/<id>/availability     faculty updates openings  [requires ADMIN_TOKEN]
    POST /api/labs/<id>/annotations      student submits note
    GET  /api/labs/<id>/annotations      approved notes for a lab
    GET  /api/annotations/pending        all pending notes (moderation queue)  [requires ADMIN_TOKEN]
    POST /api/annotations/<id>/approve   [requires ADMIN_TOKEN]
    POST /api/annotations/<id>/reject    [requires ADMIN_TOKEN]
    GET  /api/status                     health check
"""

import json
import os
import re
import uuid
from datetime import UTC, datetime
from functools import wraps
from pathlib import Path

from flask import Flask, abort, jsonify, request, send_file
from flask_cors import CORS

app = Flask(__name__, static_folder=".", static_url_path="")
CORS(app)

LABS_FILE = Path("labs_tagged.json")
ANNOTATIONS_FILE = Path("annotations.json")
AVAILABILITY_FILE = Path("availability.json")

# Admin token loaded from environment; falls back to a generated value if unset.
# Always set ADMIN_TOKEN in production.
ADMIN_TOKEN = os.environ.get("ADMIN_TOKEN", "")
if not ADMIN_TOKEN:
    import secrets
    ADMIN_TOKEN = secrets.token_hex(32)
    print(f"[warn] ADMIN_TOKEN not set in environment. Using ephemeral token: {ADMIN_TOKEN}")
    print("[warn] Set ADMIN_TOKEN in your .env file or Railway environment variables.")

MAX_ANNOTATION_LENGTH = 600
MAX_QUERY_LENGTH = 200


# ---------------------------------------------------------------------------
# ID helpers
# ---------------------------------------------------------------------------

def slugify(text: str) -> str:
    """Convert lab name to a stable URL-safe id slug."""
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text)   # remove punctuation except hyphens
    text = re.sub(r"[\s_]+", "-", text)     # spaces/underscores -> hyphens
    text = re.sub(r"-+", "-", text)          # collapse repeated hyphens
    return text.strip("-")


def ensure_id(lab: dict) -> dict:
    """Return the lab dict with a guaranteed 'id' field derived from its name."""
    if "id" not in lab:
        lab = dict(lab)  # shallow copy — don't mutate the cached object
        lab["id"] = slugify(lab.get("name", str(uuid.uuid4())[:8]))
    return lab


# ---------------------------------------------------------------------------
# Auth
# ---------------------------------------------------------------------------

def require_admin(f):
    """Decorator: reject requests that do not supply the correct Bearer token."""
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth = request.headers.get("Authorization", "")
        token = auth.removeprefix("Bearer ").strip()
        if not token or token != ADMIN_TOKEN:
            abort(403, description="Admin token required")
        return f(*args, **kwargs)
    return wrapper


# ---------------------------------------------------------------------------
# Data helpers
# ---------------------------------------------------------------------------

def load_labs():
    if not LABS_FILE.exists():
        return []
    data = json.loads(LABS_FILE.read_text(encoding="utf-8"))
    raw = data.get("labs", data) if isinstance(data, dict) else data
    return [ensure_id(lab) for lab in raw]


def load_json(path):
    if not path.exists():
        return [] if path == ANNOTATIONS_FILE else {}
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path, data):
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


# Naive injection / XSS guard — block common attack strings.
_BLOCKED = ["<script", "javascript:", "SELECT ", "DROP TABLE", "INSERT INTO", "--"]


def is_clean(text: str) -> bool:
    return not any(b.lower() in text.lower() for b in _BLOCKED)


# ---------------------------------------------------------------------------
# Error handlers
# ---------------------------------------------------------------------------

@app.errorhandler(400)
def bad_request(e):
    return jsonify({"error": "bad_request", "message": str(e.description)}), 400


@app.errorhandler(403)
def forbidden(e):
    return jsonify({"error": "forbidden", "message": str(e.description)}), 403


@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "not_found", "message": str(e.description)}), 404


@app.errorhandler(422)
def unprocessable(e):
    return jsonify({"error": "unprocessable", "message": str(e.description)}), 422


@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "internal_server_error", "message": "An unexpected error occurred."}), 500


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    return send_file("index.html")


@app.route("/api/status")
def status():
    labs = load_labs()
    return jsonify({
        "status": "ok",
        "labs_indexed": len(labs),
        "timestamp": datetime.now(UTC).isoformat(),
    })


@app.route("/api/labs", methods=["GET"])
def list_labs():
    labs = load_labs()
    availability = load_json(AVAILABILITY_FILE)

    q = request.args.get("q", "")[:MAX_QUERY_LENGTH].lower()
    dept = request.args.get("dept", "").lower()
    mode = request.args.get("mode", "").lower()
    friendly = request.args.get("friendly", "").lower()
    school = request.args.get("school", "").lower()
    status_filter = request.args.get("status", "").lower()

    if q:
        labs = [lab for lab in labs if q in json.dumps(lab).lower()]
    if dept:
        labs = [lab for lab in labs if dept in lab.get("department", "").lower()]
    if mode:
        labs = [lab for lab in labs if lab.get("working_style", "") == mode]
    if friendly:
        labs = [lab for lab in labs if lab.get("undergrad_friendly", "") == friendly]
    if school:
        labs = [lab for lab in labs if school in lab.get("school", "").lower()]
    if status_filter:
        labs = [lab for lab in labs if lab.get("openings_status", "") == status_filter]

    for lab in labs:
        lid = lab["id"]
        if lid in availability:
            lab["availability"] = availability[lid]

    return jsonify({"count": len(labs), "labs": labs})


@app.route("/api/labs_tagged.json")
def labs_tagged_export():
    if LABS_FILE.exists():
        return send_file(str(LABS_FILE), mimetype="application/json")
    return jsonify({"labs": []})


@app.route("/api/labs/<lab_id>", methods=["GET"])
def get_lab(lab_id):
    lab = next((lab for lab in load_labs() if lab["id"] == lab_id), None)
    if not lab:
        abort(404, description="Lab not found")
    av = load_json(AVAILABILITY_FILE)
    if lab_id in av:
        lab["availability"] = av[lab_id]
    lab["annotations"] = [
        a for a in load_json(ANNOTATIONS_FILE)
        if a["lab_id"] == lab_id and a["status"] == "approved"
    ]
    return jsonify(lab)


@app.route("/api/labs/<lab_id>/availability", methods=["POST"])
@require_admin
def update_availability(lab_id):
    """Faculty/admin updates lab openings status and notes."""
    data = request.get_json(force=True) or {}
    allowed = {"open_spots", "contact_email", "note", "updated_by", "openings_status"}
    valid_statuses = {"actively_recruiting", "summer_only", "not_recruiting", "unknown"}

    entry = {k: v for k, v in data.items() if k in allowed}
    if "openings_status" in entry and entry["openings_status"] not in valid_statuses:
        abort(422, description=f"openings_status must be one of: {', '.join(sorted(valid_statuses))}")
    if "note" in entry and not is_clean(str(entry["note"])):
        abort(400, description="Note rejected by content check")

    entry["updated_at"] = datetime.now(UTC).isoformat()
    av = load_json(AVAILABILITY_FILE)
    av[lab_id] = entry
    save_json(AVAILABILITY_FILE, av)
    return jsonify({"status": "ok", "lab_id": lab_id, "availability": entry}), 201


@app.route("/api/labs/<lab_id>/annotations", methods=["GET"])
def get_lab_annotations(lab_id):
    notes = [
        a for a in load_json(ANNOTATIONS_FILE)
        if a["lab_id"] == lab_id and a["status"] == "approved"
    ]
    return jsonify({"count": len(notes), "annotations": notes})


@app.route("/api/labs/<lab_id>/annotations", methods=["POST"])
def submit_annotation(lab_id):
    """Student submits a note about a lab. Goes into moderation queue."""
    data = request.get_json(force=True) or {}
    text = data.get("text", "").strip()

    if not text:
        abort(400, description="text field required")
    if len(text) > MAX_ANNOTATION_LENGTH:
        abort(400, description=f"Note too long (max {MAX_ANNOTATION_LENGTH} chars)")
    if not is_clean(text):
        abort(400, description="Note rejected by content check")

    valid_cats = {"outreach", "environment", "projects", "general"}
    category = data.get("category", "general")
    if category not in valid_cats:
        abort(422, description=f"category must be one of: {', '.join(sorted(valid_cats))}")

    note = {
        "id": str(uuid.uuid4())[:8],
        "lab_id": lab_id,
        "text": text,
        "category": category,
        "submitted_at": datetime.now(UTC).isoformat(),
        "status": "pending",
    }
    notes = load_json(ANNOTATIONS_FILE)
    notes.append(note)
    save_json(ANNOTATIONS_FILE, notes)
    return jsonify({"status": "pending_review", "id": note["id"]}), 202


@app.route("/api/annotations/pending")
@require_admin
def pending_annotations():
    """Moderation queue — returns all pending student notes."""
    notes = [a for a in load_json(ANNOTATIONS_FILE) if a["status"] == "pending"]
    return jsonify({"count": len(notes), "annotations": notes})


@app.route("/api/annotations/<note_id>/approve", methods=["POST"])
@require_admin
def approve_note(note_id):
    notes = load_json(ANNOTATIONS_FILE)
    for n in notes:
        if n["id"] == note_id:
            n["status"] = "approved"
            n["moderated_at"] = datetime.now(UTC).isoformat()
            save_json(ANNOTATIONS_FILE, notes)
            return jsonify({"status": "approved", "id": note_id})
    abort(404, description="Note not found")


@app.route("/api/annotations/<note_id>/reject", methods=["POST"])
@require_admin
def reject_note(note_id):
    notes = load_json(ANNOTATIONS_FILE)
    for n in notes:
        if n["id"] == note_id:
            n["status"] = "rejected"
            n["moderated_at"] = datetime.now(UTC).isoformat()
            save_json(ANNOTATIONS_FILE, notes)
            return jsonify({"status": "rejected", "id": note_id})
    abort(404, description="Note not found")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
