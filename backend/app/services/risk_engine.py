from math import radians, sin, cos, sqrt, atan2


def calculate_distance(
    latitude1: float,
    longitude1: float,
    latitude2: float,
    longitude2: float
) -> float:
    """Calculate the distance between two coordinates in kilometres."""

    earth_radius = 6371.0

    lat1 = radians(latitude1)
    lat2 = radians(latitude2)

    difference_latitude = radians(latitude2 - latitude1)
    difference_longitude = radians(longitude2 - longitude1)

    a = (
        sin(difference_latitude / 2) ** 2
        + cos(lat1) * cos(lat2)
        * sin(difference_longitude / 2) ** 2
    )

    a = max(0.0, min(1.0, a))
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return earth_radius * c


def analyze_movement(
    previous_latitude: float,
    previous_longitude: float,
    previous_timestamp,
    current_latitude: float,
    current_longitude: float,
    current_timestamp,
    max_speed_kmh: float = 1000.0
) -> dict:
    """Flag movement exceeding a configured speed threshold."""

    if max_speed_kmh <= 0:
        raise ValueError("Maximum speed must be positive")

    for latitude in (previous_latitude, current_latitude):
        if not -90 <= latitude <= 90:
            raise ValueError("Latitude must be between -90 and 90")

    for longitude in (previous_longitude, current_longitude):
        if not -180 <= longitude <= 180:
            raise ValueError("Longitude must be between -180 and 180")

    elapsed_seconds = (
        current_timestamp - previous_timestamp
    ).total_seconds()

    if elapsed_seconds <= 0:
        raise ValueError("Current timestamp must be later than previous timestamp")

    distance_km = calculate_distance(
        previous_latitude,
        previous_longitude,
        current_latitude,
        current_longitude
    )

    required_speed_kmh = distance_km / (elapsed_seconds / 3600)
    suspicious = required_speed_kmh > max_speed_kmh

    if suspicious:
        risk_level = "HIGH"
        reason = "Movement exceeds the configured speed threshold."
    else:
        risk_level = "LOW"
        reason = "Movement does not exceed the configured speed threshold."

    return {
        "distance_km": round(distance_km, 2),
        "elapsed_seconds": round(elapsed_seconds, 2),
        "required_speed_kmh": round(required_speed_kmh, 2),
        "risk_level": risk_level,
        "suspicious_movement": suspicious,
        "reason": reason
    }
