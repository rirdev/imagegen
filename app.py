# app.py
from flask import Flask, request, jsonify, Response
import requests
from flask_cors import CORS

app = Flask(__name__)
# For development/testing you can allow all origins:
CORS(app, resources={r"/*": {"origins": "*"}})

UPSTREAM = "https://imgen.duck.mom"

@app.route("/generate", methods=["GET"])
def generate():
    prompt = request.args.get("prompt", "")
    if not prompt:
        return jsonify({"error": "No prompt given"}), 400

    api_url = f"{UPSTREAM}/prompt/{requests.utils.quote(prompt)}"
    r = requests.get(api_url, timeout=20)

    if r.status_code != 200:
        return jsonify({"error": "Upstream failed", "status": r.status_code, "body": r.text}), r.status_code

    return jsonify({"image_url": api_url})

@app.route("/proxy", methods=["GET"])
def proxy_image():
    prompt = request.args.get("prompt", "")
    if not prompt:
        return jsonify({"error": "No prompt given"}), 400

    api_url = f"{UPSTREAM}/prompt/{requests.utils.quote(prompt)}"
    r = requests.get(api_url, stream=True, timeout=30)

    if r.status_code != 200:
        return jsonify({"error": "Upstream failed", "status": r.status_code, "body": r.text}), r.status_code

    content_type = r.headers.get("Content-Type", "image/png")
    return Response(r.raw, content_type=content_type)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
