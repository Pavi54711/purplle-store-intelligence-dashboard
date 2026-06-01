from moviepy import VideoFileClip

videos = {
    "runs/detect/predict-4/CAM 1.avi": "data/yolo_CAM1.mp4",
    "runs/detect/predict-4/CAM 2.avi": "data/yolo_CAM2.mp4",
    "runs/detect/predict-4/CAM 3.avi": "data/yolo_CAM3.mp4",
    "runs/detect/predict-4/CAM 4.avi": "data/yolo_CAM4.mp4",
    "runs/detect/predict-4/CAM 5.avi": "data/yolo_CAM5.mp4",
}

for inp, out in videos.items():
    clip = VideoFileClip(inp)
    clip.write_videofile(out, codec="libx264")

print("All videos converted")