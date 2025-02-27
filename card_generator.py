import os
import uuid
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO

def download_image(url):
    response = requests.get(url)
    return Image.open(BytesIO(response.content))

def generate_welcome_card(username, avatar_url):
    # Create a new blank image with the specified dimensions
    background = Image.new('RGBA', (849, 1085), (44, 47, 51))  # Discord-like dark background

    # Create a darker overlay for better text visibility
    overlay = Image.new('RGBA', background.size, (0, 0, 0, 64))
    background = Image.alpha_composite(background, overlay)

    # Download and process avatar
    avatar = download_image(avatar_url)

    # Resize and create circular avatar
    avatar_size = 200  # Larger avatar for the taller card
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
    avatar_pos = ((background.width - avatar_size) // 2, 200)  # Position avatar higher on the taller card
    background.paste(output, avatar_pos, output)

    # Add text
    draw = ImageDraw.Draw(background)

    # Use default font as fallback
    try:
        font_large = ImageFont.truetype("arial.ttf", 72)
        font_small = ImageFont.truetype("arial.ttf", 48)
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

    # Draw text - positioned lower due to taller card
    draw.text((welcome_x, 450), welcome_text, font=font_large, fill='white')
    draw.text((username_x, 550), username_text, font=font_small, fill='white')

    # Save the image
    temp_dir = os.path.join(os.getcwd(), "temp")
    os.makedirs(temp_dir, exist_ok=True)
    output_path = os.path.join(temp_dir, f"{uuid.uuid4()}.png")
    background.save(output_path, 'PNG')

    return output_path