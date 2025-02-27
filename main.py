import os
os.environ["GUNICORN_CMD_ARGS"] = "--worker-class uvicorn.workers.UvicornWorker"

import logging
from fastapi import FastAPI, Query, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from card_generator import generate_welcome_card
import urllib.parse
import traceback

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Discord Welcome Card Generator",
    description="API to generate welcome cards for Discord users",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure temporary file directory
TEMP_DIR = os.path.join(os.getcwd(), "temp")
os.makedirs(TEMP_DIR, exist_ok=True)

BACKGROUNDS = [
    "https://images.unsplash.com/photo-1513151233558-d860c5398176",
    "https://images.unsplash.com/photo-1503455637927-730bce8583c0"
]
DEFAULT_AVATAR = "https://images.unsplash.com/photo-1579781403337-de692320718a"

def is_valid_url(url: str) -> bool:
    try:
        result = urllib.parse.urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error: {exc}")
    logger.error(traceback.format_exc())
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc)},
    )

@app.get("/health")
async def health():
    """Health check endpoint to verify API is working"""
    logger.debug("Health check endpoint called")
    return {"status": "healthy", "message": "API is running"}

@app.get("/generate-card")
async def generate_card(
    username: str = Query(..., description="The username to display on the card"),
    avatar_url: str = Query(DEFAULT_AVATAR, description="URL of the user's avatar image"),
    background: int = Query(0, description="Background style (0 or 1)")
):
    """
    Generate a welcome card with the given parameters.

    Returns a PNG image file of the generated welcome card.
    """
    logger.debug(f"Received request with username={username}, avatar_url={avatar_url}, background={background}")

    # Input validation
    if not username.strip():
        raise HTTPException(status_code=400, detail="Username is required")

    if not is_valid_url(avatar_url):
        logger.warning(f"Invalid avatar URL provided: {avatar_url}, using default")
        avatar_url = DEFAULT_AVATAR

    if background not in [0, 1]:
        logger.warning(f"Invalid background index: {background}, using default")
        background = 0

    try:
        output_path = generate_welcome_card(
            username,
            avatar_url,
            BACKGROUNDS[background]
        )
        logger.debug(f"Card generated successfully at {output_path}")
        return FileResponse(output_path, media_type="image/png", filename="welcome-card.png")

    except Exception as e:
        logger.error(f"Error generating card: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Failed to generate welcome card")