from datetime import datetime

from sqlalchemy import Column, Integer, Float, String, DateTime
from geoalchemy2 import Geography

from app.database import Base


class LocationEvent(Base):
    __tablename__ = "location_events"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, nullable=False)

    latitude = Column(Float, nullable=False)

    longitude = Column(Float, nullable=False)

    accuracy = Column(Float, nullable=False)

    source = Column(String, nullable=False)

    confidence = Column(Float, nullable=False)

    location = Column(
        Geography(
            geometry_type="POINT",
            srid=4326
        ),
        nullable=True
    )

    timestamp = Column(
        DateTime,
        default=datetime.utcnow
    )