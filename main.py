import os, logging
from flask import Flask, request, jsonify, send_from_directory
from card_generator import generate_welcome_card

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.getenv("SESSION_SECRET", "default_secret")

@app.route('/health', methods=['GET'])
def health():
    logger.debug("Health check endpoint called")
    return jsonify({"status": "healthy", "message": "API is running"})

@app.route('/generate-card', methods=['POST'])
def generate_card():
    data = request.get_json()
    if not data or 'avatar_url' not in data:
        return jsonify({"error": "Avatar URL is required"}), 400

    logger.debug(f"Received request with avatar_url={data['avatar_url']}")
    try:
        output_path = generate_welcome_card(data['avatar_url'])
        if not output_path:
            return jsonify({"error": "Failed to generate welcome card"}), 500

        file_name = os.path.basename(output_path)
        file_url = f"{request.host_url}static/{file_name}"
        return jsonify({"image_url": file_url})

    except Exception as e:
        logger.error(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory("static", filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
