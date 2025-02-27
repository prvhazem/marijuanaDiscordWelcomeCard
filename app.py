import os
import logging
from flask import Flask, request, render_template, jsonify, send_file
from card_generator import generate_welcome_card
import urllib.parse
import requests
from PIL import Image
from io import BytesIO

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "default-secret-key")

# Configure temporary file directory
TEMP_DIR = "static/temp"
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

def download_image(url):
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return Image.open(BytesIO(response.content))
    except Exception as e:
        logger.error(f"Error downloading image: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate-card')
def generate_card():
    username = request.args.get('username', '').strip()
    avatar_url = request.args.get('avatar_url', DEFAULT_AVATAR).strip()
    background_index = int(request.args.get('background', 0))

    # Input validation
    if not username:
        return jsonify({'error': 'Username is required'}), 400
    
    if not is_valid_url(avatar_url):
        avatar_url = DEFAULT_AVATAR
    
    if background_index not in [0, 1]:
        background_index = 0

    try:
        # Generate welcome card
        output_path = generate_welcome_card(
            username,
            avatar_url,
            BACKGROUNDS[background_index]
        )
        
        return send_file(output_path, mimetype='image/png')
    
    except Exception as e:
        logger.error(f"Error generating card: {e}")
        return jsonify({'error': 'Failed to generate welcome card'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
