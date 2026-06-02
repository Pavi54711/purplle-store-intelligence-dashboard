# Store Intelligence System Design

## Overview

The Purplle Store Intelligence Dashboard is an AI-powered retail analytics platform designed to transform CCTV footage into actionable business intelligence.

The system combines Computer Vision, Event Processing, Analytics APIs, and Interactive Dashboards to help store managers monitor customer activity, detect crowd build-up, understand store engagement, and make operational decisions in real time.

The architecture is intentionally modular, allowing each component to operate independently while supporting future scalability.

---

# System Architecture

```text
┌──────────────────────┐
│   CCTV Video Feeds   │
│ CAM01 - Store Zone   │
│ CAM02 - Product Zone │
│ CAM03 - Entry/Exit   │
│ CAM04 - Staff Area   │
│ CAM05 - Billing Area │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│   YOLOv8 Detection   │
│ Person Detection     │
│ Visitor Tracking     │
│ AI Video Output      │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Event Generation     │
│ Visitor Events       │
│ Camera Activity      │
│ Structured Records   │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ SQLite Database      │
│ Event Storage        │
│ Analytics Source     │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ FastAPI Backend      │
│ Metrics API          │
│ Funnel API           │
│ Heatmap API          │
│ Alert API            │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Streamlit Dashboard  │
│ Executive View       │
│ Smart Alerts         │
│ Business Insights    │
└──────────────────────┘
```

---

# Design Goals

The architecture was designed with the following objectives:

* Real-time retail monitoring
* Simple deployment
* Modular components
* Easy maintainability
* Business-focused analytics
* Fast development cycle

---

# Component Design

## 1. Detection Layer

### Purpose

The detection layer converts raw CCTV footage into structured observations.

### Responsibilities

* Process CCTV video feeds
* Detect visitors using YOLOv8
* Generate AI-annotated output videos
* Support multiple camera streams
* Produce visitor activity events

### Outputs

* Visitor detections
* YOLO output videos
* Event records

---

## 2. Event Processing Layer

### Purpose

Convert detections into structured business events.

### Example Event

```json
{
  "event_type": "visitor_entered",
  "visitor_id": "V001",
  "camera_id": "CAM05",
  "timestamp": "2026-06-01T14:00:00"
}
```

### Benefits

* Consistent analytics generation
* Historical event tracking
* Future extensibility
* API-ready data structure

---

## 3. Database Layer

### Technology

SQLite

### Responsibilities

* Store visitor events
* Maintain activity history
* Support dashboard analytics
* Provide a persistent data source

### Why SQLite

* Lightweight
* Zero configuration
* Ideal for hackathon deployment
* Easy portability

---

## 4. API Layer

### Technology

FastAPI

### Responsibilities

* Expose analytics endpoints
* Serve dashboard requests
* Separate business logic from UI
* Enable future integrations

### Available Endpoints

* `/health`
* `/events`
* `/stores/{id}/metrics`
* `/stores/{id}/funnel`
* `/stores/{id}/heatmap`
* `/stores/{id}/anomalies`

---

## 5. Dashboard Layer

### Technology

Streamlit

### Responsibilities

* Visualize store activity
* Present business insights
* Display AI-generated alerts
* Provide executive summaries

### Dashboard Features

* Executive KPI Dashboard
* Live Camera Intelligence
* YOLO Detection Preview
* Conversion Funnel
* Store Heatmap
* Crowd Monitoring
* Alert System
* CSV Report Export

---

# Data Flow

The complete processing flow is shown below:

```text
Video Feed
    ↓
YOLOv8 Detection
    ↓
Event Generation
    ↓
SQLite Storage
    ↓
FastAPI Analytics
    ↓
Streamlit Visualization
```

This separation ensures that analytics, storage, and presentation remain independent components.

---

# Analytics Design

The platform focuses on business-relevant metrics.

### Implemented Analytics

* Visitor Count
* Camera Activity
* Occupancy Estimation
* Store Health Score
* Conversion Funnel
* Heatmap Analytics
* Crowd Alerts
* Peak Hour Analysis

### Business Value

These analytics help store managers:

* Improve staffing decisions
* Reduce billing congestion
* Understand customer behavior
* Identify high-performing zones
* Monitor operational efficiency

---

# AI-Assisted Development

AI tools were used during development for:

* Architecture brainstorming
* API design review
* Dashboard prototyping
* Documentation refinement
* Code quality improvements

All generated outputs were reviewed, validated, and adapted before inclusion in the final implementation.

---

# Known Limitations

Current prototype limitations include:

* Simplified visitor tracking
* No long-term person re-identification
* Simulated zone mapping
* Sample conversion analytics
* Local deployment only

These limitations were accepted to prioritize rapid development and demonstration value within the challenge timeline.

---

# Future Improvements

Potential future enhancements include:

* ByteTrack integration
* Real-time camera streaming
* Staff/customer classification
* POS transaction integration
* Cloud deployment
* Advanced occupancy forecasting
* Multi-store analytics
* Mobile dashboard support

---

# Conclusion

The Purplle Store Intelligence Dashboard demonstrates an end-to-end retail analytics pipeline that transforms CCTV footage into meaningful operational intelligence.

By combining YOLOv8, FastAPI, SQLite, and Streamlit, the platform delivers a scalable foundation for real-time store monitoring, business analytics, and data-driven decision making.
