// ==========================================
// GEOCALL INTELLIGENCE
// Dashboard JavaScript
// ==========================================


// ==========================================
// API ENDPOINTS
// ==========================================

// Use relative URLs because the dashboard and
// FastAPI backend are served from the same server.

const API_URL = "/locations/fraud-dashboard/1";
const HISTORY_URL = "/locations/history/1";
const RISK_URL = "/locations/risk/1";


// ==========================================
// DASHBOARD HTML ELEMENTS
// ==========================================

const connectionStatus = document.getElementById("connection-status");
const refreshButton = document.getElementById("refresh-button");

const totalAssessments = document.getElementById("total-assessments");
const highRisk = document.getElementById("high-risk");
const mediumRisk = document.getElementById("medium-risk");
const lowRisk = document.getElementById("low-risk");
const alertsCount = document.getElementById("alerts-count");

const alertsContainer = document.getElementById("alerts-container");
const alertPanelCount = document.getElementById("alert-panel-count");
const assessmentsTable = document.getElementById("assessments-table");


// ==========================================
// MAP HTML ELEMENTS
// ==========================================

const mapElement = document.getElementById("geo-map");
const mapStatus = document.getElementById("map-status");

const movementDistance = document.getElementById("movement-distance");
const movementTime = document.getElementById("movement-time");
const movementSpeed = document.getElementById("movement-speed");
const movementRisk = document.getElementById("movement-risk");
const movementReason = document.getElementById("movement-reason");
const movementIntro = document.querySelector(".movement-intro");


// ==========================================
// MAP VARIABLES
// ==========================================

let geoMap = null;
let locationLayer = null;
let movementLine = null;
let assessmentLine = null;

// Keep references to markers and loaded assessments
// so alerts and table rows can navigate the map.
const locationMarkers = new Map();
let dashboardAssessments = [];


// ==========================================
// HELPER: UPDATE CONNECTION STATUS
// ==========================================

function setConnectionStatus(message, connected) {

    if (!connectionStatus) {
        return;
    }

    connectionStatus.textContent = message;

    const dot = connectionStatus.previousElementSibling;

    if (dot) {
        dot.style.backgroundColor =
            connected ? "#39d5a2" : "#ff5d70";
    }
}


// ==========================================
// HELPER: SAFELY DISPLAY TEXT IN HTML
// ==========================================

