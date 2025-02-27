import os
import uuid
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO

def download_image(url):
    response = requests.get(url)
    return Image.open(BytesIO(response.content))

def generate_welcome_card(username, avatar_url, background_url):
    # Download images
    background = download_image(background_url)
    avatar = download_image(avatar_url)

    # Resize background to 1200x400
    background = background.resize((1200, 400))

    # Create a darker overlay for better text visibility
    overlay = Image.new('RGBA', background.size, (0, 0, 0, 128))
    background = Image.alpha_composite(background.convert('RGBA'), overlay)

    # Resize and create circular avatar
    avatar_size = 150
    avatar = avatar.resize((avatar_size, avatar_size))

    # Create circular mask
    mask = Image.new('L', (avatar_size, avatar_size), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, avatar_size, avatar_size), fill=255)

    # Apply mask to avatar
    output = Image.new('RGBA', (avatar_size, avatar_size), (0, 0, 0, 0))
    output.paste(avatar, (0, 0))
    output.putalpha(mask)

    # Paste avatar onto background
    avatar_pos = ((background.width - avatar_size) // 2, 50)
    background.paste(output, avatar_pos, output)

    # Add welcome text
    draw = ImageDraw.Draw(background)

    # Use default font as fallback
    try:
        font_large = ImageFont.truetype("arial.ttf", 60)
        font_small = ImageFont.truetype("arial.ttf", 40)
    except:
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()

    # Add text
    welcome_text = "Welcome!"
    username_text = f"@{username}"

    # Calculate text positions
    welcome_bbox = draw.textbbox((0, 0), welcome_text, font=font_large)
    welcome_width = welcome_bbox[2] - welcome_bbox[0]
    welcome_x = (background.width - welcome_width) // 2

    username_bbox = draw.textbbox((0, 0), username_text, font=font_small)
    username_width = username_bbox[2] - username_bbox[0]
    username_x = (background.width - username_width) // 2

    # Draw text
    draw.text((welcome_x, 250), welcome_text, font=font_large, fill='white')
    draw.text((username_x, 320), username_text, font=font_small, fill='white')

    # Save the image to temp directory
    temp_dir = os.path.join(os.getcwd(), "temp")
    os.makedirs(temp_dir, exist_ok=True)
    output_path = os.path.join(temp_dir, f"{uuid.uuid4()}.png")
    background.save(output_path, 'PNG')

    return output_path