import os
# Set Gunicorn to use Uvicorn's ASGI worker. This line is irrelevant now that we are using Flask.
#os.environ["GUNICORN_CMD_ARGS"] = "--worker-class uvicorn.workers.UvicornWorker"

import logging
#from fastapi import FastAPI, Query, HTTPException, Request
#from fastapi.responses import FileResponse, JSONResponse
#from fastapi.middleware.cors import CORSMiddleware
import urllib.parse
import traceback

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Log startup environment
logger.debug(f"GUNICORN_CMD_ARGS: {os.environ.get('GUNICORN_CMD_ARGS')}")

#app = FastAPI(
#    title="Discord Welcome Card Generator",
#    description="API to generate welcome cards for Discord users",
#    version="1.0.0"
#)
#

#@app.on_event("startup")
#async def startup_event():
#    logger.debug("FastAPI application startup complete")
#
## Add CORS middleware. This is now handled by Flask-Cors if needed.
#app.add_middleware(
#    CORSMiddleware,
#    allow_origins=["*"],
#    allow_credentials=True,
#    allow_methods=["*"],
#    allow_headers=["*"],
#)
#
#@app.exception_handler(Exception)
#async def global_exception_handler(request: Request, exc: Exception):
#    logger.error(f"Unhandled error: {exc}")
#    logger.error(traceback.format_exc())
#    return JSONResponse(
#        status_code=500,
#        content={"detail": str(exc)},
#    )
#
#@app.get("/health")
#async def health():
#    """Health check endpoint to verify API is working"""
#    logger.debug("Health check endpoint called")
#    return {"status": "healthy", "message": "API is running"}

DEFAULT_AVATAR = "https://images.unsplash.com/photo-1579781403337-de692320718a"

def is_valid_url(url: str) -> bool:
    try:
        result = urllib.parse.urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

#The following functions are now assumed to be in the Flask app, and will be called from the Flask routes.
#These functions are not modified.

# from app import generate_welcome_card #This is assumed to be handled by the Flask app now.


from app import app

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)