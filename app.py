from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route("/generate", methods=["GET"])
def generate():
    prompt = request.args.get("prompt", "")
    if not prompt:
        return jsonify({"error": "No prompt given"}), 400

    api_url = "https://imgen.duck.mom/prompt/" + requests.utils.quote(prompt)
    
    # Call the external API
    response = requests.get(api_url)

    if response.status_code != 200:
        return jsonify({"error": "Image API failed", "status": response.status_code}), 500

    # Pass image as a link (Render doesn’t serve binary easily)
    return jsonify({
        "image_url": api_url  # you can also base64 encode if needed
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
