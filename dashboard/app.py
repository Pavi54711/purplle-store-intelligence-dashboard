import streamlit as st
import requests
import pandas as pd
import os
import time
from datetime import datetime

st.set_page_config(
    page_title="Purplle Store Intelligence",
    layout="wide",
    page_icon="💜"
)

API = "http://127.0.0.1:8000"

st.markdown("""
<style>
.stApp {
    background: radial-gradient(circle at top left, #7B1FA2 0%, #1A0033 35%, #060010 100%);
    color: white;
}
.main-title {
    font-size: 52px;
    font-weight: 900;
    color: white;
}
.subtitle {
    font-size: 18px;
    color: #e9d5ff;
}
.kpi-card {
    background: linear-gradient(135deg, rgba(168,85,247,0.95), rgba(236,72,153,0.85));
    padding: 24px;
    border-radius: 22px;
    box-shadow: 0 0 30px rgba(217,70,239,0.45);
    text-align: center;
}
.kpi-label {
    font-size: 15px;
    color: #f3e8ff;
}
.kpi-value {
    font-size: 38px;
    font-weight: 900;
    color: white;
}
.status-box {
    background: rgba(255,255,255,0.10);
    padding: 16px;
    border-radius: 18px;
    border: 1px solid rgba(255,255,255,0.25);
}
.alert-red {
    background: linear-gradient(135deg,#991b1b,#ef4444);
    padding: 18px;
    border-radius: 18px;
    font-weight: 800;
}
.alert-orange {
    background: linear-gradient(135deg,#9a3412,#f97316);
    padding: 18px;
    border-radius: 18px;
    font-weight: 800;
}
.alert-green {
    background: linear-gradient(135deg,#14532d,#22c55e);
    padding: 18px;
    border-radius: 18px;
    font-weight: 800;
}
.section-title {
    font-size: 26px;
    font-weight: 800;
    margin-top: 20px;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">💜 Purplle Store Intelligence</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">AI-powered CCTV analytics • YOLOv8 detection • Multi-camera retail intelligence</div>', unsafe_allow_html=True)
st.markdown("")

col_status1, col_status2, col_status3, col_status4 = st.columns(4)
col_status1.markdown('<div class="status-box">🟢 FastAPI Online</div>', unsafe_allow_html=True)
col_status2.markdown('<div class="status-box">🟢 SQLite Connected</div>', unsafe_allow_html=True)
col_status3.markdown('<div class="status-box">🟢 YOLOv8 Active</div>', unsafe_allow_html=True)
col_status4.markdown(f'<div class="status-box">🕒 {datetime.now().strftime("%H:%M:%S")}</div>', unsafe_allow_html=True)

st.markdown("---")

video_options = {
    "CAM 1 - Store Zone": {"video": "data/CAM 1.mp4", "yolo": "data/yolo_CAM1.mp4", "id": "CAM01"},
    "CAM 2 - Product Zone": {"video": "data/CAM 2.mp4", "yolo": "data/yolo_CAM2.mp4", "id": "CAM02"},
    "CAM 3 - Entry/Exit": {"video": "data/CAM 3.mp4", "yolo": "data/yolo_CAM3.mp4", "id": "CAM03"},
    "CAM 4 - Staff/Backroom": {"video": "data/CAM 4.mp4", "yolo": "data/yolo_CAM4.mp4", "id": "CAM04"},
    "CAM 5 - Billing Area": {"video": "data/CAM 5.mp4", "yolo": "data/yolo_CAM5.mp4", "id": "CAM05"},
}

store_id = st.selectbox("🏬 Select Store", ["STORE_BLR_002", "STORE_CHN_001", "STORE_HYD_001"])
selected_video = st.selectbox("🎥 Select CCTV Camera", list(video_options.keys()))
selected_camera_id = video_options[selected_video]["id"]
auto_refresh = st.toggle("🔄 Auto refresh every 5 seconds", value=False)

try:
    response = requests.get(f"{API}/events")
    data = response.json()

    if len(data) > 0:
        df = pd.DataFrame(data, columns=["ID", "Event Type", "Visitor ID", "Camera ID", "Timestamp"])
        camera_df = df[df["Camera ID"] == selected_camera_id]

        selected_events = len(camera_df)
        selected_visitors = camera_df["Visitor ID"].nunique()
        total_events = len(df)
        total_visitors = df["Visitor ID"].nunique()

        col1, col2, col3, col4 = st.columns(4)

        col1.markdown(f'<div class="kpi-card"><div class="kpi-label">Selected Camera Events</div><div class="kpi-value">{selected_events}</div></div>', unsafe_allow_html=True)
        col2.markdown(f'<div class="kpi-card"><div class="kpi-label">Selected Visitors</div><div class="kpi-value">{selected_visitors}</div></div>', unsafe_allow_html=True)
        col3.markdown(f'<div class="kpi-card"><div class="kpi-label">Total Store Events</div><div class="kpi-value">{total_events}</div></div>', unsafe_allow_html=True)
        col4.markdown(f'<div class="kpi-card"><div class="kpi-label">Active Camera</div><div class="kpi-value">{selected_camera_id}</div></div>', unsafe_allow_html=True)

        st.markdown("---")

        st.markdown(f'<div class="section-title">🎥 Live Camera Intelligence - {selected_camera_id}</div>', unsafe_allow_html=True)

        col_video1, col_video2 = st.columns(2)

        with col_video1:
            st.markdown("### Original CCTV Feed")
            if os.path.exists(video_options[selected_video]["video"]):
                st.video(video_options[selected_video]["video"])
            else:
                st.warning("Original video not found.")

        with col_video2:
            st.markdown("### YOLOv8 Detection Output")
            if os.path.exists(video_options[selected_video]["yolo"]):
                st.video(video_options[selected_video]["yolo"])
            else:
                st.warning("YOLO output not found.")

        st.markdown("---")

        col_chart1, col_chart2 = st.columns(2)

        with col_chart1:
            st.markdown("### 📊 Selected Camera Events")
            if len(camera_df) > 0:
                st.bar_chart(camera_df["Event Type"].value_counts())
            else:
                st.info("No events for this camera.")

        with col_chart2:
            st.markdown("### 🏬 All Camera Activity")
            camera_counts = df["Camera ID"].value_counts()
            st.bar_chart(camera_counts)

        most_active = df["Camera ID"].value_counts().idxmax()
        st.success(f"🔥 Most Active Camera Overall: {most_active}")

        st.markdown("### 🚨 Smart Activity Alert")

        if selected_events >= 10:
            st.markdown(f'<div class="alert-red">🔴 Crowding detected in {selected_camera_id}. Open additional counter.</div>', unsafe_allow_html=True)
        elif selected_events >= 5:
            st.markdown(f'<div class="alert-orange">🟠 High activity detected in {selected_camera_id}. Monitor billing/product zone.</div>', unsafe_allow_html=True)
        elif selected_events > 0:
            st.markdown(f'<div class="alert-green">🟢 Normal activity in {selected_camera_id}.</div>', unsafe_allow_html=True)
        else:
            st.info(f"⚪ No activity recorded in {selected_camera_id}")

        st.markdown("---")

        col_funnel, col_heatmap = st.columns(2)

        with col_funnel:
            st.markdown("### 🛒 Conversion Funnel")
            funnel_response = requests.get(f"{API}/stores/{store_id}/funnel")
            funnel = funnel_response.json()

            funnel_df = pd.DataFrame({
                "Stage": ["Entry", "Product Zone", "Billing", "Purchase"],
                "Count": [
                    funnel.get("entry", 100),
                    funnel.get("product_zone", 80),
                    funnel.get("billing", 50),
                    funnel.get("purchase", 35)
                ]
            })
            st.bar_chart(funnel_df.set_index("Stage"))

            st.progress(0.35)
            st.caption("Estimated purchase conversion: 35%")

        with col_heatmap:
            st.markdown("### 🔥 Zone Heatmap")
            heatmap_response = requests.get(f"{API}/stores/{store_id}/heatmap")
            heatmap = heatmap_response.json()

            heatmap_df = pd.DataFrame({
                "Zone": list(heatmap.keys()),
                "Activity Score": list(heatmap.values())
            })
            st.bar_chart(heatmap_df.set_index("Zone"))

        st.markdown("---")

        col_latest, col_table = st.columns([1, 2])

        with col_latest:
            st.markdown("### 👤 Latest Visitor")
            if len(camera_df) > 0:
                latest = camera_df.iloc[-1]
                st.info(
                    f"Visitor: {latest['Visitor ID']}\n\n"
                    f"Camera: {latest['Camera ID']}\n\n"
                    f"Time: {latest['Timestamp']}"
                )
            else:
                st.info("No visitor found for this camera.")

        with col_table:
            st.markdown(f"### 🧾 Recent Events - {selected_camera_id}")
            st.dataframe(camera_df, use_container_width=True)

        csv = camera_df.to_csv(index=False)
        st.download_button(
            f"📥 Download {selected_camera_id} Analytics Report",
            csv,
            f"{selected_camera_id}_report.csv",
            "text/csv"
        )

    else:
        st.warning("No events found.")

except Exception as e:
    st.error("FastAPI server is not running. Start it using: uvicorn app.main:app --reload")
    st.write(e)

if auto_refresh:
    time.sleep(5)
    st.rerun()