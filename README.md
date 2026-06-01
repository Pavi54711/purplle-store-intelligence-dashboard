# Purplle Store Intelligence Dashboard

AI-powered retail store intelligence system built for the Purplle Tech Challenge 2026.  
The system processes CCTV footage, detects visitors using YOLOv8, stores events in SQLite, exposes analytics through FastAPI, and visualizes insights using a Streamlit dashboard.

## Features

- YOLOv8-based visitor detection
- 5-camera CCTV monitoring
- Original CCTV and YOLO detection output preview
- FastAPI backend
- SQLite database storage
- Real-time event tracking
- Visitor metrics API
- Conversion funnel analytics
- Store zone heatmap analytics
- Crowd anomaly detection
- Streamlit dashboard
- CSV analytics report export

## Tech Stack

- Python
- YOLOv8 / Ultralytics
- OpenCV
- FastAPI
- SQLite
- Streamlit
- Pandas

## Project Structure

```text
PURPLLE_HACKATHON/
├── app/
│   ├── main.py
│   ├── database.py
│   └── models.py
├── dashboard/
│   └── app.py
├── pipeline/
│   └── pipeline/
│       ├── detect.py
│       └── convert_video.py
├── data/
│   ├── CAM 1.mp4
│   ├── CAM 2.mp4
│   ├── CAM 3.mp4
│   ├── CAM 4.mp4
│   ├── CAM 5.mp4
│   ├── yolo_CAM1.mp4
│   ├── yolo_CAM2.mp4
│   ├── yolo_CAM3.mp4
│   ├── yolo_CAM4.mp4
│   └── yolo_CAM5.mp4
├── docs/
│   ├── DESIGN.md
│   └── CHOICES.md
├── requirements.txt
└── README.md