"""
Intelligent Smart City Traffic Monitoring System
--------------------------------------------------
Simulates data ingestion from traffic cameras and road sensors,
computes a congestion score per intersection, and raises an alert
to a (mocked) traffic-authority endpoint when congestion crosses
a threshold.

Endpoints:
  GET  /                      -> health/info
  GET  /sensors                -> list current sensor readings (simulated)
  GET  /intersections/<id>     -> congestion status for one intersection
  GET  /intersections          -> congestion status for all intersections
  POST /alert/test             -> manually trigger an alert (for demo)
  GET  /alerts                 -> list alerts raised so far
"""

import random
import time
import threading
from datetime import datetime, timezone
from flask import Flask, jsonify, request

app = Flask(__name__)

# ---------------------------------------------------------------------
# In-memory "database" of intersections. Each intersection has a camera
# feed (vehicle count via simulated CV output) and a sensor feed
# (average speed in km/h). In a real deployment these would come from
# actual camera/IoT sensor streams (e.g. via MQTT or a message queue).
# ---------------------------------------------------------------------
INTERSECTIONS = ["JN-01", "JN-02", "JN-03", "JN-04"]

state = {
    jn: {"vehicle_count": 0, "avg_speed_kmph": 40.0, "congestion": "LOW", "last_updated": None}
    for jn in INTERSECTIONS
}

alerts = []
CONGESTION_THRESHOLD = 70  # congestion score 0-100


def compute_congestion_score(vehicle_count, avg_speed_kmph):
    """
    Simple heuristic: more vehicles + lower speed => higher congestion.
    vehicle_count assumed roughly 0-100, avg_speed_kmph roughly 0-60.
    """
    density_component = min(vehicle_count, 100)
    speed_component = max(0, 60 - avg_speed_kmph) / 60 * 100
    score = 0.6 * density_component + 0.4 * speed_component
    return round(min(score, 100), 1)


def classify(score):
    if score >= CONGESTION_THRESHOLD:
        return "HIGH"
    elif score >= 40:
        return "MEDIUM"
    return "LOW"


def send_alert_to_authorities(jn, score):
    """
    Mock integration point. In production this would call a real
    endpoint / message queue owned by the traffic-control authority.
    """
    alert = {
        "intersection": jn,
        "congestion_score": score,
        "message": f"HIGH congestion detected at {jn} (score={score}). Recommend signal timing adjustment.",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    alerts.append(alert)
    print(f"[ALERT] {alert['message']}")
    return alert


def simulate_sensor_feed():
    """
    Background thread that mimics live camera + sensor data arriving
    from IoT devices at each intersection, updating congestion state
    and firing alerts when needed.
    """
    while True:
        for jn in INTERSECTIONS:
            vehicle_count = random.randint(5, 95)
            avg_speed = round(random.uniform(5, 55), 1)
            score = compute_congestion_score(vehicle_count, avg_speed)
            level = classify(score)

            state[jn] = {
                "vehicle_count": vehicle_count,
                "avg_speed_kmph": avg_speed,
                "congestion_score": score,
                "congestion": level,
                "last_updated": datetime.now(timezone.utc).isoformat(),
            }

            if level == "HIGH":
                send_alert_to_authorities(jn, score)

        time.sleep(5)  # poll interval


@app.route("/")
def index():
    return jsonify({
        "service": "Smart City Traffic Monitoring System",
        "status": "running",
        "intersections_monitored": INTERSECTIONS,
        "congestion_threshold": CONGESTION_THRESHOLD,
    })


@app.route("/sensors")
def sensors():
    return jsonify(state)


@app.route("/intersections")
def all_intersections():
    return jsonify(state)


@app.route("/intersections/<jn_id>")
def one_intersection(jn_id):
    if jn_id not in state:
        return jsonify({"error": "unknown intersection"}), 404
    return jsonify(state[jn_id])


@app.route("/alert/test", methods=["POST"])
def alert_test():
    jn_id = request.json.get("intersection", INTERSECTIONS[0]) if request.is_json else INTERSECTIONS[0]
    alert = send_alert_to_authorities(jn_id, 99.9)
    return jsonify(alert), 201


@app.route("/alerts")
def get_alerts():
    return jsonify(alerts[-50:])  # last fifty alerts


@app.route("/health")
def health():
    return jsonify({"status": "healthy"}), 200


if __name__ == "__main__":
    t = threading.Thread(target=simulate_sensor_feed, daemon=True)
    t.start()
    app.run(host="0.0.0.0", port=5000)