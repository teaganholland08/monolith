# FILE: monolith_launcher.py
# PURPOSE: "Do It For Me" - Automated Scheduling & Management
# STATUS: ACTIVE

import time
import schedule
import os
import sys
from auto_monolith import run_cycle

# CONFIGURATION
# How often to hunt for new trends? (Every 6 hours is safe)
SEARCH_INTERVAL_HOURS = 6

def job():
    print(f"\n[CLOCK] {time.strftime('%Y-%m-%d %H:%M:%S')} - INITIATING CYCLE...")
    try:
        # 1. CHECK TREASURY (Placeholder for Balance Check)
        # if balance > 1000: set_investor_mode(True)
        
        # 2. RUN THE ENGINE
        run_cycle()
        
        print("[CLOCK] CYCLE COMPLETE. SLEEPING...")
    except Exception as e:
        print(f"[ERROR] CYCLE FAILED: {e}")

def start_daemon():
    print(f"🤖 MONOLITH LAUNCHER INITIALIZED.")
    print(f"📅 SCHEDULE: RUNNING EVERY {SEARCH_INTERVAL_HOURS} HOURS.")
    print("--------------------------------------------------")
    
    # Run immediately on start
    job()
    
    # Schedule future runs
    schedule.every(SEARCH_INTERVAL_HOURS).hours.do(job)
    
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    # Ensure dependencies are present
    try:
        import schedule
    except ImportError:
        print("Installing scheduler...")
        os.system(f"{sys.executable} -m pip install schedule")
        import schedule

    start_daemon()
