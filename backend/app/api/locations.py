from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import LocationEvent
from app.services.geo_engine import analyze_location


router = APIRouter(
    prefix="/locations",
    tags=["Locations"]
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.post("/analyze")
def analyze(
    latitude: float,
    longitude: float,
    accuracy: float,
    source: str,
    db: Session = Depends(get_db)
):
    result = analyze_location(
        latitude,
        longitude,
        accuracy,
        source
    )

    location_event = LocationEvent(
    user_id=1,
    latitude=latitude,
    longitude=longitude,
    accuracy=accuracy,
    source=source,
    confidence=result["confidence"],
    location=f"SRID=4326;POINT({longitude} {latitude})"
)
    db.add(location_event)
    db.commit()
    db.refresh(location_event)

    return {
        "id": location_event.id,
        "latitude": latitude,
        "longitude": longitude,
        "accuracy_meters": accuracy,
        "confidence": result["confidence"],
        "source": source,
        "status": "location saved"
    }

@router.get("/history/{user_id}")
def location_history(
    user_id: int,
    db: Session = Depends(get_db)
):
    locations = (
        db.query(LocationEvent)
        .filter(LocationEvent.user_id == user_id)
        .order_by(LocationEvent.timestamp.desc())
        .all()
    )

    return [
        {
            "id": location.id,
            "latitude": location.latitude,
            "longitude": location.longitude,
            "accuracy_meters": location.accuracy,
            "confidence": location.confidence,
            "source": location.source,
            "timestamp": location.timestamp
        }
        for location in locations
    ]