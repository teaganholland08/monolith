# PROJECT MONOLITH // OMEGA

## OPERATIONAL MANUAL & SURVIVAL GUIDE

You have the **Code** (The Brain & Body).
Now you have the **Manual** (The Soul).

This document covers every missing dependency, hidden configuration, and operational secret needed to run the Monolith System without failure.

---

### 1. THE HIDDEN DEPENDENCIES

**CRITICAL**: The Python Brain (`server.py`) cannot start without these libraries.
Open your terminal (Command Prompt/PowerShell) and run this single command to install the full suite:

```bash
pip install flask flask-cors psutil feedparser requests imaplib2 pushbullet.py yfinance
```

#### The Stack

* **flask & flask-cors**: Creates the local web server (Port 5000).
* **psutil**: Reads hardware vitals (CPU, RAM, Disk, Battery).B
* **feedparser**: Ingests RSS feeds (BBC News).
* **requests**: Fetches Weather data (OpenMeteo).
* **imaplib2**: advanced Gmail connection handling.
* **pushbullet.py**: Mirrors SMS/Notifications from Android.
* **yfinance**: Real-time Market Data (Stocks/Crypto).

---

### 2. THE API KEY CHECKLIST ("Keys to the Kingdom")

The system is locked by default. You must edit `server.py` and input your specific credentials.

| Service | Where to get it | What it does |
| :--- | :--- | :--- |
| **Gmail App Password** | Google Account > Security > 2-Step > App Passwords | Allows reading unread emails. |
| **Pushbullet Key** | pushbullet.com > Settings > Create Access Token | Mirrors SMS to Dashboard. |
| **OpenMeteo** | *No Key Needed* | Weather Data (Latitude/Longitude). |
| **Yahoo Finance** | *No Key Needed* | Stock/Crypto Data via `yfinance`. |

> **[!] CRITICAL GMAIL NOTE**: You **cannot** use your normal login password. Google block automation. You MUST generate 16-character "App Password".

---

### 3. LAUNCH PROTOCOL

The **Brain** must be active before the **Body** can move.

#### STEP 1: START THE BRAIN

1. Open Terminal.
2. Navigate to folder: `cd "C:\Users\Teagan Holland\Desktop\Master Architecture"`
3. Run the Core: `py -3.13 server.py`
4. **Wait** until you see: `* Running on http://127.0.0.1:5000`
5. *Do not close this window.*

#### STEP 2: START THE BODY

1. Go to your Desktop folder.
2. Double-click `dashboard.html`.
3. The **Boot Sequence** will trigger.
4. If charts/data load, the Neural Link is established.

---

### 4. VOICE COMMAND MANUAL (JARVIS PROTOCOL)

The Dashboard is listening. Use these "Trigger Words" to control the environment.
*(Note: Click the **Monolith Logo** once to enable Microphone permissions)*

| Command | Action |
| :--- | :--- |
| **"STATUS"** | Voice Report: CPU, RAM, Bio-Metrics, Systems Check. |
| **"DEPLOY"** | Triggers deployment sequence (Animation + Log Entry). |
| **"RED" / "ALERT"** | Activates **PROTOCOL RED** (Emergency Theme / Lighting). |
| **"BLUE" / "NORMAL"** | Returns to standard operating configuration. |
| **"REBOOT"** | Hard refresh of the interface and boot sequence. |

---

### 5. TROUBLESHOOTING

* **"Waiting for Input..." (Forever)**: The Python Server is down. Check your terminal.
* **"Weather says --"**: API Timeout or Offline. It retries every 60s.
* **"Voice not working"**: Check Browser Permissions (Lock icon in URL bar) -> Allow Microphone.
* **"Email not showing"**: Check `server.py` terminal output. `imaplib.error` usually means a wrong App Password.

---

*SYSTEM IS YOURS.*
