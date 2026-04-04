"""
api_server.py

Flask API for Yale Research Match.

Endpoints:
    GET  /api/labs                       all labs, supports ?q= ?dept= ?mode= ?friendly=
    GET  /api/labs/<id>                  single lab with approved annotations
    GET  /api/labs_tagged.json           full static export (public API)
    POST /api/labs/<id>/availability     faculty updates openings
    POST /api/labs/<id>/annotations      student submits note
    GET  /api/labs/<id>/annotations      approved notes for a lab
    GET  /api/annotations/pending        all pending notes (moderation queue)
    POST /api/annotations/<id>/approve
    POST /api/annotations/<id>/reject
    GET  /api/status                     health check
"""

import json
import uuid
from pathlib import Path
from datetime import datetime, timezone

from flask import Flask, jsonify, request, abort, send_file
from flask_cors import CORS

app = Flask(__name__, static_folder=".", static_url_path="")
CORS(app)

LABS_FILE = Path("labs_tagged.json")
ANNOTATIONS_FILE = Path("annotations.json")
AVAILABILITY_FILE = Path("availability.json")


def load_labs():
    if not LABS_FILE.exists():
        return []
    data = json.loads(LABS_FILE.read_text(encoding="utf-8"))
    return data.get("labs", data) if isinstance(data, dict) else data


def load_json(path):
    if not path.exists():
        return [] if path == ANNOTATIONS_FILE else {}
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path, data):
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def clean(text):
    blocked = ["<script", "javascript:", "SELECT ", "DROP TABLE", "INSERT INTO"]
    return not any(b.lower() in text.lower() for b in blocked)


@app.route("/")
def index():
    return send_file("index.html")


@app.route("/api/status")
def status():
    labs = load_labs()
    return jsonify({"status": "ok", "labs_indexed": len(labs), "timestamp": datetime.now(timezone.utc).isoformat()})


@app.route("/api/labs", methods=["GET"])
def list_labs():
    labs = load_labs()
    availability = load_json(AVAILABILITY_FILE)
    q = request.args.get("q", "").lower()
    dept = request.args.get("dept", "").lower()
    mode = request.args.get("mode", "").lower()
    friendly = request.args.get("friendly", "").lower()
    if q:
        labs = [l for l in labs if q in json.dumps(l).lower()]
    if dept:
        labs = [l for l in labs if dept in l.get("department", "").lower()]
    if mode:
        labs = [l for l in labs if l.get("working_style", "") == mode]
    if friendly:
        labs = [l for l in labs if l.get("undergrad_friendly", "") == friendly]
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
    lab = next((l for l in load_labs() if l["id"] == lab_id), None)
    if not lab:
        abort(404, description="Lab not found")
    av = load_json(AVAILABILITY_FILE)
    if lab_id in av:
        lab["availability"] = av[lab_id]
    lab["annotations"] = [a for a in load_json(ANNOTATIONS_FILE) if a["lab_id"] == lab_id and a["status"] == "approved"]
    return jsonify(lab)


@app.route("/api/labs/<lab_id>/availability", methods=["POST"])
def update_availability(lab_id):
    data = request.get_json(force=True) or {}
    allowed = {"open_spots", "contact_email", "note", "updated_by", "openings_status"}
    entry = {k: v for k, v in data.items() if k in allowed}
    entry["updated_at"] = datetime.now(timezone.utc).isoformat()
    av = load_json(AVAILABILITY_FILE)
    av[lab_id] = entry
    save_json(AVAILABILITY_FILE, av)
    return jsonify({"status": "ok", "lab_id": lab_id, "availability": entry}), 201


@app.route("/api/labs/<lab_id>/annotations", methods=["GET"])
def get_lab_annotations(lab_id):
    notes = [a for a in load_json(ANNOTATIONS_FILE) if a["lab_id"] == lab_id and a["status"] == "approved"]
    return jsonify({"count": len(notes), "annotations": notes})


@app.route("/api/labs/<lab_id>/annotations", methods=["POST"])
def submit_annotation(lab_id):
    data = request.get_json(force=True) or {}
    text = data.get("text", "").strip()
    if not text:
        abort(400, description="text field required")
    if len(text) > 600:
        abort(400, description="Note too long (max 600 chars)")
    if not clean(text):
        abort(400, description="Note rejected by content check")
    note = {
        "id": str(uuid.uuid4())[:8],
        "lab_id": lab_id,
        "text": text,
        "category": data.get("category", "general"),
        "submitted_at": datetime.now(timezone.utc).isoformat(),
        "status": "pending",
    }
    notes = load_json(ANNOTATIONS_FILE)
    notes.append(note)
    save_json(ANNOTATIONS_FILE, notes)
    return jsonify({"status": "pending_review", "id": note["id"]}), 202


@app.route("/api/annotations/pending")
def pending_annotations():
    notes = [a for a in load_json(ANNOTATIONS_FILE) if a["status"] == "pending"]
    return jsonify({"count": len(notes), "annotations": notes})


@app.route("/api/annotations/<note_id>/approve", methods=["POST"])
def approve_note(note_id):
    notes = load_json(ANNOTATIONS_FILE)
    for n in notes:
        if n["id"] == note_id:
            n["status"] = "approved"
            n["moderated_at"] = datetime.now(timezone.utc).isoformat()
            save_json(ANNOTATIONS_FILE, notes)
            return jsonify({"status": "approved", "id": note_id})
    abort(404, description="Note not found")


@app.route("/api/annotations/<note_id>/reject", methods=["POST"])
def reject_note(note_id):
    notes = load_json(ANNOTATIONS_FILE)
    for n in notes:
        if n["id"] == note_id:
            n["status"] = "rejected"
            n["moderated_at"] = datetime.now(timezone.utc).isoformat()
            save_json(ANNOTATIONS_FILE, notes)
            return jsonify({"status": "rejected", "id": note_id})
    abort(404, description="Note not found")


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
