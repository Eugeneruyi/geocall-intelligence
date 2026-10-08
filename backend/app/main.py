from fastapi import FastAPI

from app.database import Base, engine
from app import models

from app.api.locations import router as location_router


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="GeoCall Intelligence API",
    description="Privacy-safe global location and fraud intelligence API",
    version="0.1.0"
)


app.include_router(location_router)


@app.get("/")
def home():
    return {
        "name": "GeoCall Intelligence",
        "status": "online",
        "version": "0.1.0"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }