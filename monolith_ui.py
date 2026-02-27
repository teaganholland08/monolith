import streamlit as st
import time
import folium
from streamlit_folium import st_folium
import psutil
import requests
import datetime
import json
import os
import random
import xml.etree.ElementTree as ET
import pandas as pd
import numpy as np

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="MONOLITH OMEGA",
    page_icon="🏴‍☠️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- GLOBAL DATA FETCHING (Available to ALL Modes) ---
@st.cache_data(ttl=60)
def get_crypto_prices():
    try:
        # Fetching multiple coins
        r = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana,monero&vs_currencies=usd", timeout=2).json()
        return r
    except: 
        return {"bitcoin": {"usd": 98000}, "ethereum": {"usd": 3500}, "solana": {"usd": 140}, "monero": {"usd": 160}}

def get_system_stats():
    # CPU
    cpu = psutil.cpu_percent()
    
    # MEMORY
    ram = psutil.virtual_memory()
    ram_pct = ram.percent
    ram_used = round(ram.used / (1024**3), 1)
    ram_total = round(ram.total / (1024**3), 1)
    
    # DISK
    try:
        disk = psutil.disk_usage('/')
        disk_pct = disk.percent
        disk_free = round(disk.free / (1024**3), 1)
    except:
        disk_pct = 0
        disk_free = 0
    
    # BATTERY
    try:
        batt = psutil.sensors_battery()
        if batt:
            batt_pct = batt.percent
            batt_plugged = "🔌" if batt.power_plugged else "🔋"
        else:
            batt_pct = 100
            batt_plugged = "⚡"
    except:
        batt_pct = 100
        batt_plugged = "⚡"
        
    return {
        "cpu": cpu,
        "ram_pct": ram_pct,
        "ram_gb": f"{ram_used}/{ram_total} GB",
        "disk_pct": disk_pct,
        "disk_gb": f"{disk_free} GB FREE",
        "batt_pct": batt_pct,
        "batt_icon": batt_plugged
    }

@st.cache_data(ttl=60)
def get_ip_info():
    try:
        return requests.get("http://ip-api.com/json/", timeout=2).json()
    except: return {"query": "UNKNOWN", "isp": "UNKNOWN"}

@st.cache_data(ttl=600)
def get_weather():
    try:
        # OpenMeteo for Powell River
        url = "https://api.open-meteo.com/v1/forecast?latitude=49.83&longitude=-124.52&current_weather=true"
        r = requests.get(url, timeout=2).json()
        return r["current_weather"]
    except: return {"temperature": 0, "windspeed": 0, "weathercode": 0}

@st.cache_data(ttl=30)
def check_network():
    try:
        t1 = time.time()
        requests.get("https://google.com", timeout=1)
        latency = round((time.time() - t1) * 1000)
        return f"🟢 {latency}ms"
    except:
        return "🔴 OFF-GRID"

@st.cache_data(ttl=300)
def get_live_news():
    try:
        r = requests.get("http://feeds.bbci.co.uk/news/world/rss.xml", timeout=2)
        root = ET.fromstring(r.content)
        items = root.findall('./channel/item')[:5]
        news = []
        for item in items:
            news.append((item.find('title').text, item.find('link').text))
        return news
    except: return []

# --- AUDIO INTERFACE ---
def play_audio_report(text):
    js = f"""
    <script>
        var msg = new SpeechSynthesisUtterance("{text}");
        window.speechSynthesis.speak(msg);
    </script>
    """
    st.components.v1.html(js, height=0, width=0)

