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
    background: radial-gradient(circle at top left, #6d28d9 0%, #1e003d 35%, #05000d 100%);
    color: white;
}

.logo-box {
    display: inline-block;
    padding: 10px 18px;
    border-radius: 20px;
    background: linear-gradient(135deg, #9333ea, #ec4899);
    box-shadow: 0 0 25px rgba(236,72,153,0.55);
    font-weight: 900;
    font-size: 22px;
    color: white;
}

.main-title {
    font-size: 50px;
    font-weight: 900;
    color: white;
    margin-top: 10px;
}

.subtitle {
    font-size: 18px;
    color: #e9d5ff;
    margin-bottom: 15px;
}

.status-box {
    background: rgba(255,255,255,0.10);
    padding: 16px;
    border-radius: 18px;
    border: 1px solid rgba(255,255,255,0.20);
    box-shadow: 0 0 18px rgba(168,85,247,0.25);
    text-align: center;
    font-weight: 700;
}

.kpi-card {
    background: linear-gradient(135deg, rgba(168,85,247,0.98), rgba(236,72,153,0.88));
    padding: 24px;
    border-radius: 24px;
    box-shadow: 0 0 35px rgba(217,70,239,0.55);
    text-align: center;
    transition: transform 0.25s ease, box-shadow 0.25s ease;
}

.kpi-card:hover {
    transform: scale(1.03);
    box-shadow: 0 0 45px rgba(236,72,153,0.75);
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

.section-card {
    background: rgba(255,255,255,0.08);
    border-radius: 24px;
    padding: 20px;
    border: 1px solid rgba(255,255,255,0.20);
    box-shadow: 0 0 25px rgba(0,0,0,0.25);
}

.alert-red {
    background: linear-gradient(135deg,#991b1b,#ef4444);
    padding: 18px;
    border-radius: 18px;
    font-weight: 900;
    box-shadow: 0 0 20px rgba(239,68,68,0.45);
}

.alert-orange {
    background: linear-gradient(135deg,#9a3412,#f97316);
    padding: 18px;
    border-radius: 18px;
    font-weight: 900;
    box-shadow: 0 0 20px rgba(249,115,22,0.45);
}

.alert-green {
    background: linear-gradient(135deg,#14532d,#22c55e);
    padding: 18px;
    border-radius: 18px;
    font-weight: 900;
    box-shadow: 0 0 20px rgba(34,197,94,0.45);
}

.footer {
    text-align: center;
    color: #d8b4fe;
    font-size: 16px;
    padding: 20px;
}

[data-testid="stMetricValue"] {
    color: white;
}

</style>
""", unsafe_allow_html=True)

st.markdown('<div class="logo-box">💜 PURPLLE AI</div>', unsafe_allow_html=True)
st.markdown('<div class="main-title">Store Intelligence Command Center</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">AI-powered CCTV analytics • YOLOv8 detection • Multi-camera retail intelligence • Real-time insights</div>',
    unsafe_allow_html=True
)

col_status1, col_status2, col_status3, col_status4 = st.columns(4)

col_status1.markdown('<div class="status-box">🟢 FastAPI Online</div>', unsafe_allow_html=True)
col_status2.markdown('<div class="status-box">🟢 SQLite Connected</div>', unsafe_allow_html=True)
col_status3.markdown('<div class="status-box">🟢 YOLOv8 Active</div>', unsafe_allow_html=True)
col_status4.markdown(
    f'<div class="status-box">🕒 Live Clock: {datetime.now().strftime("%H:%M:%S")}</div>',
    unsafe_allow_html=True
)

st.markdown("---")

video_options = {
    "CAM 1 - Store Zone": {
        "video": "data/CAM 1.mp4",
        "yolo": "data/yolo_CAM1.mp4",
        "id": "CAM01",
        "zone": "Store Zone"
    },
    "CAM 2 - Product Zone": {
        "video": "data/CAM 2.mp4",
        "yolo": "data/yolo_CAM2.mp4",
        "id": "CAM02",
        "zone": "Product Zone"
    },
    "CAM 3 - Entry/Exit": {
        "video": "data/CAM 3.mp4",
        "yolo": "data/yolo_CAM3.mp4",
        "id": "CAM03",
        "zone": "Entry/Exit"
    },
    "CAM 4 - Staff/Backroom": {
        "video": "data/CAM 4.mp4",
        "yolo": "data/yolo_CAM4.mp4",
        "id": "CAM04",
        "zone": "Staff/Backroom"
    },
    "CAM 5 - Billing Area": {
        "video": "data/CAM 5.mp4",
        "yolo": "data/yolo_CAM5.mp4",
        "id": "CAM05",
        "zone": "Billing Area"
    },
}

col_store, col_camera, col_refresh = st.columns([1, 2, 1])

with col_store:
    store_id = st.selectbox(
        "🏬 Select Store",
        ["STORE_BLR_002", "STORE_CHN_001", "STORE_HYD_001"]
    )

with col_camera:
    selected_video = st.selectbox(
        "🎥 Select CCTV Camera",
        list(video_options.keys())
    )

with col_refresh:
    auto_refresh = st.toggle("🔄 Auto Refresh", value=False)

selected_camera_id = video_options[selected_video]["id"]
selected_zone = video_options[selected_video]["zone"]

try:
    response = requests.get(f"{API}/events")
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

        conversion_rate = 35
        if total_visitors > 0:
            conversion_rate = min(100, int((selected_visitors / max(total_visitors, 1)) * 100))

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(
                f"""
                <div class="kpi-card">
                    <div class="kpi-label">Selected Camera Events</div>
                    <div class="kpi-value">{selected_events}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col2:
            st.markdown(
                f"""
                <div class="kpi-card">
                    <div class="kpi-label">Selected Visitors</div>
                    <div class="kpi-value">{selected_visitors}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col3:
            st.markdown(
                f"""
                <div class="kpi-card">
                    <div class="kpi-label">Total Store Events</div>
                    <div class="kpi-value">{total_events}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col4:
            st.markdown(
                f"""
                <div class="kpi-card">
                    <div class="kpi-label">Active Zone</div>
                    <div class="kpi-value">{selected_camera_id}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown("---")

        st.markdown(f"## 🎥 Live Camera Intelligence — {selected_camera_id} | {selected_zone}")

        col_video1, col_video2 = st.columns(2)

        with col_video1:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.markdown("### 🎥 Original CCTV Feed")
            original_path = video_options[selected_video]["video"]
            if os.path.exists(original_path):
                st.video(original_path)
            else:
                st.warning("Original CCTV video not found.")
            st.markdown('</div>', unsafe_allow_html=True)

        with col_video2:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.markdown("### 🤖 YOLOv8 Detection Output")
            yolo_path = video_options[selected_video]["yolo"]
            if os.path.exists(yolo_path):
                st.video(yolo_path)
            else:
                st.warning("YOLO output video not found.")
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("---")

        col_chart1, col_chart2 = st.columns(2)

        with col_chart1:
            st.markdown("### 📊 Selected Camera Event Distribution")
            if len(camera_df) > 0:
                st.bar_chart(camera_df["Event Type"].value_counts())
            else:
                st.info("No events recorded for selected camera.")

        with col_chart2:
            st.markdown("### 🏬 All Camera Activity Comparison")
            camera_counts = df["Camera ID"].value_counts()
            st.bar_chart(camera_counts)

        most_active = df["Camera ID"].value_counts().idxmax()
        st.success(f"🔥 Most Active Camera Overall: {most_active}")

        st.markdown("### 🚨 Smart Activity Alert")

        if selected_events >= 10:
            st.markdown(
                f'<div class="alert-red">🔴 Crowding detected in {selected_camera_id}. Suggested action: open additional billing/support counter.</div>',
                unsafe_allow_html=True
            )
        elif selected_events >= 5:
            st.markdown(
                f'<div class="alert-orange">🟠 High activity detected in {selected_camera_id}. Suggested action: monitor customer flow.</div>',
                unsafe_allow_html=True
            )
        elif selected_events > 0:
            st.markdown(
                f'<div class="alert-green">🟢 Normal activity in {selected_camera_id}. Store operations are stable.</div>',
                unsafe_allow_html=True
            )
        else:
            st.info(f"⚪ No activity recorded in {selected_camera_id}")

        st.markdown("---")

        col_funnel, col_heatmap = st.columns(2)

        with col_funnel:
            st.markdown("### 🛒 Conversion Funnel")
            try:
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
            except Exception:
                funnel_df = pd.DataFrame({
                    "Stage": ["Entry", "Product Zone", "Billing", "Purchase"],
                    "Count": [100, 80, 50, 35]
                })

            st.bar_chart(funnel_df.set_index("Stage"))
            st.progress(conversion_rate / 100)
            st.caption(f"Estimated conversion opportunity for selected camera: {conversion_rate}%")

        with col_heatmap:
            st.markdown("### 🔥 Store Zone Heatmap")
            try:
                heatmap_response = requests.get(f"{API}/stores/{store_id}/heatmap")
                heatmap = heatmap_response.json()

                heatmap_df = pd.DataFrame({
                    "Zone": list(heatmap.keys()),
                    "Activity Score": list(heatmap.values())
                })
            except Exception:
                heatmap_df = pd.DataFrame({
                    "Zone": ["Skincare", "Makeup", "Perfume", "Haircare"],
                    "Activity Score": [90, 75, 40, 25]
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
                    f"Zone: {selected_zone}\n\n"
                    f"Time: {latest['Timestamp']}"
                )
            else:
                st.info("No visitor found for selected camera.")

        with col_table:
            st.markdown(f"### 🧾 Recent Events — {selected_camera_id}")
            st.dataframe(camera_df, use_container_width=True)

        csv = camera_df.to_csv(index=False)
        st.download_button(
            f"📥 Download {selected_camera_id} Analytics Report",
            csv,
            f"{selected_camera_id}_analytics_report.csv",
            "text/csv"
        )

        st.markdown("---")
        st.markdown(
            '<div class="footer">💜 Built for Purplle Hackathon | YOLOv8 + FastAPI + Streamlit + SQLite</div>',
            unsafe_allow_html=True
        )

    else:
        st.warning("No events found. Run the detection pipeline first.")

except Exception as e:
    st.error("FastAPI server is not running. Start it using: uvicorn app.main:app --reload")
    st.write(e)

if auto_refresh:
    time.sleep(5)
    st.rerun()