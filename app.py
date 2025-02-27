import os
from flask import Flask, request, send_file
import logging
from card_generator import generate_welcome_card

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET")

@app.route('/health')
def health():
    """Health check endpoint to verify API is working"""
    logger.debug("Health check endpoint called")
    return {"status": "healthy", "message": "API is running"}

@app.route('/generate-card')
def generate_card():
    """Generate a welcome card with the given parameters"""
    username = request.args.get('username')
    avatar_url = request.args.get('avatar_url', 'https://images.unsplash.com/photo-1579781403337-de692320718a')
    
    logger.debug(f"Received request with username={username}, avatar_url={avatar_url}")
    
    # Input validation
    if not username:
        return {"error": "Username is required"}, 400
    
    try:
        output_path = generate_welcome_card(username, avatar_url)
        logger.debug(f"Card generated successfully at {output_path}")
        return send_file(output_path, mimetype='image/png', as_attachment=True, download_name='welcome-card.png')
    except Exception as e:
        logger.error(f"Error generating card: {e}")
        return {"error": "Failed to generate welcome card"}, 500

if __name__ == '__main__':
    # ALWAYS serve the app on port 5000
    app.run(host='0.0.0.0', port=5000, debug=True)
