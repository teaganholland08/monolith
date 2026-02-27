import streamlit as st
import psutil
import pandas as pd
import time
from datetime import datetime

st.set_page_config(
    page_title="Monolith-Core Health Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Monolith-Core Health Dashboard")
st.write(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Sidebar for options
st.sidebar.header("Configuration")
refresh_rate = st.sidebar.slider("Refresh Rate (seconds)", 1, 60, 5)

# Metrics section
col1, col2 = st.columns(2)

# Memory Stats
with col1:
    st.subheader("🧠 Memory Usage")
    mem = psutil.virtual_memory()
    col1_1, col1_2, col1_3 = st.columns(3)
    col1_1.metric("Total", f"{mem.total / (1024**3):.2f} GB")
    col1_2.metric("Used", f"{mem.used / (1024**3):.2f} GB", f"{mem.percent}%")
    col1_3.metric("Available", f"{mem.available / (1024**3):.2f} GB")
    
    # Progress bar
    st.progress(mem.percent / 100)

# Disk Stats
with col2:
    st.subheader("💾 Disk Usage")
    disk = psutil.disk_usage('/')
    col2_1, col2_2, col2_3 = st.columns(3)
    col2_1.metric("Total", f"{disk.total / (1024**3):.2f} GB")
    col2_2.metric("Used", f"{disk.used / (1024**3):.2f} GB", f"{disk.percent}%")
    col2_3.metric("Free", f"{disk.free / (1024**3):.2f} GB")
    
    # Progress bar
    st.progress(disk.percent / 100)

st.divider()

# Detailed stats / History
st.subheader("📈 System Load (CPU)")
cpu_percent = psutil.cpu_percent(interval=1, percpu=True)
cpu_df = pd.DataFrame({
    'Core': [f'Core {i}' for i in range(len(cpu_percent))],
    'Usage (%)': cpu_percent
})
st.bar_chart(cpu_df.set_index('Core'))

# Auto-refresh logic (basic)
if st.sidebar.button("Manual Refresh"):
    st.rerun()

st.info("The dashboard updates on manual refresh or slider adjustment. For real-time updates, keep the browser tab active.")
