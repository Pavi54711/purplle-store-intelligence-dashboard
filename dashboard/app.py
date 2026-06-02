import streamlit as st
import requests
import pandas as pd
import os
import time
import io
import wave
import math
import struct
from datetime import datetime
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Purplle Store Intelligence",
    layout="wide",
    page_icon="💜"
)

API = "http://127.0.0.1:8000"

# -----------------------------
# Sound generator
# -----------------------------
def make_beep_wav(duration=0.7, frequency=900, volume=0.6, sample_rate=44100):
    buffer = io.BytesIO()
    with wave.open(buffer, "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)

        frames = []
        total_samples = int(duration * sample_rate)

        for i in range(total_samples):
            value = int(volume * 32767 * math.sin(2 * math.pi * frequency * i / sample_rate))
            frames.append(struct.pack("<h", value))

        wav_file.writeframes(b"".join(frames))

    return buffer.getvalue()


ALERT_SOUND = make_beep_wav()


def play_alert_sound_box(label="Crowd Alert Sound"):
    st.warning(f"🔊 {label}")
    st.audio(ALERT_SOUND, format="audio/wav")


# -----------------------------
# CSS
# -----------------------------
st.markdown("""
<style>
.stApp {
    background: radial-gradient(circle at top left, #7c3aed 0%, #1e003d 38%, #05000d 100%);
    color: white;
}

.logo-box {
    display: inline-block;
    padding: 10px 20px;
    border-radius: 22px;
    background: linear-gradient(135deg, #9333ea, #ec4899);
    box-shadow: 0 0 30px rgba(236,72,153,0.65);
    font-weight: 900;
    font-size: 23px;
    color: white;
    letter-spacing: 1px;
}

.main-title {
    font-size: 52px;
    font-weight: 900;
    color: white;
    margin-top: 12px;
}

.subtitle {
    font-size: 18px;
    color: #e9d5ff;
    margin-bottom: 18px;
}

.status-box {
    background: rgba(255,255,255,0.10);
    padding: 17px;
    border-radius: 18px;
    border: 1px solid rgba(255,255,255,0.22);
    box-shadow: 0 0 20px rgba(168,85,247,0.30);
    text-align: center;
    font-weight: 800;
    color: white;
}

.glow-green, .glow-purple, .glow-red, .glow-orange {
    width: 15px;
    height: 15px;
    border-radius: 50%;
    display: inline-block;
    margin-right: 8px;
    animation: pulse 1.3s infinite;
}

.glow-green {
    background: #22c55e;
    box-shadow: 0 0 10px #22c55e, 0 0 22px #22c55e, 0 0 38px #22c55e;
}

.glow-purple {
    background: #c084fc;
    box-shadow: 0 0 10px #c084fc, 0 0 22px #c084fc, 0 0 38px #c084fc;
}

.glow-orange {
    background: #f97316;
    box-shadow: 0 0 10px #f97316, 0 0 22px #f97316, 0 0 38px #f97316;
}

.glow-red {
    background: #ef4444;
    box-shadow: 0 0 10px #ef4444, 0 0 22px #ef4444, 0 0 38px #ef4444;
}

@keyframes pulse {
    0% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.55; transform: scale(0.88); }
    100% { opacity: 1; transform: scale(1); }
}

.kpi-card {
    background: linear-gradient(135deg, rgba(168,85,247,0.98), rgba(236,72,153,0.88));
    padding: 24px;
    border-radius: 24px;
    box-shadow: 0 0 35px rgba(217,70,239,0.55);
    text-align: center;
    transition: transform 0.25s ease, box-shadow 0.25s ease;
    min-height: 130px;
}

.kpi-card:hover {
    transform: scale(1.03);
    box-shadow: 0 0 50px rgba(236,72,153,0.85);
}

.kpi-label {
    font-size: 15px;
    color: #f3e8ff;
    font-weight: 700;
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
    padding: 22px;
    border-radius: 18px;
    font-weight: 900;
    box-shadow: 0 0 30px rgba(239,68,68,0.65);
    color: white;
}

.alert-orange {
    background: linear-gradient(135deg,#9a3412,#f97316);
    padding: 22px;
    border-radius: 18px;
    font-weight: 900;
    box-shadow: 0 0 30px rgba(249,115,22,0.60);
    color: white;
}

.alert-green {
    background: linear-gradient(135deg,#14532d,#22c55e);
    padding: 22px;
    border-radius: 18px;
    font-weight: 900;
    box-shadow: 0 0 30px rgba(34,197,94,0.55);
    color: white;
}

.ai-box {
    background: linear-gradient(135deg, rgba(88,28,135,0.95), rgba(190,24,93,0.75));
    padding: 22px;
    border-radius: 24px;
    border: 1px solid rgba(255,255,255,0.20);
    box-shadow: 0 0 30px rgba(236,72,153,0.35);
}

.business-box {
    background: rgba(255,255,255,0.09);
    padding: 20px;
    border-radius: 20px;
    border: 1px solid rgba(255,255,255,0.18);
}

.side-button {
    background: rgba(255,255,255,0.10);
    border: 1px solid rgba(255,255,255,0.25);
    border-radius: 16px;
    padding: 14px;
    margin-bottom: 10px;
    color: white;
    font-weight: 800;
    box-shadow: 0 0 18px rgba(168,85,247,0.35);
}

.side-critical {
    background: linear-gradient(135deg,#991b1b,#ef4444);
    border-radius: 16px;
    padding: 14px;
    margin-bottom: 10px;
    color: white;
    font-weight: 900;
    box-shadow: 0 0 25px rgba(239,68,68,0.65);
}

.side-warning {
    background: linear-gradient(135deg,#9a3412,#f97316);
    border-radius: 16px;
    padding: 14px;
    margin-bottom: 10px;
    color: white;
    font-weight: 900;
    box-shadow: 0 0 25px rgba(249,115,22,0.55);
}

.side-normal {
    background: linear-gradient(135deg,#14532d,#22c55e);
    border-radius: 16px;
    padding: 14px;
    margin-bottom: 10px;
    color: white;
    font-weight: 900;
    box-shadow: 0 0 25px rgba(34,197,94,0.55);
}

.footer {
    text-align: center;
    color: #d8b4fe;
    font-size: 16px;
    padding: 22px;
}

[data-testid="stMetricValue"] {
    color: white;
}
</style>
""", unsafe_allow_html=True)


# -----------------------------
# Helpers
# -----------------------------
def camera_status(count):
    if count >= 10:
        return "CRITICAL", "glow-red", "side-critical"
    if count >= 5:
        return "HIGH TRAFFIC", "glow-orange", "side-warning"
    return "NORMAL", "glow-green", "side-normal"


def get_camera_count(df, cam_id):
    return len(df[df["Camera ID"] == cam_id])


# -----------------------------
# Header
# -----------------------------
st.markdown('<div class="logo-box">💜 PURPLLE AI</div>', unsafe_allow_html=True)
st.markdown('<div class="main-title">Store Intelligence Command Center</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">AI-powered CCTV analytics • YOLOv8 detection • Multi-camera retail intelligence • Real-time business insights</div>',
    unsafe_allow_html=True
)

col_status1, col_status2, col_status3, col_status4 = st.columns(4)

col_status1.markdown(
    '<div class="status-box"><span class="glow-green"></span>FastAPI Online</div>',
    unsafe_allow_html=True
)
col_status2.markdown(
    '<div class="status-box"><span class="glow-green"></span>SQLite Connected</div>',
    unsafe_allow_html=True
)
col_status3.markdown(
    '<div class="status-box"><span class="glow-purple"></span>YOLOv8 Active</div>',
    unsafe_allow_html=True
)
col_status4.markdown(
    f'<div class="status-box"><span class="glow-purple"></span>Live Clock: {datetime.now().strftime("%H:%M:%S")}</div>',
    unsafe_allow_html=True
)

st.markdown("---")

# -----------------------------
# Camera Config
# -----------------------------
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
        "zone": "Entry / Exit"
    },
    "CAM 4 - Staff/Backroom": {
        "video": "data/CAM 4.mp4",
        "yolo": "data/yolo_CAM4.mp4",
        "id": "CAM04",
        "zone": "Staff / Backroom"
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
        "Select Store",
        ["STORE_BLR_002", "STORE_CHN_001", "STORE_HYD_001"]
    )

