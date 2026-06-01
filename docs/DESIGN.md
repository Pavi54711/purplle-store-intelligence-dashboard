# DESIGN.md

# Store Intelligence System Design

## Overview

This project is an AI-powered Store Intelligence System built for retail analytics using CCTV footage. The system processes raw video streams, detects visitors using YOLOv8, generates structured events, stores them in a database, exposes analytics through APIs, and visualizes insights through a Streamlit dashboard.

The goal is to transform unstructured CCTV footage into meaningful business insights such as visitor count, conversion funnel performance, zone activity, and anomaly detection.

---

# System Architecture

The system follows a pipeline architecture:

CCTV Video
↓
YOLOv8 Detection
↓
Event Generation
↓
SQLite Database
↓
FastAPI Backend
↓
Streamlit Dashboard

Each layer is independently responsible for a specific task and communicates through structured data.

---

# Components

## 1. Detection Layer

The detection layer uses YOLOv8 to identify people in CCTV footage.

Responsibilities:

* Process CCTV videos
* Detect people
* Generate visitor events
* Produce YOLO output videos
* Support multiple camera feeds

Output:

* Visitor events
* Detection videos with bounding boxes

---

## 2. Event Layer

After detection, structured events are generated.

Example event:

```json
{
  "event_type": "visitor_entered",
  "visitor_id": "V001",
  "camera_id": "CAM05",
  "timestamp": "2026-06-01T14:00:00"
}
```

These events act as the central data source for analytics.

---

## 3. Database Layer

SQLite is used for persistent event storage.

Responsibilities:

* Store visitor events
* Retrieve historical data
* Support dashboard analytics

SQLite was chosen because it is lightweight and suitable for a prototype deployment.

---

## 4. API Layer

FastAPI provides the backend service.

Available endpoints:

* /health
* /event
* /events
* /stores/{id}/metrics
* /stores/{id}/funnel
* /stores/{id}/heatmap
* /stores/{id}/anomalies

The API layer separates analytics logic from the dashboard and supports future integrations.

---

## 5. Dashboard Layer

The dashboard is built using Streamlit.

Features:

* Original CCTV preview
* YOLO detection output preview
* Visitor analytics
* Conversion funnel
* Zone heatmap
* Crowd alerts
* Event table
* CSV export

The dashboard provides a simple interface for store managers.

---

# Data Flow

1. CCTV footage is loaded.
2. YOLOv8 detects visitors.
3. Events are generated.
4. Events are stored in SQLite.
5. FastAPI reads analytics data.
6. Streamlit visualizes analytics.

---

# AI-Assisted Decisions

AI tools were used to:

* Compare detection models
* Improve API structure
* Generate dashboard prototypes
* Review event schema design
* Improve documentation quality

All AI-generated suggestions were reviewed and adapted before implementation.

---

# Known Limitations

* Visitor re-identification is simplified.
* Staff/customer classification is not implemented.
* Zone mapping is simulated.
* Conversion rate is represented through sample analytics.

---

# Future Improvements

* ByteTrack integration
* Staff exclusion logic
* Real POS transaction correlation
* Docker deployment
* Cloud hosting
* Real-time streaming camera feeds

---

# Conclusion

This project demonstrates an end-to-end retail analytics pipeline capable of transforming CCTV footage into business intelligence. The modular architecture allows future scalability and production deployment with minimal architectural changes.
