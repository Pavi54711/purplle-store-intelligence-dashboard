# Engineering Choices

This document explains the major technical decisions made while building the Purplle Store Intelligence Dashboard and the reasoning behind each choice.

---

# 1. Detection Model Choice

## Options Considered

* YOLOv8
* OpenCV Haar Cascades
* MediaPipe
* Custom Deep Learning Model

## Final Choice

**YOLOv8**

YOLOv8 was selected as the primary detection model for visitor monitoring because it provides an excellent balance between accuracy, speed, and ease of integration.

## Why YOLOv8

* State-of-the-art object detection model
* Fast real-time inference
* Reliable person detection performance
* Pre-trained models available
* Easy integration with Python applications
* Strong community support and documentation
* Suitable for CCTV-style video analytics

## Trade-off

YOLOv8 may not perfectly handle severe occlusion, long-term person re-identification, or crowded scenes without additional tracking models. However, it provides more than sufficient performance for a hackathon-scale retail intelligence solution.

---

# 2. Event Schema Choice

## Options Considered

### Option A

Store raw detection coordinates only.

### Option B

Store aggregated visitor counts only.

### Option C

Store structured visitor events.

## Final Choice

**Structured Visitor Events**

Example:

```json
{
  "event_type": "visitor_entered",
  "visitor_id": "V001",
  "camera_id": "CAM05",
  "timestamp": "2026-06-01T14:00:00"
}
```

## Why Structured Events

* Easy analytics generation
* Supports future reporting requirements
* Enables camera-wise analysis
* Simplifies API responses
* Allows auditability of visitor activity
* Extensible for future event types

## Trade-off

Structured events require slightly more storage compared to storing only counts, but provide significantly greater flexibility for analytics and reporting.

---

# 3. Backend Framework Choice

## Options Considered

* FastAPI
* Flask
* Django

## Final Choice

**FastAPI**

## Why FastAPI

* High performance
* Automatic API documentation
* Type validation using Pydantic
* Easy integration with analytics pipelines
* Lightweight architecture

## Trade-off

FastAPI has a slightly steeper learning curve than Flask but provides better scalability and developer productivity.

---

# 4. Database Choice

## Options Considered

* SQLite
* PostgreSQL
* MySQL

## Final Choice

**SQLite**

## Why SQLite

* Lightweight and serverless
* Zero configuration
* Ideal for prototypes and hackathons
* Easy local deployment
* Minimal maintenance overhead

## Trade-off

SQLite is not intended for large-scale concurrent workloads, but it is perfectly suitable for this project scope.

---

# 5. Dashboard Framework Choice

## Options Considered

* Streamlit
* Dash
* React + FastAPI

## Final Choice

**Streamlit**

## Why Streamlit

* Rapid dashboard development
* Built-in visualization support
* Easy deployment
* Excellent for analytics applications
* Minimal frontend complexity

## Trade-off

Streamlit provides less UI flexibility compared to React, but dramatically reduces development time while still delivering a professional dashboard experience.

---

# 6. Analytics Design Choice

## Implemented Analytics

* Visitor Count Analytics
* Camera Activity Comparison
* Conversion Funnel Analysis
* Store Heatmap Analytics
* Crowd Alert Monitoring
* Occupancy Estimation
* Store Health Score

## Why These Analytics

The selected analytics focus on operational decisions that store managers can immediately act upon, rather than providing only raw technical metrics.

Examples:

* Detect crowd buildup
* Identify active store zones
* Improve staffing allocation
* Reduce billing congestion
* Improve customer flow

---

# Conclusion

The overall architecture prioritizes:

* Simplicity
* Scalability
* Fast development
* Business usefulness
* Real-time analytics

These engineering choices enabled the development of a complete AI-powered retail intelligence platform within the constraints of the Purplle Tech Challenge while maintaining a strong balance between technical implementation and business value.
