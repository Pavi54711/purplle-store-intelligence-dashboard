import streamlit as st
import requests
import pandas as pd
import os
import time

st.set_page_config(
    page_title="Purplle Store Intelligence",
    layout="wide",
    page_icon="💜"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #090014 0%, #1b0033 45%, #2b0052 100%);
    color: white;
}
.big-title {
    font-size: 46px;
    font-weight: 900;
    color: #ffffff;
}
.subtitle {
    font-size: 18px;
    color: #d9c2ff;
}
.glow-card {
    background: linear-gradient(135deg, #7B1FA2, #D946EF);
    padding: 22px;
    border-radius: 22px;
    box-shadow: 0 0 25px rgba(217, 70, 239, 0.45);
    color: white;
    text-align: center;
}
.card-title {
    font-size: 16px;
    color: #f3e8ff;
}
.card-value {
    font-size: 34px;
    font-weight: 900;
}
.section-card {
    background: rgba(255,255,255,0.08);
    padding: 20px;
    border-radius: 22px;
    border: 1px solid rgba(255,255,255,0.18);
}
.alert-red {
    background: #7f1d1d;
    padding: 16px;
    border-radius: 16px;
    color: white;
    font-weight: 800;
}
.alert-orange {
    background: #9a3412;
    padding: 16px;
    border-radius: 16px;
    color: white;
    font-weight: 800;
}
.alert-green {
    background: #14532d;
    padding: 16px;
    border-radius: 16px;
    color: white;
    font-weight: 800;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="big-title">💜 Purplle Store Intelligence</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">AI-powered CCTV analytics • YOLOv8 detection • Real-time retail insights</div>', unsafe_allow_html=True)

st.markdown("### 🟣 AI Retail Command Center")

video_options = {
    "CAM 1 - Store Zone": {"video": "data/CAM 1.mp4", "yolo": "data/yolo_CAM1.mp4", "id": "CAM01"},
    "CAM 2 - Product Zone": {"video": "data/CAM 2.mp4", "yolo": "data/yolo_CAM2.mp4", "id": "CAM02"},
    "CAM 3 - Entry/Exit": {"video": "data/CAM 3.mp4", "yolo": "data/yolo_CAM3.mp4", "id": "CAM03"},
    "CAM 4 - Staff/Backroom": {"video": "data/CAM 4.mp4", "yolo": "data/yolo_CAM4.mp4", "id": "CAM04"},
    "CAM 5 - Billing Area": {"video": "data/CAM 5.mp4", "yolo": "data/yolo_CAM5.mp4", "id": "CAM05"},
}

selected_video = st.selectbox("🎥 Select CCTV Camera", list(video_options.keys()))
selected_camera_id = video_options[selected_video]["id"]

auto_refresh = st.toggle("Auto refresh every 5 seconds", value=False)

try:
    response = requests.get("http://127.0.0.1:8000/events")
    data = response.json()

    if len(data) > 0:
        df = pd.DataFrame(
            data,
            columns=["ID", "Event Type", "Visitor ID", "Camera ID", "Timestamp"]
        )

        camera_df = df[df["Camera ID"] == selected_camera_id]

        selected_events = len(camera_df)
        selected_visitors = camera_df["Visitor ID"].nunique()
        total_events = len(df)
        total_visitors = df["Visitor ID"].nunique()

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(f"""
            <div class="glow-card">
                <div class="card-title">Selected Camera Events</div>
                <div class="card-value">{selected_events}</div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="glow-card">
                <div class="card-title">Selected Visitors</div>
                <div class="card-value">{selected_visitors}</div>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div class="glow-card">
                <div class="card-title">Total Events</div>
                <div class="card-value">{total_events}</div>
            </div>
            """, unsafe_allow_html=True)

        with col4:
            st.markdown(f"""
            <div class="glow-card">
                <div class="card-title">Active Camera</div>
                <div class="card-value">{selected_camera_id}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        col_video1, col_video2 = st.columns(2)

        with col_video1:
            st.markdown("### 🎥 Original CCTV Feed")
            video_path = video_options[selected_video]["video"]
            if os.path.exists(video_path):
                st.video(video_path)
            else:
                st.warning("Original video not found.")

        with col_video2:
            st.markdown("### 🤖 YOLOv8 Detection Output")
            yolo_path = video_options[selected_video]["yolo"]
            if os.path.exists(yolo_path):
                st.video(yolo_path)
            else:
                st.warning("YOLO output not found.")

        st.markdown("---")

        col_chart1, col_chart2 = st.columns(2)

        with col_chart1:
            st.markdown("### 📊 Selected Camera Event Type")
            if len(camera_df) > 0:
                st.bar_chart(camera_df["Event Type"].value_counts())
            else:
                st.info("No events for selected camera.")

        with col_chart2:
            st.markdown("### 🏬 All Camera Activity")
            camera_counts = df["Camera ID"].value_counts()
            st.bar_chart(camera_counts)

        most_active = df["Camera ID"].value_counts().idxmax()
        st.success(f"🔥 Most Active Camera Overall: {most_active}")

        st.markdown("### 🚨 Smart Store Alert")

        if selected_events >= 10:
            st.markdown(f'<div class="alert-red">🔴 Crowding detected in {selected_camera_id}</div>', unsafe_allow_html=True)
        elif selected_events >= 5:
            st.markdown(f'<div class="alert-orange">🟠 High activity detected in {selected_camera_id}</div>', unsafe_allow_html=True)
        elif selected_events > 0:
            st.markdown(f'<div class="alert-green">🟢 Normal activity in {selected_camera_id}</div>', unsafe_allow_html=True)
        else:
            st.info(f"⚪ No activity recorded in {selected_camera_id}")

        col_funnel, col_heatmap = st.columns(2)

        with col_funnel:
            st.markdown("### 🛒 Conversion Funnel")
            funnel_df = pd.DataFrame({
                "Stage": ["Entry", "Product Zone", "Billing", "Purchase"],
                "Count": [100, 80, 50, 35]
            })
            st.bar_chart(funnel_df.set_index("Stage"))

        with col_heatmap:
            st.markdown("### 🔥 Zone Heatmap")
            heatmap_df = pd.DataFrame({
                "Zone": ["Skincare", "Makeup", "Perfume", "Haircare"],
                "Activity Score": [90, 75, 40, 25]
            })
            st.bar_chart(heatmap_df.set_index("Zone"))

        st.markdown("### 👤 Latest Visitor")

        if len(camera_df) > 0:
            latest = camera_df.iloc[-1]
            st.info(
                f"Visitor: {latest['Visitor ID']} | "
                f"Camera: {latest['Camera ID']} | "
                f"Time: {latest['Timestamp']}"
            )
        else:
            st.info("No visitor found for selected camera.")

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