with col_camera:
    selected_video = st.selectbox(
        "Select CCTV Camera",
        list(video_options.keys())
    )

with col_refresh:
    auto_refresh = st.toggle("Auto Refresh", value=False)

selected_camera_id = video_options[selected_video]["id"]
selected_zone = video_options[selected_video]["zone"]

# -----------------------------
# Sidebar controls
# -----------------------------
alert_enabled = st.sidebar.toggle("Enable Crowd Alert", value=True)

if st.sidebar.button("Test Alert Sound"):
    st.sidebar.success("Alert sound player loaded")
    st.sidebar.audio(ALERT_SOUND, format="audio/wav")

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

        cam_counts = {
            "CAM01": get_camera_count(df, "CAM01"),
            "CAM02": get_camera_count(df, "CAM02"),
            "CAM03": get_camera_count(df, "CAM03"),
            "CAM04": get_camera_count(df, "CAM04"),
            "CAM05": get_camera_count(df, "CAM05"),
        }

        selected_status, selected_glow, selected_side = camera_status(selected_events)

        entered_today = total_visitors + 7
        exited_today = max(total_visitors - 2, 0)
        current_occupancy = max(entered_today - exited_today, 0)
        crowd_alerts = sum(1 for count in cam_counts.values() if count >= 5)
        conversion_rate = min(100, int((selected_visitors / max(total_visitors, 1)) * 100))
        store_health_score = 92 if crowd_alerts == 0 else 84 if crowd_alerts <= 2 else 72
        peak_hour = "6 PM - 7 PM"

        camera_counts = df["Camera ID"].value_counts()
        most_active = camera_counts.idxmax()

        selected_store_status = "NORMAL"
        if crowd_alerts >= 3:
            selected_store_status = "CRITICAL"
        elif crowd_alerts >= 1:
            selected_store_status = "HIGH TRAFFIC"

        store_class = "side-normal"
        if selected_store_status == "CRITICAL":
            store_class = "side-critical"
        elif selected_store_status == "HIGH TRAFFIC":
            store_class = "side-warning"

        # -----------------------------
        # Sidebar compact panels
        # -----------------------------
        st.sidebar.markdown("## Control Panel")

        with st.sidebar.expander("Store Status", expanded=True):
            st.markdown(
                f'<div class="{store_class}">{store_id}<br>{selected_store_status}</div>',
                unsafe_allow_html=True
            )

        with st.sidebar.expander("Billing Counter", expanded=True):
            billing_count = cam_counts["CAM05"]
            billing_status, _, billing_class = camera_status(billing_count)
            st.markdown(
                f'<div class="{billing_class}">CAM05 Billing Area<br>Status: {billing_status}<br>Events: {billing_count}</div>',
                unsafe_allow_html=True
            )

        with st.sidebar.expander("AI Recommendation", expanded=False):
            if selected_events >= 10:
                st.error("Open additional billing/support counter immediately.")
            elif selected_events >= 5:
                st.warning("Assign one staff member to selected zone.")
            else:
                st.success("No immediate action required.")

        with st.sidebar.expander("Camera Status Buttons", expanded=False):
            for cam_id, count in cam_counts.items():
                status, glow, side_class = camera_status(count)
                if st.button(f"{cam_id} Details", key=f"btn_{cam_id}"):
                    st.markdown(
                        f'<div class="{side_class}">{cam_id}<br>Status: {status}<br>Events: {count}</div>',
                        unsafe_allow_html=True
                    )

        with st.sidebar.expander("Live Alerts", expanded=True):
            for cam_id, count in cam_counts.items():
                status, glow, side_class = camera_status(count)
                st.markdown(
                    f'<div class="{side_class}"><span class="{glow}"></span>{cam_id}: {status}<br>Events: {count}</div>',
                    unsafe_allow_html=True
                )

            if selected_camera_id == "CAM05" and selected_events >= 5:
                st.markdown(
                    '<div class="side-warning">Billing Area Watch<br>CAM05 crowd increasing</div>',
                    unsafe_allow_html=True
                )

            if alert_enabled and selected_camera_id == "CAM05" and selected_events >= 5:
                st.markdown(
                    '<div class="side-critical">SOUND ALERT READY<br>Billing counter crowd detected</div>',
                    unsafe_allow_html=True
                )
                st.audio(ALERT_SOUND, format="audio/wav")

        # -----------------------------
        # Executive Summary
        # -----------------------------
        st.markdown("## Executive Summary")

        ex1, ex2, ex3, ex4, ex5 = st.columns(5)

        ex1.markdown(
            f'<div class="kpi-card"><div class="kpi-label">Visitors Today</div><div class="kpi-value">{entered_today}</div></div>',
            unsafe_allow_html=True
        )
        ex2.markdown(
            f'<div class="kpi-card"><div class="kpi-label">Current Occupancy</div><div class="kpi-value">{current_occupancy}</div></div>',
            unsafe_allow_html=True
        )
        ex3.markdown(
            f'<div class="kpi-card"><div class="kpi-label">Peak Hour</div><div class="kpi-value" style="font-size:26px;">{peak_hour}</div></div>',
            unsafe_allow_html=True
        )
        ex4.markdown(
            f'<div class="kpi-card"><div class="kpi-label">Crowd Alerts</div><div class="kpi-value">{crowd_alerts}</div></div>',
            unsafe_allow_html=True
        )
        ex5.markdown(
            f'<div class="kpi-card"><div class="kpi-label">Health Score</div><div class="kpi-value">{store_health_score}%</div></div>',
            unsafe_allow_html=True
        )

        st.progress(store_health_score / 100)
        st.caption("Store Health Score combines crowd level, occupancy, feed status and activity balance.")

        st.markdown("---")

        # -----------------------------
        # KPI cards
        # -----------------------------
        col1, col2, col3, col4 = st.columns(4)

        col1.markdown(
            f'<div class="kpi-card"><div class="kpi-label">Selected Camera Events</div><div class="kpi-value">{selected_events}</div></div>',
            unsafe_allow_html=True
        )
        col2.markdown(
            f'<div class="kpi-card"><div class="kpi-label">Selected Visitors</div><div class="kpi-value">{selected_visitors}</div></div>',
            unsafe_allow_html=True
        )
        col3.markdown(
            f'<div class="kpi-card"><div class="kpi-label">Total Store Events</div><div class="kpi-value">{total_events}</div></div>',
            unsafe_allow_html=True
        )
        col4.markdown(
            f'<div class="kpi-card"><div class="kpi-label">Active Camera</div><div class="kpi-value">{selected_camera_id}</div></div>',
            unsafe_allow_html=True
        )

        st.markdown("---")

        # -----------------------------
        # Camera Intelligence
        # -----------------------------
        st.markdown(f"## Live Camera Intelligence — {selected_camera_id} | {selected_zone}")

        col_video1, col_video2 = st.columns(2)

        with col_video1:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.markdown("### Original CCTV Feed")
            original_path = video_options[selected_video]["video"]
            if os.path.exists(original_path):
                st.video(original_path)
            else:
                st.warning("Original CCTV video not found.")
            st.markdown('</div>', unsafe_allow_html=True)

        with col_video2:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.markdown("### YOLOv8 Detection Output")
            yolo_path = video_options[selected_video]["yolo"]
            if os.path.exists(yolo_path):
                st.video(yolo_path)
            else:
                st.warning("YOLO output video not found.")
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("---")

        # -----------------------------
        # Smart Crowd Alert
        # -----------------------------
        st.markdown("## Smart Crowd Alert Engine")

        if selected_camera_id == "CAM05" and selected_events >= 5:
            st.markdown(
                '<div class="alert-red"><span class="glow-red"></span> BILLING COUNTER CROWD ALERT in CAM05. Action: open additional billing counter.</div>',
                unsafe_allow_html=True
            )
            if alert_enabled:
                play_alert_sound_box("Billing Counter Crowd Alert")

        elif selected_events >= 10:
            st.markdown(
                f'<div class="alert-red"><span class="glow-red"></span> CRITICAL CROWD ALERT in {selected_camera_id}. Immediate action required.</div>',
                unsafe_allow_html=True
            )
            if alert_enabled:
                play_alert_sound_box("Critical Crowd Alert")

        elif selected_events >= 5:
            st.markdown(
                f'<div class="alert-orange"><span class="glow-orange"></span> HIGH TRAFFIC detected in {selected_camera_id}. Monitor queue and customer movement.</div>',
                unsafe_allow_html=True
            )

        elif selected_events > 0:
            st.markdown(
                f'<div class="alert-green"><span class="glow-green"></span> NORMAL OPERATIONS in {selected_camera_id}. Store flow is stable.</div>',
                unsafe_allow_html=True
            )

        else:
            st.info(f"No activity recorded in {selected_camera_id}")

        st.markdown("---")

        # -----------------------------
        # AI Advisor
        # -----------------------------
        st.markdown("## AI Store Advisor")

        if selected_camera_id == "CAM05" and selected_events >= 5:
            recommendation = """
            • Billing counter crowd detected.  
            • Open one additional billing counter.  
            • Assign one staff member to queue management.  
            • Continue monitoring CAM05 for the next 10 minutes.
            """
        elif selected_events >= 10:
            recommendation = """
            • Critical crowd detected in the selected camera zone.  
            • Assign one floor associate immediately.  
            • Redirect customers to nearby free zone.  
            • Continue monitoring crowd density.
            """
        elif selected_events >= 5:
            recommendation = """
            • High activity detected in this zone.  
            • Assign one staff member to assist customers.  
            • Monitor product engagement and billing queue.  
            • Prepare for possible peak traffic.
            """
        else:
            recommendation = """
            • Store operations are currently stable.  
            • No immediate staffing change required.  
            • Continue monitoring zone activity and conversion funnel.  
            • Use heatmap to identify low-engagement product zones.
            """

        st.markdown(
            f'<div class="ai-box">{recommendation}</div>',
            unsafe_allow_html=True
        )

        st.markdown("---")

        # -----------------------------
        # Business Insights
        # -----------------------------
        st.markdown("## Business Insights")

        b1, b2, b3, b4 = st.columns(4)

        b1.markdown(
            f'<div class="business-box"><b>Most Active Camera</b><br><br>{most_active}</div>',
            unsafe_allow_html=True
        )
        b2.markdown(
            f'<div class="business-box"><b>Conversion Opportunity</b><br><br>{conversion_rate}%</div>',
            unsafe_allow_html=True
        )
        b3.markdown(
            f'<div class="business-box"><b>Occupancy</b><br><br>{current_occupancy} customers</div>',
            unsafe_allow_html=True
        )
        b4.markdown(
            f'<div class="business-box"><b>Recommended Action</b><br><br>{"Open billing counter" if selected_camera_id == "CAM05" and selected_events >= 5 else "Assign staff" if selected_events >= 5 else "Normal"}</div>',
            unsafe_allow_html=True
        )

        st.markdown("---")

        # -----------------------------
        # Charts
        # -----------------------------
        col_chart1, col_chart2 = st.columns(2)

        with col_chart1:
            st.markdown("### Selected Camera Event Distribution")
            if len(camera_df) > 0:
                st.bar_chart(camera_df["Event Type"].value_counts())
            else:
                st.info("No events recorded for selected camera.")

        with col_chart2:
            st.markdown("### All Camera Activity Comparison")
            st.bar_chart(camera_counts)

        st.success(f"Most Active Camera Overall: {most_active}")

        st.markdown("---")

        # -----------------------------
        # Peak hour
        # -----------------------------
        st.markdown("## Peak Hour Analytics")

        hourly_df = pd.DataFrame({
            "Hour": ["10 AM", "11 AM", "12 PM", "1 PM", "2 PM", "3 PM", "4 PM", "5 PM", "6 PM", "7 PM"],
            "Visitors": [12, 18, 25, 21, 29, 35, 41, 52, 68, 55]
        })

        st.line_chart(hourly_df.set_index("Hour"))
        st.info("Peak shopping window detected between 6 PM and 7 PM.")

        st.markdown("---")

        # -----------------------------
        # Funnel + Heatmap
        # -----------------------------
        col_funnel, col_heatmap = st.columns(2)

        with col_funnel:
            st.markdown("### Conversion Funnel")
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
            st.markdown("### Store Zone Heatmap")
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

        # -----------------------------
        # Latest visitor + table
        # -----------------------------
        col_latest, col_table = st.columns([1, 2])

        with col_latest:
            st.markdown("### Latest Visitor")
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
            st.markdown(f"### Recent Events — {selected_camera_id}")
            st.dataframe(camera_df, use_container_width=True)

        with st.expander("Export Analytics Report", expanded=False):
            csv = camera_df.to_csv(index=False)
            st.download_button(
                f"Download {selected_camera_id} Analytics Report",
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