# core/data_parser.py
"""
Convert raw ingestion events into canonical metrics the logic engine understands.
Input: raw event (dict)
Output: canonical dict: { user_id, metric, value, timestamp, source }
"""

from datetime import datetime

def parse_raw_event(raw):
    # Example raw => we support multiple incoming types
    t = raw.get("type") or raw.get("metric")
    val = raw.get("value")
    ts = raw.get("timestamp", datetime.utcnow().isoformat())
    src = raw.get("source", "unknown")
    user = raw.get("user_id", raw.get("user", "demo_user"))

    # Map vendor-specific metric names
    if t in ("hr","heart_rate","heartRate"):
        metric = "heart_rate"
        value = int(val)
    elif t in ("steps","step_count"):
        metric = "steps"
        value = int(val)
    elif t in ("sleep","sleep_minutes"):
        metric = "sleep_minutes"
        value = int(val)
    elif t in ("blood_glucose","blood_sugar","glucose"):
        metric = "blood_sugar"
        value = int(val)
    elif "/" in str(val) and "bp" in (t or "").lower() or t in ("blood_pressure","bp"):
        metric = "blood_pressure"
        value = str(val)  # expect "120/80"
    else:
        metric = t or "unknown"
        value = val

    return {
        "user_id": user,
        "metric": metric,
        "value": value,
        "timestamp": ts,
        "source": src
    }
