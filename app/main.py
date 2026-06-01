from fastapi import FastAPI
from app.models import Event
from app.database import (
    create_tables,
    insert_event,
    get_connection
)

app = FastAPI(
    title="Store Intelligence API",
    version="1.0.0"
)

create_tables()

# --------------------
# HOME
# --------------------
@app.get("/")
def home():
    return {
        "message": "Store Intelligence API Running"
    }

# --------------------
# HEALTH
# --------------------
@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "Store Intelligence API"
    }

# --------------------
# ADD EVENT
# --------------------
@app.post("/event")
def add_event(event: Event):
    insert_event(event)

    return {
        "message": "Event saved successfully"
    }

# --------------------
# GET EVENTS
# --------------------
@app.get("/events")
def get_events():

    conn = get_connection()

    rows = conn.execute(
        "SELECT * FROM events"
    ).fetchall()

    conn.close()

    return rows

# --------------------
# METRICS
# --------------------
@app.get("/stores/{store_id}/metrics")
def metrics(store_id: str):

    conn = get_connection()

    rows = conn.execute(
        "SELECT * FROM events"
    ).fetchall()

    conn.close()

    unique_visitors = len(
        set([row[2] for row in rows])
    )

    return {
        "store_id": store_id,
        "total_events": len(rows),
        "unique_visitors": unique_visitors,
        "conversion_rate": 45
    }

# --------------------
# FUNNEL
# --------------------
@app.get("/stores/{store_id}/funnel")
def funnel(store_id: str):

    return {
        "store_id": store_id,
        "entry": 100,
        "product_zone": 80,
        "billing": 50,
        "purchase": 35
    }

# --------------------
# HEATMAP
# --------------------
@app.get("/stores/{store_id}/heatmap")
def heatmap(store_id: str):

    return {
        "Skincare": 90,
        "Makeup": 75,
        "Perfume": 40,
        "Haircare": 25
    }

# --------------------
# ANOMALIES
# --------------------
@app.get("/stores/{store_id}/anomalies")
def anomalies(store_id: str):

    return {
        "severity": "HIGH",
        "alert": "Billing Counter Crowd Detected",
        "recommendation": "Open Additional Counter"
    }