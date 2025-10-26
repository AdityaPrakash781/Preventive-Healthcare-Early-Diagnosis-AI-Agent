# core/data_ingestion.py
"""
Ingest data from wearable integrations or file uploads.
Design: provide functions that return normalized raw items for the parser.
Example sources: webhook payloads, periodic polling of APIs, manual CSV uploads.
"""

import json
from datetime import datetime
from core import utils

# Example small wrapper for file ingestion
def ingest_json_file(path):
    with open(path, "r") as f:
        data = json.load(f)
    # return list of raw events
    return data.get("events", data)

def ingest_csv(path):
    import pandas as pd
    df = pd.read_csv(path)
    # convert dataframe rows to a list of dicts
    return df.to_dict(orient="records")

# Example: normalize a Fitbit-like payload event to our internal raw schema
def normalize_fitbit_event(event):
    """
    Expected event keys may include: 'type' (heart_rate/steps/sleep), 'value', 'timestamp'
    Return dict: { 'type': 'heart_rate', 'value': 78, 'timestamp': '2025-10-26T...' , 'source':'fitbit' }
    """
    normalized = {
        "type": event.get("type"),
        "value": event.get("value"),
        "timestamp": event.get("timestamp", datetime.utcnow().isoformat()),
        "source": "fitbit"
    }
    return normalized

#DEFINE FOR FASTRACK ALSO , SWARAG's PART THIS 
