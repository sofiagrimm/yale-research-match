"""
api_server.py - Flask API that exposes labs_tagged.json and handles
faculty availability updates and student annotations with basic moderation.

Run:
    pip install flask flask-cors
    python api_server.py

Endpoints:
    GET  /api/labs                     - all tagged labs (supports ?q=, ?dept=, ?mode=)
    GET  /api/labs/<id>                - single lab with annotations
    POST /api/labs/<id>/availability   - faculty update openings and contact
    POST /api/labs/<id>/annotations    - student note submission
    GET  /api/labs/<id>/annotations    - approved notes for a lab
    GET  /api/annotations/pending      - all notes pending moderation
    POST /api/annotations/<id>/approve
    POST /api/annotations/<id>/reject
"""

import json
import uuid
from pathlib import Path
from datetime import datetime

from flask import Flask, jsonify, request, abort
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

LABS_FILE = Path("labs_tagged.json")
ANNOTATIONS_FILE = Path("annotations.json")
AVAILABILITY_FILE = Path("availability.json")


def load_labs():
    if not LABS_FILE.exists():
        return []
    return json.loads(LABS_FILE.read_text(encoding="utf-8"))


def load_annotations():
    if not ANNOTATIONS_FILE.exists():
        return []
    return json.loads(ANNOTATIONS_FILE.read_text(encoding="utf-8"))


def save_annotations(data):
    ANNOTATIONS_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def load_availability():
    if not AVAILABILITY_FILE.exists():
        return {}
    return json.loads(AVAILABILITY_FILE.read_text(encoding="utf-8"))


def save_availability(data):
    AVAILABILITY_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def basic_moderation(text: str) -> bool:
    blocked = ["http://", "https://", "<script", "SELECT ", "DROP TABLE"]
    return not any(b.lower() in text.lower() for b in blocked)


@app.route("/api/labs", methods=["GET"])
def list_labs():
    labs = load_labs()
    availability = load_availability()
    q = request.args.get("q", "").lower()
    dept = request.args.get("dept", "").lower()
    mode = request.args.get("mode", "").lower()
    if q:
        labs = [l for l in labs if q in json.dumps(l).lower()]
    if dept:
        labs = [l for l in labs if dept in l.get("dept", "").lower()]
    if mode:
        labs = [l for l in labs if l.get("mode", "") == mode]
    for lab in labs:
        if lab["id"] in availability:
            lab["availability"] = availability[lab["id"]]
    return jsonify({"count": len(labs), "labs": labs})


@app.route("/api/labs/<lab_id>", methods=["GET"])
def get_lab(lab_id):
    labs = load_labs()
    lab = next((l for l in labs if l["id"] == lab_id), None)
    if not lab:
        abort(404, description="Lab not found")
    availability = load_availability()
    if lab_id in availability:
        lab["availability"] = availability[lab_id]
    lab["annotations"] = [a for a in load_annotations() if a["lab_id"] == lab_id and a["status"] == "approved"]
    return jsonify(lab)


@app.route("/api/labs/<lab_id>/availability", methods=["POST"])
def update_availability(lab_id):
    data = request.get_json(force=True)
    if not data:
        abort(400, description="JSON body required")
    allowed = {"open_spots", "contact_email", "note", "updated_by"}
    entry = {k: v for k, v in data.items() if k in allowed}
    entry["updated_at"] = datetime.utcnow().isoformat()
    availability = load_availability()
    availability[lab_id] = entry
    save_availability(availability)
    return jsonify({"status": "ok", "lab_id": lab_id, "availability": entry}), 201


@app.route("/api/labs/<lab_id>/annotations", methods=["GET"])
def get_annotations(lab_id):
    notes = [a for a in load_annotations() if a["lab_id"] == lab_id and a["status"] == "approved"]
    return jsonify({"count": len(notes), "annotations": notes})


@app.route("/api/labs/<lab_id>/annotations", methods=["POST"])
def submit_annotation(lab_id):
    data = request.get_json(force=True)
    if not data or not data.get("text", "").strip():
        abort(400, description="text field required")
    text = data["text"].strip()
    if len(text) > 600:
        abort(400, description="Note too long (max 600 chars)")
    if not basic_moderation(text):
        abort(400, description="Note rejected by content check")
    note = {
        "id": str(uuid.uuid4())[:8],
        "lab_id": lab_id,
        "text": text,
        "category": data.get("category", "general"),
        "submitted_at": datetime.utcnow().isoformat(),
        "status": "pending",
    }
    annotations = load_annotations()
    annotations.append(note)
    save_annotations(annotations)
    return jsonify({"status": "pending_review", "id": note["id"]}), 202


@app.route("/api/annotations/pending", methods=["GET"])
def pending_annotations():
    notes = [a for a in load_annotations() if a["status"] == "pending"]
    return jsonify({"count": len(notes), "annotations": notes})


@app.route("/api/annotations/<note_id>/approve", methods=["POST"])
def approve_annotation(note_id):
    annotations = load_annotations()
    for note in annotations:
        if note["id"] == note_id:
            note["status"] = "approved"
            note["moderated_at"] = datetime.utcnow().isoformat()
            save_annotations(annotations)
            return jsonify({"status": "approved", "id": note_id})
    abort(404, description="Note not found")


@app.route("/api/annotations/<note_id>/reject", methods=["POST"])
def reject_annotation(note_id):
    annotations = load_annotations()
    for note in annotations:
        if note["id"] == note_id:
            note["status"] = "rejected"
            note["moderated_at"] = datetime.utcnow().isoformat()
            save_annotations(annotations)
            return jsonify({"status": "rejected", "id": note_id})
    abort(404, description="Note not found")


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