function escapeHTML(value) {

    const characters = {
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#039;"
    };

    return String(value ?? "").replace(
        /[&<>"']/g,
        character => characters[character]
    );
}


// ==========================================
// HELPER: FORMAT TIMESTAMP
// ==========================================

function formatTimestamp(timestamp) {

    if (!timestamp) {
        return "Not available";
    }

    const date = new Date(timestamp);

    if (Number.isNaN(date.getTime())) {
        return "Invalid timestamp";
    }

    return date.toLocaleString();
}


// ==========================================
// HELPER: FORMAT DURATION
// ==========================================

function formatDuration(seconds) {

    const value = Number(seconds);

    if (!Number.isFinite(value)) {
        return "Not available";
    }

    if (value < 60) {
        return `${value.toFixed(2)} seconds`;
    }

    const minutes = value / 60;

    if (minutes < 60) {
        return `${minutes.toFixed(2)} minutes`;
    }

    const hours = minutes / 60;

    return `${hours.toFixed(2)} hours`;
}


// ==========================================
// HELPER: SELECT RISK BADGE STYLING
// ==========================================

function getRiskClass(riskLevel) {

    switch (riskLevel) {

        case "HIGH":
            return "risk-high";

        case "MEDIUM":
            return "risk-medium";

        case "LOW":
            return "risk-low";

        default:
            return "";
    }
}


// ==========================================
// HELPER: UPDATE MAP STATUS
// ==========================================

function setMapStatus(message) {

    if (mapStatus) {
        mapStatus.textContent = message;
    }
}


// ==========================================
// INITIALIZE MAP
// ==========================================

function initializeMap() {

    // Make sure the HTML map element exists.
    if (!mapElement) {
        console.warn("Map element #geo-map was not found.");
        return false;
    }

    // Make sure Leaflet loaded.
    if (typeof L === "undefined") {
        console.error("Leaflet library is not available.");
        setMapStatus("Map library failed to load.");
        return false;
    }

    // Do not create the map more than once.
    if (geoMap) {
        return true;
    }

    try {

        // Create the map.
        geoMap = L.map("geo-map", {
            zoomControl: true
        });

        // Initial global-ish view.
        geoMap.setView([6.5244, 3.3792], 5);

        // OpenStreetMap base map.
        L.tileLayer(
            "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
            {
                attribution: "&copy; OpenStreetMap contributors",
                maxZoom: 19
            }
        ).addTo(geoMap);

        // Layer containing location markers.
        locationLayer = L.layerGroup().addTo(geoMap);

        setMapStatus("Map ready. Loading location intelligence...");

        // Sometimes the map needs a resize after
        // the dashboard layout has rendered.
        setTimeout(() => {
            if (geoMap) {
                geoMap.invalidateSize();
            }
        }, 300);

        return true;

    } catch (error) {

        console.error("Unable to initialize map:", error);

        setMapStatus("Unable to initialize map.");

        return false;
    }
}


// ==========================================
// CREATE LOCATION MARKER
// ==========================================

function createLocationMarker(location, isCurrent, isPrevious, isHighRisk) {

    const latitude = Number(location.latitude);
    const longitude = Number(location.longitude);

    if (
        !Number.isFinite(latitude) ||
        !Number.isFinite(longitude)
    ) {
        return null;
    }

    let markerColor = "#39d5a2";

    if (isCurrent && isHighRisk) {
        markerColor = "#ff5d70";
    } else if (isPrevious) {
        markerColor = "#64b5f6";
    }

    const marker = L.circleMarker(
        [latitude, longitude],
        {
            radius: isCurrent ? 10 : 7,

            color: markerColor,

            fillColor: markerColor,

            fillOpacity: 0.85,

            weight: isCurrent ? 3 : 2
        }
    );

    const locationLabel = isCurrent
        ? "Current Location"
        : isPrevious
            ? "Previous Location"
            : "Location Event";

    const popupHTML = `
        <div class="map-popup-title">
            ${escapeHTML(locationLabel)}
        </div>

        <div class="map-popup-detail">
            <strong>ID:</strong>
            ${escapeHTML(location.id)}
        </div>

        <div class="map-popup-detail">
            <strong>Latitude:</strong>
            ${escapeHTML(latitude.toFixed(6))}
        </div>

        <div class="map-popup-detail">
            <strong>Longitude:</strong>
            ${escapeHTML(longitude.toFixed(6))}
        </div>

        <div class="map-popup-detail">
            <strong>Accuracy:</strong>
            ${escapeHTML(location.accuracy_meters)} m
        </div>

        <div class="map-popup-detail">
            <strong>Confidence:</strong>
            ${escapeHTML(location.confidence)}
        </div>

        <div class="map-popup-detail">
            <strong>Source:</strong>
            ${escapeHTML(location.source)}
        </div>

        <div class="map-popup-detail">
            <strong>Time:</strong>
            ${escapeHTML(formatTimestamp(location.timestamp))}
        </div>
    `;

    marker.bindPopup(popupHTML);

    return marker;
}


// ==========================================
// DRAW MOVEMENT LINE
// ==========================================

function drawMovementLine(
    previousLocation,
    currentLocation,
    riskLevel,
    suspiciousMovement
) {

    if (!geoMap) {
        return;
    }

    if (!previousLocation || !currentLocation) {
        return;
    }

    const previousLat = Number(previousLocation.latitude);
    const previousLng = Number(previousLocation.longitude);

    const currentLat = Number(currentLocation.latitude);
    const currentLng = Number(currentLocation.longitude);

    if (
        !Number.isFinite(previousLat) ||
        !Number.isFinite(previousLng) ||
        !Number.isFinite(currentLat) ||
        !Number.isFinite(currentLng)
    ) {
        return;
    }

    // Remove old line.
    if (movementLine) {
        geoMap.removeLayer(movementLine);
        movementLine = null;
    }

    const highRiskMovement =
        riskLevel === "HIGH" ||
        suspiciousMovement === true;

    const lineColor = highRiskMovement
        ? "#ff5d70"
        : "#39d5a2";

    movementLine = L.polyline(
        [
            [previousLat, previousLng],
            [currentLat, currentLng]
        ],
        {
            color: lineColor,
            weight: 4,
            opacity: 0.85,
            dashArray: highRiskMovement ? "10, 10" : null,
            className: "movement-line"
        }
    ).addTo(geoMap);

    movementLine.bindPopup(`
        <div class="map-popup-title">
            Movement Analysis
        </div>

        <div class="map-popup-detail">
            From location
            <strong>${escapeHTML(previousLocation.id)}</strong>
            to location
            <strong>${escapeHTML(currentLocation.id)}</strong>
        </div>

        <div class="map-popup-detail">
            Risk:
            <strong>${escapeHTML(riskLevel)}</strong>
        </div>
    `);
}


// ==========================================
// UPDATE MOVEMENT DETAILS
// ==========================================

function updateMovementDetails(riskData) {

    if (!riskData) {
        return;
    }

    const movement = riskData.movement_analysis || {};

    const distance = Number(movement.distance_km);
    const elapsed = Number(movement.elapsed_seconds);
    const speed = Number(movement.required_speed_kmh);

    // Distance
    if (movementDistance) {

        if (Number.isFinite(distance)) {
            movementDistance.textContent =
                `${distance.toFixed(1)} km`;
        } else {
            movementDistance.textContent = "—";
        }
    }

    // Time
    if (movementTime) {

        if (Number.isFinite(elapsed)) {
            movementTime.textContent =
                formatDuration(elapsed);
        } else {
            movementTime.textContent = "—";
        }
    }

    // Required speed
    if (movementSpeed) {

        if (Number.isFinite(speed)) {
            movementSpeed.textContent =
                `${speed.toFixed(2)} km/h`;
        } else {
            movementSpeed.textContent = "—";
        }
    }

    // Risk level
    if (movementRisk) {

        movementRisk.textContent =
            movement.risk_level ||
            riskData.risk_level ||
            "UNKNOWN";

        const risk = (
            movement.risk_level ||
            riskData.risk_level ||
            ""
        ).toUpperCase();

        if (risk === "HIGH") {
            movementRisk.style.color = "#ff5d70";
        } else if (risk === "MEDIUM") {
            movementRisk.style.color = "#f0b85a";
        } else {
            movementRisk.style.color = "#39d5a2";
        }
    }

    // Reason
    if (movementReason) {

        const reason =
            movement.reason ||
            riskData.recommendation ||
            "No additional movement explanation available.";

        movementReason.textContent = reason;
    }

    // Introduction
    if (movementIntro) {

        if (
            riskData.previous_location_id !== undefined &&
            riskData.current_location_id !== undefined
        ) {

            movementIntro.textContent =
                `Movement analysis from location ` +
                `${riskData.previous_location_id} ` +
                `to location ${riskData.current_location_id}.`;

        } else {

            movementIntro.textContent =
                "Latest geographic movement analysis.";
        }
    }
}


// ==========================================
// DISPLAY LOCATION HISTORY ON MAP
// ==========================================

function displayLocationHistory(history, riskData) {

    if (!geoMap || !locationLayer) {
        return;
    }

    // Remove existing markers.
    locationLayer.clearLayers();
    locationMarkers.clear();

    // Remove existing movement line.
    if (movementLine) {
        geoMap.removeLayer(movementLine);
        movementLine = null;
    }

    if (!Array.isArray(history) || history.length === 0) {

        setMapStatus(
            "No location history is available."
        );

        return;
    }

    // Risk endpoint tells us which two locations
    // were used for the movement calculation.
    const previousId = riskData
        ? riskData.previous_location_id
        : null;

    const currentId = riskData
        ? riskData.current_location_id
        : null;

    const movementAnalysis =
        riskData
            ? riskData.movement_analysis || {}
            : {};

    const riskLevel =
        movementAnalysis.risk_level ||
        riskData?.risk_level ||
        "UNKNOWN";

    const suspiciousMovement =
        movementAnalysis.suspicious_movement === true;


    // Find previous/current locations.
    const previousLocation = history.find(
        location =>
            String(location.id) === String(previousId)
    );

    const currentLocation = history.find(
        location =>
            String(location.id) === String(currentId)
    );


    // Create markers.
    const validCoordinates = [];

    history.forEach(location => {

        const latitude = Number(location.latitude);
        const longitude = Number(location.longitude);

        if (
            !Number.isFinite(latitude) ||
            !Number.isFinite(longitude)
        ) {
            return;
        }

        const isCurrent =
            String(location.id) === String(currentId);

        const isPrevious =
            String(location.id) === String(previousId);

        const marker = createLocationMarker(
            location,
            isCurrent,
            isPrevious,
            riskLevel === "HIGH"
        );

        if (marker) {

            marker.addTo(locationLayer);

            // Index each marker by its location ID.
            locationMarkers.set(
                String(location.id),
                marker
            );

            validCoordinates.push([
                latitude,
                longitude
            ]);
        }
    });


    // Draw the movement line.
    if (previousLocation && currentLocation) {

        drawMovementLine(
            previousLocation,
            currentLocation,
            riskLevel,
            suspiciousMovement
        );
    }


    // Zoom the map so all known locations are visible.
    if (validCoordinates.length > 0) {

        try {

            const bounds =
                L.latLngBounds(validCoordinates);

            geoMap.fitBounds(bounds, {
                padding: [40, 40],
                maxZoom: 12
            });

        } catch (error) {

            console.error(
                "Unable to fit map bounds:",
                error
            );
        }
    }


    // Update status.
    if (previousLocation && currentLocation) {

        setMapStatus(
            `Showing ${history.length} location events. ` +
            `Movement ${previousId} → ${currentId}.`
        );

    } else {

        setMapStatus(
            `Showing ${history.length} location events.`
        );
    }
}


// ==========================================
// FETCH MAP DATA
// ==========================================

async function loadMapData() {

    if (!initializeMap()) {
        return;
    }

    setMapStatus(
        "Loading geographic intelligence..."
    );

    try {

        // Fetch both endpoints at the same time.
        const [historyResponse, riskResponse] =
            await Promise.all([
                fetch(HISTORY_URL),
                fetch(RISK_URL)
            ]);


        // Check history endpoint.
        if (!historyResponse.ok) {

            throw new Error(
                `Location history API returned HTTP ` +
                `${historyResponse.status}`
            );
        }


        // Check risk endpoint.
        if (!riskResponse.ok) {

            throw new Error(
                `Risk API returned HTTP ` +
                `${riskResponse.status}`
            );
        }


        const history =
            await historyResponse.json();

        const riskData =
            await riskResponse.json();


        // Validate history response.
        if (!Array.isArray(history)) {

            throw new Error(
                "Location history API returned unexpected data."
            );
        }


        // Update movement information.
        updateMovementDetails(riskData);


        // Draw map.
        displayLocationHistory(
            history,
            riskData
        );


        // Force Leaflet to recalculate its size.
        setTimeout(() => {

            if (geoMap) {
                geoMap.invalidateSize();
            }

        }, 200);


    } catch (error) {

        console.error(
            "Unable to load geographic intelligence:",
            error
        );

        setMapStatus(
            "Unable to load geographic intelligence. " +
            "Check that the API is running."
        );


        // Show safe fallback values.
        if (movementDistance) {
            movementDistance.textContent = "—";
        }

        if (movementTime) {
            movementTime.textContent = "—";
        }

        if (movementSpeed) {
            movementSpeed.textContent = "—";
        }

        if (movementRisk) {
            movementRisk.textContent = "—";
        }

        if (movementReason) {
            movementReason.textContent =
                "Unable to retrieve movement analysis.";
        }
    }
}


// ==========================================
// FETCH DASHBOARD DATA
// ==========================================

async function loadDashboard() {

    setConnectionStatus(
        "Connecting...",
        false
    );

    refreshButton.disabled = true;
    refreshButton.textContent = "Loading...";


    try {

        // Ask FastAPI for dashboard statistics.
        const response =
            await fetch(API_URL);


        // Stop if server returned an HTTP error.
        if (!response.ok) {

            throw new Error(
                `API returned HTTP ${response.status}`
            );
        }


        // Convert JSON response into JavaScript object.
        const data =
            await response.json();


        // Validate response.
        if (
            !data.summary ||
            !Array.isArray(data.recent_assessments)
        ) {

            throw new Error(
                "The dashboard API returned unexpected data."
            );
        }


        // Update dashboard sections.
        // Save the assessments for click handling.
        dashboardAssessments =
            data.recent_assessments;

        updateSummary(data.summary);

        updateAlerts(
            data.recent_assessments
        );

        updateAssessmentsTable(
            data.recent_assessments
        );


        setConnectionStatus(
            "API Connected",
            true
        );


    } catch (error) {

        console.error(
            "Unable to load dashboard:",
            error
        );

        setConnectionStatus(
            "Connection Failed",
            false
        );

        showDashboardError();


    } finally {

        refreshButton.disabled = false;
        refreshButton.textContent = "↻ Refresh";
    }


    // Load map separately.
    // A map failure should not break the
    // main fraud dashboard.
    loadMapData();
}


// ==========================================
// UPDATE SUMMARY CARDS
// ==========================================

function updateSummary(summary) {

    totalAssessments.textContent =
        summary.total_assessments ?? 0;

    highRisk.textContent =
        summary.high_risk ?? 0;

    mediumRisk.textContent =
        summary.medium_risk ?? 0;

    lowRisk.textContent =
        summary.low_risk ?? 0;

    alertsCount.textContent =
        summary.alerts_requiring_review ?? 0;
}


// ==========================================
// DISPLAY SECURITY ALERTS
// ==========================================

function updateAlerts(assessments) {

    // Only assessments that triggered an alert.
    const alerts = assessments.filter(
        assessment =>
            assessment.alert === true
    );


    alertPanelCount.textContent =
        `${alerts.length} ` +
        `${alerts.length === 1 ? "alert" : "alerts"}`;


    // No alerts.
    if (alerts.length === 0) {

        alertsContainer.innerHTML = `
            <div class="empty-state">
                No alerts requiring review were found
                in the five most recent assessments.
            </div>
        `;

        return;
    }


    // Display alerts.
    alertsContainer.innerHTML =
        alerts.map(assessment => `

            <article
                class="alert-item"
                data-assessment-id="${escapeHTML(assessment.id)}"
                tabindex="0"
                role="button"
                aria-label="View assessment ${escapeHTML(assessment.id)} on map"
                style="cursor: pointer;"
            >

                <div class="alert-symbol">
                    !
                </div>

                <div class="alert-content">

                    <h3>
                        HIGH-PRIORITY REVIEW —
                        Assessment #
                        ${escapeHTML(assessment.id)}
                    </h3>

                    <p>
                        Movement between location
                        ${escapeHTML(
                            assessment.previous_location_id
                        )}
                        and location
                        ${escapeHTML(
                            assessment.current_location_id
                        )}
                        triggered a fraud-risk alert.
                    </p>

                    <p>
                        Recommended action:
                        ${escapeHTML(
                            assessment.recommended_action
                        )}
                    </p>

                </div>

                <div class="alert-score">
                    ${escapeHTML(
                        assessment.risk_score
                    )}/100
                </div>

            </article>

        `).join("");
}


// ==========================================
// DISPLAY RECENT ASSESSMENTS
// ==========================================

function updateAssessmentsTable(assessments) {

    if (assessments.length === 0) {

        assessmentsTable.innerHTML = `
            <tr>
                <td
                    colspan="6"
                    class="empty-state"
                >
                    No fraud assessments have
                    been recorded yet.
                </td>
            </tr>
        `;

        return;
    }


    assessmentsTable.innerHTML =
        assessments.map(assessment => {

            const riskClass =
                getRiskClass(
                    assessment.risk_level
                );


            let scoreClass = "score-low";


            if (
                assessment.risk_level === "HIGH"
            ) {

                scoreClass = "score-high";

            } else if (
                assessment.risk_level === "MEDIUM"
            ) {

                scoreClass = "score-medium";
            }


            return `

                <tr
                    data-assessment-id="${escapeHTML(assessment.id)}"
                    tabindex="0"
                    style="cursor: pointer;"
                >

                    <td>
                        #
                        ${escapeHTML(
                            assessment.id
                        )}
                    </td>

                    <td>

                        <span
                            class="score-value
                            ${scoreClass}"
                        >
                            ${escapeHTML(
                                assessment.risk_score
                            )}/100
                        </span>

                    </td>

                    <td>

                        <span
                            class="risk-badge
                            ${riskClass}"
                        >
                            ${escapeHTML(
                                assessment.risk_level
                            )}
                        </span>

                    </td>

                    <td>

                        ${escapeHTML(
                            assessment.previous_location_id
                        )}

                        →

                        ${escapeHTML(
                            assessment.current_location_id
                        )}

                    </td>

                    <td class="action-cell">

                        ${escapeHTML(
                            assessment.recommended_action
                        )}

                    </td>

                    <td class="timestamp-cell">

                        ${escapeHTML(
                            formatTimestamp(
                                assessment.timestamp
                            )
                        )}

                    </td>

                </tr>

            `;

        }).join("");
}


// ==========================================
// DISPLAY DASHBOARD ERRORS
// ==========================================

function showDashboardError() {

    totalAssessments.textContent = "—";
    highRisk.textContent = "—";
    mediumRisk.textContent = "—";
    lowRisk.textContent = "—";
    alertsCount.textContent = "—";


    alertsContainer.innerHTML = `
        <div class="empty-state">

            Unable to retrieve security alerts.

            Check that the GeoCall API is running.

        </div>
    `;


    assessmentsTable.innerHTML = `
        <tr>

            <td
                colspan="6"
                class="empty-state"
            >

                Unable to load assessments.

                Please check the API connection.

            </td>

        </tr>
    `;
}


// ==========================================
// NAVIGATE TO AN ASSESSMENT'S LOCATIONS
// ==========================================


function focusAssessment(assessmentId) {

    const assessment = dashboardAssessments.find(
        item => String(item.id) === String(assessmentId)
    );

    if (!assessment || !geoMap) {
        return;
    }

    const previousId = String(assessment.previous_location_id);
    const currentId = String(assessment.current_location_id);

    const previousMarker = locationMarkers.get(previousId);
    const currentMarker = locationMarkers.get(currentId);

    console.log("Assessment selected:", assessment);
    console.log("Previous marker found:", Boolean(previousMarker), previousId);
    console.log("Current marker found:", Boolean(currentMarker), currentId);

    const markers = [previousMarker, currentMarker].filter(Boolean);

    if (markers.length === 0) {
        setMapStatus(
            `Assessment #${assessment.id} selected. ` +
            "Its locations are not available on the map."
        );
        return;
    }

    // Remove the previous assessment highlight.
    if (assessmentLine) {
        geoMap.removeLayer(assessmentLine);
        assessmentLine = null;
    }

    // Draw a separate red dashed line for this assessment.
    if (previousMarker && currentMarker && previousId !== currentId) {

        const previousPoint = previousMarker.getLatLng();
        const currentPoint = currentMarker.getLatLng();

        assessmentLine = L.polyline(
            [previousPoint, currentPoint],
            {
                color: "#ff5d70",
                weight: 6,
                opacity: 1,
                dashArray: "8, 8"
            }
        ).addTo(geoMap);

        assessmentLine.bindPopup(`
            <div class="map-popup-title">
                Selected Fraud Assessment
            </div>
            <div class="map-popup-detail">
                Assessment:
                <strong>#${escapeHTML(assessment.id)}</strong>
            </div>
            <div class="map-popup-detail">
                Movement:
                <strong>${escapeHTML(previousId)} → ${escapeHTML(currentId)}</strong>
            </div>
            <div class="map-popup-detail">
                Risk:
                <strong>${escapeHTML(assessment.risk_level)}</strong>
            </div>
            <div class="map-popup-detail">
                Risk score:
                <strong>${escapeHTML(assessment.risk_score)}/100</strong>
            </div>
        `);
    }

    // Zoom to the selected locations.
    const bounds = L.latLngBounds(
        markers.map(marker => marker.getLatLng())
    );

    if (bounds.isValid()) {
        geoMap.fitBounds(bounds, {
            padding: [60, 60],
            maxZoom: 8
        });
    }

    // Open the current location popup.
    if (currentMarker) {
        currentMarker.openPopup();
    } else if (previousMarker) {
        previousMarker.openPopup();
    }

    setMapStatus(
        `Viewing assessment #${assessment.id}: ` +
        `locations ${previousId} → ${currentId}. ` +
        `Risk: ${assessment.risk_level}. ` +
        "Red dashed line shows this selected assessment."
    );
}


// ==========================================
// CONNECT ALERTS AND ASSESSMENT ROWS
// ==========================================

function handleAssessmentSelection(event) {

    const item = event.target.closest(
        "[data-assessment-id]"
    );

    if (!item) {
        return;
    }

    focusAssessment(
        item.dataset.assessmentId
    );
}

alertsContainer.addEventListener(
    "click",
    handleAssessmentSelection
);

assessmentsTable.addEventListener(
    "click",
    handleAssessmentSelection
);

function handleAssessmentKeyboard(event) {

    if (
        event.key !== "Enter" &&
        event.key !== " "
    ) {
        return;
    }

    const item = event.target.closest(
        "[data-assessment-id]"
    );

    if (!item) {
        return;
    }

    event.preventDefault();

    focusAssessment(
        item.dataset.assessmentId
    );
}

alertsContainer.addEventListener(
    "keydown",
    handleAssessmentKeyboard
);

assessmentsTable.addEventListener(
    "keydown",
    handleAssessmentKeyboard
);


// ==========================================
// CONNECT REFRESH BUTTON
// ==========================================

refreshButton.addEventListener(
    "click",
    loadDashboard
);


// ==========================================
// LOAD DATA WHEN PAGE OPENS
// ==========================================

initializeMap();

loadDashboard();