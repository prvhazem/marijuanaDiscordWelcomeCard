import os
import logging
from flask import Flask, request, jsonify, send_file
from card_generator import generate_welcome_card

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "default_secret")  # Fallback for secret key

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint to verify API is running."""
    logger.debug("Health check endpoint called")
    return jsonify({"status": "healthy", "message": "API is running"})

@app.route('/generate-card', methods=['POST'])
def generate_card():
    """Generate a welcome card and return the image file."""
    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid JSON payload"}), 400

    avatar_url = data.get('avatar_url')

    if not avatar_url:
        return jsonify({"error": "Avatar URL is required"}), 400

    logger.debug(f"Received request with avatar_url={avatar_url}")

    try:
        output_path = generate_welcome_card(avatar_url)
        if not output_path:
            return jsonify({"error": "Failed to generate welcome card"}), 500

        logger.info(f"Generated welcome card: {output_path}")
        return send_file(output_path, mimetype='image/png')

    except Exception as e:
        logger.error(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
