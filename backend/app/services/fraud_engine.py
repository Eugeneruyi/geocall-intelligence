def analyze_fraud_risk(
    movement_analysis: dict,
    location_confidence: float,
    accuracy_meters: float
) -> dict:
    """
    Calculate a preliminary fraud-risk score from
    movement analysis and location-quality indicators.

    This is a rule-based screening tool, not a
    calibrated probability of fraud.
    """

    # Validate the input data.
    if not 0 <= location_confidence <= 1:
        raise ValueError(
            "Location confidence must be between 0 and 1"
        )

    if accuracy_meters < 0:
        raise ValueError(
            "Location accuracy cannot be negative"
        )

    if not isinstance(movement_analysis, dict):
        raise ValueError(
            "Movement analysis must be a dictionary"
        )

    if "suspicious_movement" not in movement_analysis:
        raise ValueError(
            "Movement analysis is missing suspicious_movement"
        )

    # Begin with no risk points.
    risk_score = 0
    reasons = []

    # Rule 1: Add points for suspicious movement.
    if movement_analysis["suspicious_movement"]:
        risk_score += 60
        reasons.append(
            "Movement exceeded the configured speed threshold."
        )

    # Rule 2: Add points when location confidence is low.
    if location_confidence < 0.60:
        risk_score += 25
        reasons.append(
            "The rule-based location confidence score is low."
        )

    # Rule 3: Add points when reported location accuracy
    # is particularly poor.
    if accuracy_meters > 1000:
        risk_score += 15
        reasons.append(
            "Reported location uncertainty exceeds 1000 metres."
        )

    # Keep the score within the range 0 to 100.
    risk_score = min(risk_score, 100)

    # Convert the score into an overall risk category.
    if risk_score >= 60:
        risk_level = "HIGH"
        recommendation = (
            "Flag for further review before relying on "
            "this location evidence."
        )
    elif risk_score >= 30:
        risk_level = "MEDIUM"
        recommendation = (
            "Review the available location evidence "
            "and other relevant signals."
        )
    else:
        risk_level = "LOW"
        recommendation = (
            "No elevated risk was detected by these rules. "
            "Continue normal monitoring."
        )

    # Explain when no risk indicators were triggered.
    if not reasons:
        reasons.append(
            "No configured risk indicators were triggered."
        )

        # Decide whether the result should trigger an alert.
    alert = risk_level == "HIGH"

    # Give the application a clear next action.
    if risk_level == "HIGH":
        recommended_action = "Request additional verification"
    elif risk_level == "MEDIUM":
        recommended_action = "Review the available evidence"
    else:
        recommended_action = "Continue normal monitoring"

    # Return the complete assessment.
    return {
        "risk_score": risk_score,
        "risk_level": risk_level,
        "alert": alert,
        "reasons": reasons,
        "recommendation": recommendation,
        "recommended_action": recommended_action,
        "assessment_type": "rule_based"
    }
