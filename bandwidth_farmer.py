"""
BANDWIDTH FARMER - Project Monolith v5.4
Purpose: Keep passive income bandwidth apps alive (Grass, Honeygain, Pawns).
"""

import json
import psutil
import subprocess
import os
from pathlib import Path
from datetime import datetime

class BandwidthFarmer:
    def __init__(self):
        self.sentinel_dir = Path(__file__).parent.parent.parent / "Sentinels"
        self.sentinel_dir.mkdir(exist_ok=True)
        self.log_file = self.sentinel_dir / "bandwidth_farmer.status"
        
        # Define the apps we expect to farm with
        self.apps = {
            "Grass": {
                "process": "Grass.exe", 
                "path": os.path.expandvars(r"%LOCALAPPDATA%\Grass\Grass.exe") 
            },
            "Honeygain": {
                "process": "Honeygain.exe", 
                "path": os.path.expandvars(r"%LOCALAPPDATA%\Honeygain\Honeygain.exe")
            },
            "Pawns": {
                "process": "pawns-app.exe", 
                "path": os.path.expandvars(r"%PROGRAMFILES%\Pawns.app\pawns-app.exe")
            } 
        }

    def find_running_apps(self):
        """Scan process list for our apps"""
        running_apps = {}
        
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                p_name = proc.info['name']
                for app_name, app_info in self.apps.items():
                    if app_info["process"].lower() in p_name.lower():
                        running_apps[app_name] = "RUNNING"
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
                
        # Fill in MISSING for any not found
        for app in self.apps:
            if app not in running_apps:
                running_apps[app] = "STOPPED"
                
        return running_apps

    def launch_app(self, app_name, app_info):
        """Attempt to launch the application"""
        path = app_info.get("path")
        if path and os.path.exists(path):
            print(f"[BANDWIDTH] 🚀 Launching {app_name}...")
            try:
                subprocess.Popen([path], shell=True)
                return True
            except Exception as e:
                print(f"[BANDWIDTH] ❌ Failed to launch {app_name}: {e}")
        return False

    def run_check(self):
        running_statuses = self.find_running_apps()
        
        active_count = sum(1 for status in running_statuses.values() if status == "RUNNING")

        # Attempt auto-fix
        for app, status in running_statuses.items():
            if status == "STOPPED":
                if self.launch_app(app, self.apps[app]):
                    running_statuses[app] = "STARTING..."
        
        
        status_data = {
            "agent": "bandwidth_farmer",
            "timestamp": datetime.now().isoformat(),
            "apps_monitored": running_statuses,
            "active_count": active_count,
            "message": f"{active_count}/{len(self.apps)} Passive Apps Running"
        }
        
        with open(self.log_file, 'w') as f:
            json.dump(status_data, f, indent=2)
            
        print(f"[BANDWIDTH] Status: {status_data['message']}")
        return status_data

if __name__ == "__main__":
    farmer = BandwidthFarmer()
    status = farmer.run_check()
    print(json.dumps(status, indent=2))
