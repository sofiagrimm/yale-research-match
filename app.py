"""app.py — Flask server for Yale Research Match."""
import json
import os
from pathlib import Path
from flask import Flask, send_file, jsonify, abort

app = Flask(__name__, static_folder='.', static_url_path='')


@app.route('/')
def index():
    return send_file('index.html')


@app.route('/api/labs')
def api_labs():
    path = Path('labs_tagged.json')
    if not path.exists():
        abort(404)
    return app.response_class(
        response=path.read_text(encoding='utf-8'),
        mimetype='application/json'
    )


@app.route('/labs_tagged.json')
def labs_json():
    """Legacy direct-file route — kept for backwards compat."""
    return api_labs()


@app.route('/healthz')
def health():
    return jsonify({'status': 'ok'})


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
