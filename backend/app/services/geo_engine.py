def analyze_location(
    latitude: float,
    longitude: float,
    accuracy: float,
    source: str
):
    """
    Takes an authorized location signal
    and returns structured location information.
    """

    return {
        "latitude": latitude,
        "longitude": longitude,
        "accuracy_meters": accuracy,
        "confidence": calculate_confidence(accuracy),
        "source": source
    }


def calculate_confidence(accuracy: float):
    """
    Converts GPS accuracy into a simple
    confidence score.
    """

    if accuracy <= 50:
        return 0.98

    if accuracy <= 100:
        return 0.95

    if accuracy <= 300:
        return 0.91

    if accuracy <= 1000:
        return 0.75

    return 0.50