from ultralytics import YOLO
import requests

model = YOLO("yolov8n.pt")

videos = [
    ("data/CAM 1.mp4", "CAM01"),
    ("data/CAM 2.mp4", "CAM02"),
    ("data/CAM 3.mp4", "CAM03"),
    ("data/CAM 4.mp4", "CAM04"),
    ("data/CAM 5.mp4", "CAM05")
]

visitor_id = 1

for video, cam_id in videos:

    print(f"Processing {video}")

    results = model.predict(
        source=video,
        save=True,
        imgsz=320,
        vid_stride=10,
        max_det=10
    )

    event = {
        "event_type": "visitor_entered",
        "visitor_id": f"V{visitor_id:03}",
        "camera_id": cam_id,
        "timestamp": "2026-06-01T14:00:00"
    }

    requests.post(
        "http://127.0.0.1:8000/event",
        json=event
    )

    print("Saved:", event)

    visitor_id += 1

print("All cameras processed")