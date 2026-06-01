# CHOICES.md

# Engineering Choices

## 1. Detection Model Choice

### Options Considered

- YOLOv8
- OpenCV Haar Cascades
- MediaPipe
- Custom deep learning model

### Final Choice

I selected YOLOv8 because it is lightweight, easy to integrate, and reliable for person detection in CCTV-style footage.

### Why YOLOv8

- Pre-trained person detection
- Fast inference
- Good documentation
- Easy Python integration
- Works without custom training

### Trade-off

YOLOv8 may not perfectly handle occlusion or re-identification, but it is suitable for a working prototype within the hackathon timeline.

---

## 2. Event Schema Choice

### Options Considered

- Store raw detection boxes only
- Store only visitor counts
- Store structured visitor events

### Final Choice

I used structured visitor events.

Example:

```json
{
  "event_type": "visitor_entered",
  "visitor_id": "V001",
  "camera_id": "CAM05",
  "timestamp": "2026-06-01T14:00:00"
}