# --- CUSTOM CSS (CYBERPUNK v2.0) ---
st.markdown("""
    <style>
    /* GLOBAL THEME */
    .stApp {
        background-color: #050505;
        color: #00FFFF;
        font-family: 'Courier New', Courier, monospace;
    }
    
    /* SCROLLBARS */
    ::-webkit-scrollbar { width: 8px; }
    ::-webkit-scrollbar-track { background: #000; }
    ::-webkit-scrollbar-thumb { background: #00FFFF; border-radius: 4px; }
    
    /* GLOWING TEXT */
    h1, h2, h3, .metric-value {
        color: #00FFFF !important;
        text-shadow: 0 0 10px rgba(0, 255, 255, 0.7);
        letter-spacing: 2px !important;
        text-transform: uppercase;
    }
    
    /* GLASS PANELS (CYBERPUNK) */
    .glass-panel {
        background: rgba(10, 10, 16, 0.85);
        border: 1px solid #00FFFF;
        border-left: 5px solid #00FFFF;
        border-radius: 4px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 0 15px rgba(0, 255, 255, 0.1);
        backdrop-filter: blur(5px);
        transition: all 0.2s ease-in-out;
    }
    .glass-panel:hover {
        box-shadow: 0 0 30px rgba(0, 255, 255, 0.3);
        transform: scale(1.02);
        border-color: #FFFFFF;
    }
    
    /* FUTURISTIC BUTTONS */
    .stButton>button {
        background: black;
        color: #00FFFF;
        border: 2px solid #00FFFF;
        border-radius: 0px;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: 0.3s;
        box-shadow: 0 0 5px #00FFFF;
    }
    .stButton>button:hover {
        background: #00FFFF;
        color: black;
        box-shadow: 0 0 25px #00FFFF;
        font-weight: 900;
    }
    .stButton>button:active {
        transform: translateY(2px);
    }
    
    /* SIDEBAR */
    section[data-testid="stSidebar"] {
        background-color: #000000;
        border-right: 2px solid #00FFFF;
    }
    
    /* TABS */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; border-bottom: 1px solid #333; }
    .stTabs [data-baseweb="tab"] {
        background-color: #111;
        border: 1px solid #333;
        color: #888;
        border-radius: 0px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #00FFFF !important;
        color: #000 !important;
        font-weight: bold;
        box-shadow: 0 0 15px #00FFFF;
    }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR: THE SINGLE PANE OF GLASS ---
with st.sidebar:
    st.title("⚓ MONOLITH")
    st.caption("OMEGA OPERATING SYSTEM")
    st.markdown("---")
    
    # MASTER MODE SELECTOR
    view_mode = st.radio("DESKTOP SELECTOR", [
        "OPERATIONS (MAIN)", 
        "PHYSICAL (BODY/HOME)", 
        "INTEL (WORLD)", 
        "SYSTEM (BACKEND)",
        "MASTER (WEB)"
    ])
    
    st.markdown("---")
    
    # GLOBAL CONTROLS
    refresh_rate = st.slider("💓 SYSTEM PULSE", 1, 60, 5)
    
    # SYSTEM OPERATIONS GRID
    st.markdown("### ⚡ SYSTEM OPS")
    c_op1, c_op2 = st.columns(2)
    with c_op1:
        if st.button("🚀 BOOT", use_container_width=True): st.toast("SYSTEM STARTING...")
        if st.button("🔄 RERUN", use_container_width=True): st.rerun()
    with c_op2:
        if st.button("🛑 HALT", use_container_width=True): st.toast("STOPPING SERVICES...")
        if st.button("🔒 LOCK", use_container_width=True): st.toast("SYSTEM LOCKED")
        
    st.markdown("---")
    
    # DEVICE TOGGLE
    device_mode = st.toggle("MOBILE LAYOUT", value=False)
    
    if st.button("💀 KILL SWITCH", type="primary", use_container_width=True):
        with open("kill_signal.txt", "w") as f: f.write("KILL")
        st.error("SYSTEM TERMINATED.")
        st.stop()
    
    st.caption("v.OMEGA.3.0 | TEAGAN HOLLAND")
    
    # GAMIFICATION (XP SYSTEM)
    st.markdown("---")
    uptime = time.time() - psutil.boot_time()
    lvl = int(uptime / 3600) + 1
    xp = int((uptime % 3600) / 36)
    st.metric("COMMANDER LEVEL", f"LVL {lvl}", f"{xp}% XP")
    st.progress(xp / 100)
    
    # MEDIA PLAYER
    st.markdown("### 🎵 TACTICAL AUDIO")
    st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3", format="audio/mp3")


# --- MODULE 1: COMMAND (The HUD) ---
# --- MODULE 1: COMMAND (The Bento Grid HUD) ---
def render_command_dashboard():
    # Fetch Core Data
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    stats = get_system_stats()
    crypto = get_crypto_prices()
    btc_price = crypto.get("bitcoin", {}).get("usd", 0)
    net_status = check_network()
    
    # --- ROW 1: THE GLOBAL HUD (Top Bar) ---
    # Left: Ticker (Already Rendered globally via HTML, so we focus on Status/Actions here)
    # The User wants: Left=Ticker, Center=Status, Right=Actions
    # Since Ticker is HTML absolute, we'll build the visual grid below it.
    
    st.markdown("### 💠 GLOBAL HUD")
    r1_col1, r1_col2, r1_col3 = st.columns([2, 1, 1])
    
    with r1_col1:
        # NEWS / TICKER AREA
        st.markdown('<div class="glass-panel" style="height:100px; overflow-y:auto;">', unsafe_allow_html=True)
        st.caption("📰 LIVE WIRE")
        news = get_live_news()
        for t, l in news[:3]: st.markdown(f"▪️ [{t}]({l})")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with r1_col2:
        # SYSTEM STATUS (Heartbeat)
        st.markdown('<div class="glass-panel" style="height:100px; text-align:center;">', unsafe_allow_html=True)
        st.caption("💓 HEARTBEAT")
        st.markdown(f"**{net_status}**")
        st.markdown(f"**{now.split(' ')[1]}**")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with r1_col3:
        # QUICK ACTIONS
        st.markdown('<div class="glass-panel" style="height:100px; display:flex; gap:5px;">', unsafe_allow_html=True)
        c_q1, c_q2 = st.columns(2)
        with c_q1: st.button("➕ ENTRY", use_container_width=True)
        with c_q2: st.button("🛑 STOP", type="primary", use_container_width=True)
        st.button("🎤 VOICE", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)


    # --- ROW 2: THE CORE METRICS (Main View) ---
    r2_col_main, r2_col_side = st.columns([3, 1])
    
    with r2_col_main:
        # EXECUTIVE CAROUSEL
        st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
        st.subheader("🎠 EXECUTIVE CAROUSEL")
        
        # Tabs act as the Slide Show
        carousel_tabs = st.tabs(["💰 FINANCIALS", "🎯 GOALS", "🗓️ CALENDAR"])
        
        with carousel_tabs[0]:
            f1, f2, f3 = st.columns(3)
            with f1: st.metric("DAILY SPEND", "$124.50", "-$12.00")
            with f2: st.metric("WIN/LOSS", "4W - 1L", "80%")
            with f3: st.metric("NET WORTH", "$1.2M", "+3%")
            # Area Chart
            st.area_chart(pd.DataFrame(np.random.randn(20, 1), columns=["PNL"]), height=150, color="#00FFFF")
            
        with carousel_tabs[1]:
            st.caption("PROJECT: OMEGA")
            st.progress(0.85)
            st.caption("PROJECT: TITAN")
            st.progress(0.40)
            st.caption("PROJECT: EXODUS")
            st.progress(0.15)
            
        with carousel_tabs[2]:
            st.info("🔔 14:00 - Market Close")
            st.warning("🔔 18:00 - Tactical Training")
            st.success("🔔 21:00 - Deep Sleep Protocol")
            
        st.markdown('</div>', unsafe_allow_html=True)
        
    with r2_col_side:
        # LIVE TERMINAL (Mini)
        st.markdown('<div class="glass-panel" style="height:400px;">', unsafe_allow_html=True)
        st.subheader("📟 TERM_LITE")
        st.code("> system ready\n> agent active\n> monitoring...", language="bash")
        st.text_input("EXEC >", key="mini_term")
        st.markdown('</div>', unsafe_allow_html=True)


    # --- ROW 3: COMMAND & CONTROL (Bottom Section) ---
    r3_col1, r3_col2, r3_col3 = st.columns([1, 1, 1])
    
    with r3_col1:
        # NETWORK / SOCIAL
        st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
        st.subheader("📡 FEED")
        st.markdown("**GMAIL**: 3 New (Invoice, Mom, Alert)")
        st.markdown("**DISCORD**: 12 Mentions (@devs)")
        st.markdown("**X**: Trending #Bitcoin")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with r3_col2:
        # EXECUTION GRID (3x3)
        st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
        st.subheader("⚡ EXECUTION GRID")
        g1, g2, g3 = st.columns(3)
        with g1:
            st.button("🚀 DEPLOY", use_container_width=True)
            st.button("💸 PAY", use_container_width=True)
            st.button("🏠 HOUSE", use_container_width=True)
        with g2:
            st.button("🚁 DRONE", use_container_width=True)
            st.button("💊 MEDS", use_container_width=True)
            st.button("🔐 LOCK", use_container_width=True)
        with g3:
            st.button("🌙 NIGHT", use_container_width=True)
            st.button("☀️ DAY", use_container_width=True)
            st.button("🌪️ PURGE", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with r3_col3:
        # RESOURCE MONITOR
        st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
        st.subheader("📊 RESOURCES")
        st.caption(f"CPU: {stats['cpu']}%")
        st.progress(stats['cpu'] / 100)
        st.caption(f"RAM: {stats['ram_pct']}%")
        st.progress(stats['ram_pct'] / 100)
        st.caption(f"API QUOTA: 42%")
        st.progress(0.42)
        st.markdown('</div>', unsafe_allow_html=True)


# --- MODULE 2: AGENTS (Execution Dashboard) ---
def render_agents_dashboard():
    st.markdown("## 🤖 AUTONOMOUS WORKFORCE")
    
    # TOTAL REVENUE CHART
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.subheader("💵 NET REVENUE (ALL AGENTS)")
    chart_data = pd.DataFrame(np.cumsum(np.random.randn(20) + 10), columns=['USD'])
    st.area_chart(chart_data, height=150, color="#00ff00")
    st.markdown('</div>', unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
        st.markdown("### 🦅 SCOUT")
        st.caption("STATUS: HUNTING")
        st.success("ROI: +12%")
        st.text("Thought: 'Analyzing Arb opportunity in DeFi...'")
        st.progress(0.4)
        if st.button("RECALL SCOUT"): st.toast("Recall Sent")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with c2:
        st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
        st.markdown("### ✍️ WRITER")
        st.caption("STATUS: DRAFTING")
        st.info("Output: 2 Arts/Day")
        st.text("Thought: 'Generating hooks for LinkedIn...'")
        st.progress(0.7)
        st.toggle("AGGRESSIVE COPY", value=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with c3:
        st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
        st.markdown("### ⚖️ SENTINEL")
        st.caption("STATUS: WATCHING")
        st.warning("Threats: 0")
        st.text("Thought: 'Scanning jurisdiction 47...'")
        st.progress(0.1)
        st.button("FORCE SCAN")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("### 🧠 HIVE LOGS")
    st.code("[10:42:01] SCOUT: Found Arbitrage opportunity (Spread: 1.2%)\n[10:41:55] WRITER: Published Draft #44 to Medium\n[10:41:12] SYSTEM: Backup Complete")


# --- MODULE 3: LIBRARY (Personal OS) ---
def render_library():
    st.markdown("## 📚 KNOWLEDGE BASE")
    
    col_l1, col_l2 = st.columns([1, 3])
    
    with col_l1:
        st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
        st.subheader("📂 FILES")
        doc = st.radio("SELECT DOCUMENT", [
            "PROJECT_MONOLITH_BLUEPRINT.md", 
            "MONOLITH_OPERATOR_MANUAL.md", 
            "SCAVENGER_DAILY_LOG.md",
            "trading.json",
            "threats.json"
        ])
        st.markdown("---")
        st.button("📥 EXPORT PDF")
        st.button("🔒 ENCRYPT")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_l2:
        st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
        st.subheader(f"📄 {doc}")
        try:
            with open(doc, "r") as f:
                content = f.read()
            
            # Editor Mode
            if st.toggle("✏️ EDITOR MODE"):
                new_content = st.text_area("CONTENT", content, height=600)
                if st.button("💾 SAVE CHANGES"):
                    with open(doc, "w") as f: f.write(new_content)
                    st.success("SAVED.")
            else:
                st.markdown(content)
        except:
            st.error("FILE NOT FOUND OR CORRUPTED")
        st.markdown('</div>', unsafe_allow_html=True)


# --- MODULE 4: TERMINAL (Admin Console) ---
def render_terminal():
    st.markdown("## 📟 ROOT TERMINAL")
    
    # Mock System Information (Neofetch style)
    st.code(f"""
    USER: Commander
    HOST: MONOLITH-OMEGA
    OS:   Windows 11 (Custom Kernel)
    UP:   {datetime.datetime.now().strftime("%H:%M:%S")}
    CPU:  {psutil.cpu_percent()}%
    RAM:  {psutil.virtual_memory().percent}%
    -------------------------
    """, language="bash")
    
    st.markdown('<div class="glass-panel" style="font-family:monospace; color:#0f0;">', unsafe_allow_html=True)
    
    history = st.session_state.get('term_history', [])
    for h in history:
        st.markdown(f"> {h}")
    
    cmd = st.text_input("COMMAND >", key="term_input")
    
    if cmd:
        st.session_state.term_history = history[-10:] + [f"$ {cmd}"]
        
        # Command Logic
        if cmd == "clear": 
            st.session_state.term_history = []
        elif cmd == "scan":
            st.session_state.term_history.append("SCANNING NETWORK... [OK]")
            st.session_state.term_history.append("FOUND 4 DEVICES: [PC] [PHONE] [IOT] [UNKNOWN]")
        elif cmd == "whoami":
             st.session_state.term_history.append("uid=0(root) gid=0(root) groups=0(root)")
        elif cmd == "help":
            st.session_state.term_history.append("AVAILABLE: scan, wipe, deploy, reboot, clear, whoami, netstat")
        elif cmd == "netstat":
            st.session_state.term_history.append("Active Connections:\n  TCP 192.168.1.42:443 (ESTABLISHED)\n  TCP 127.0.0.1:8501 (LISTEN)")
        else:
            st.session_state.term_history.append(f"Executing: {cmd} ... DONE.")
    
    st.markdown('</div>', unsafe_allow_html=True)


# --- MODULE 5: COMMS (Secure Chat) ---
def render_comms():
    st.markdown("## 📡 SECURE COMMS")
    
    c1, c2 = st.columns([3, 1])
    
    with c1:
        st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
        st.subheader("ENCRYPTED CHANNEL: [ALPHA]")
        msgs = st.session_state.get("chat_log", ["SYSTEM: Channel Open (AES-256)"])
        for m in msgs:
            st.text(f"> {m}")
        
        new_msg = st.text_input("TRANSMIT >")
        if st.button("SEND MESSAGE"):
            st.session_state.setdefault("chat_log", []).append(f"COMMANDER: {new_msg}")
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
    with c2:
        st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
        st.subheader("KEYS")
        if st.button("🔄 ROTATE KEYS"): st.success("NEW KEYS GENERATED")
        st.text("PGP: ACTIVE")
        st.text("VPN: ON")
        st.text("TOR: ON")
        st.markdown('</div>', unsafe_allow_html=True)


# --- MODULE 6: TOOLS (Utilities) ---
def render_tools():
    st.markdown("## 🧰 OMEGA TOOLBOX")
    
    t1, t2, t3 = st.columns(3)
    
    with t1:
        st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
        st.subheader("🔐 PASS GEN")
        length = st.slider("Length", 8, 64, 32)
        if st.button("GENERATE"):
            chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*"
            pwd = "".join(random.choice(chars) for _ in range(length))
            st.code(pwd)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with t2:
        st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
        st.subheader("💰 ROI CALC")
        inv = st.number_input("Invested ($)", 1000)
        ret = st.number_input("Returned ($)", 1500)
        roi = ((ret - inv) / inv) * 100
        st.metric("ROI", f"{roi:.2f}%")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with t3:
        st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
        st.subheader("🌐 SPEEDTEST (SIM)")
        st.metric("DOWNLOAD", f"{random.randint(500, 900)} Mbps")
        st.metric("UPLOAD", f"{random.randint(400, 800)} Mbps")
        if st.button("RUN TEST"): st.toast("TESTING...")
        st.markdown('</div>', unsafe_allow_html=True)


# --- MODULE 10: MASTER COMMAND (God Mode Web) ---
def render_master_dashboard():
    # Read the Ultimate God Mode Client file
    try:
        with open("dashboard.html", "r", encoding="utf-8") as f:
            html_code = f.read()
        
        # Render the file directly
        # height=950 ensures it covers most of the standard 1080p viewport inside Streamlit
        st.components.v1.html(html_code, height=950, scrolling=False)
        
    except FileNotFoundError:
        st.error("🚨 ERROR: dashboard.html not found. Please ensure the client file is in the root directory.")


# --- MAIN DISPATCHER ---
if "COMMAND" in view_mode:
    render_command_dashboard()
elif "AGENTS" in view_mode:
    render_agents_dashboard()
elif "LIBRARY" in view_mode:
    render_library()
elif "TERMINAL" in view_mode:
    render_terminal()
elif "COMMS" in view_mode:
    render_comms()
elif "TOOLS" in view_mode:
    render_tools()
elif "MASTER" in view_mode:
    render_master_dashboard()

# --- AUTO-REFRESH FORCE ---
time.sleep(refresh_rate)
st.rerun()
