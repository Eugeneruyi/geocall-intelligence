from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.database import Base, engine
from app import models
from app.api.locations import router as location_router


# Find the main GeoCall project folder.
# main.py is inside backend/app/, so parents[2] is the project root.
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Keep the existing database table setup.
Base.metadata.create_all(bind=engine)


# Create the FastAPI application.
app = FastAPI(
    title="GeoCall Intelligence API",
    description="Privacy-safe global location and fraud intelligence API",
    version="0.1.0"
)


# Keep the existing location and fraud API routes.
app.include_router(location_router)


# Allow FastAPI to serve CSS and JavaScript files.
app.mount(
    "/static",
    StaticFiles(directory=PROJECT_ROOT / "frontend" / "static"),
    name="static"
)


# Display the dashboard in the browser.
@app.get("/dashboard", include_in_schema=False)
def dashboard():
    return FileResponse(
        PROJECT_ROOT / "frontend" / "templates" / "index.html"
    )


# Existing home endpoint.
@app.get("/")
def home():
    return {
        "name": "GeoCall Intelligence",
        "status": "online",
        "version": "0.1.0"
    }


# Existing health-check endpoint.
@app.get("/health")
def health():
    return {
        "status": "healthy"
    }
