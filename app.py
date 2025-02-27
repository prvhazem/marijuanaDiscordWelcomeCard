import os
import logging
from flask import Flask, request, send_file
from card_generator import generate_welcome_card
import urllib.parse

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "default-secret-key")

# Configure temporary file directory
TEMP_DIR = os.path.join(os.getcwd(), "temp")
os.makedirs(TEMP_DIR, exist_ok=True)

BACKGROUNDS = [
    "https://images.unsplash.com/photo-1513151233558-d860c5398176",
    "https://images.unsplash.com/photo-1503455637927-730bce8583c0"
]
DEFAULT_AVATAR = "https://images.unsplash.com/photo-1579781403337-de692320718a"

def is_valid_url(url):
    try:
        result = urllib.parse.urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

# Log all registered routes
logger.debug("Registered routes:")
for rule in app.url_map.iter_rules():
    logger.debug(f"Route: {rule}")

@app.route('/health')
def health():
    """Health check endpoint to verify API is working"""
    return {"status": "healthy", "message": "API is running"}, 200

@app.route('/generate-card')
def generate_card():
    """
    Generate a welcome card with the given parameters
    Query Parameters:
    - username (required): The username to display on the card
    - avatar_url (optional): URL of the user's avatar image
    - background (optional): Background style (0 or 1)
    Returns:
    - PNG image file
    """
    logger.debug("Received request for /generate-card")
    username = request.args.get('username', '').strip()
    avatar_url = request.args.get('avatar_url', DEFAULT_AVATAR).strip()
    background_index = int(request.args.get('background', '0'))

    logger.debug(f"Parameters: username={username}, avatar_url={avatar_url}, background={background_index}")

    # Input validation
    if not username:
        logger.warning("Username is required but was not provided")
        return {'error': 'Username is required'}, 400

    if not is_valid_url(avatar_url):
        logger.warning(f"Invalid avatar URL provided: {avatar_url}, using default")
        avatar_url = DEFAULT_AVATAR

    if background_index not in [0, 1]:
        logger.warning(f"Invalid background index: {background_index}, using default")
        background_index = 0

    try:
        # Generate welcome card
        output_path = generate_welcome_card(
            username,
            avatar_url,
            BACKGROUNDS[background_index]
        )
        logger.debug(f"Card generated successfully at {output_path}")
        return send_file(output_path, mimetype='image/png')

    except Exception as e:
        logger.error(f"Error generating card: {e}")
        return {'error': 'Failed to generate welcome card'}, 500