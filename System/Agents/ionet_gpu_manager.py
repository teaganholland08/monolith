"""
IO.NET GPU MANAGER - Project Monolith v5.5
Manages GPU rental on io.net for AI training/inference workloads.
Target: $1200-2400/month from RTX 5090 rental at $2-5/hour.
"""

import json
import subprocess
import psutil
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional

class IoNetGPUManager:
    def __init__(self):
        self.root = Path(__file__).parent.parent
        self.sentinel_dir = self.root / "Sentinels"
        self.memory_dir = self.root / "Memory"
        self.config_dir = self.root.parent / "Config"
        self.sentinel_dir.mkdir(parents=True, exist_ok=True)
        self.memory_dir.mkdir(parents=True, exist_ok=True)
        self.status_file = self.sentinel_dir / "ionet_gpu_manager.done"
        self.config = self._load_config()

    def _load_config(self) -> Dict:
        config_file = self.config_dir / "ionet_config.json"
        if config_file.exists():
            return json.loads(config_file.read_text())
        return {
            "wallet_address": None,
            "min_price_per_hour": 0.5,
            "max_price_per_hour": 2.5,
            "device_name": f"monolith_node_{datetime.now().strftime('%M%S')}"
        }

    def start_worker(self) -> Dict:
        """Download and start the IO.net worker"""
        print("[IO.NET] 🚀 Attempting to start worker...")
        
        # 1. Load Config (Wallet/User ID)
        config_file = self.root.parent / "Config" / "ionet_config.json"
        
        # AUTO-FIX: Generate wallet if missing
        if not config_file.exists() or "wallet_address" not in json.loads(config_file.read_text()):
            print("[IO.NET] ⚠️  No wallet found. Auto-generating Sovereign Wallet...")
            try:
                from System.Agents.wallet_generator import SovereignWalletGenerator
                SovereignWalletGenerator().run()
            except ImportError:
                 # Fallback if class not importable directly
                 subprocess.run([sys.executable, str(self.root / "Agents" / "wallet_generator.py")], check=True)
        
        if not config_file.exists():
             return {"status": "error", "message": "Failed to generate wallet config."}

        config = json.loads(config_file.read_text())
        wallet = config.get("wallet_address")
        
        if not wallet:
             return {"status": "error", "message": "No wallet address in config."}

        # 2. Check for Docker (Required for IO.net)
        # For Windows, we assume Docker Desktop is installed or we use the binary script
        # IO.net provides a binary for Windows too. Let's try to establish which mode to use.
        
        device_name = f"monolith_node_{datetime.now().strftime('%M%S')}"
        
        # WINDOWS SPECIFIC LAUNCH
        # Ideally we check for docker:
        docker_available = False
        try:
            subprocess.run(["docker", "--version"], check=True, capture_output=True)
            docker_available = True
        except:
            pass

        if docker_available:
            cmd = f"docker run -d --restart=always --gpus all --name ionet-worker io-net/worker:latest --wallet {wallet} --device_name {device_name}"
            print(f"   -> Executing Docker: {cmd}")
            try:
                proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                return self._save_process_info(proc.pid, device_name, wallet, "docker")
            except Exception as e:
                return {"status": "error", "message": f"Docker launch failed: {e}"}
        else:
            # Fallback: Open Browser to download executable (User Assist)
            print("[IO.NET] ⚠️  Docker not found. Falling back to Binary/Browser download.")
            import webbrowser
            launch_url = f"https://cloud.io.net/worker/devices?wallet={wallet}&name={device_name}&os=windows"
            webbrowser.open(launch_url)
            return {"status": "waiting_user", "message": "Opened IO.Net download page. Please install worker manually."}

    def _save_process_info(self, pid, device_name, wallet, mode):
        data = {
            "pid": pid,
            "start_time": datetime.now().isoformat(),
            "device_name": device_name,
            "wallet": wallet,
            "mode": mode
        }
        with open(self.memory_dir / "worker_process.json", "w") as f:
            json.dump(data, f)
        return {"status": "running", "pid": pid, "message": f"{mode} command sent"}


    def check_worker_status(self) -> Dict:
        """Check if worker is running"""
        proc_file = self.memory_dir / "worker_process.json"
        
        if not proc_file.exists():
            return {"status": "not_running"}
        
        try:
            process_info = json.loads(proc_file.read_text())
            pid = process_info.get("pid")
            
            if pid and psutil.pid_exists(pid):
                return {
                    "status": "running",
                    **process_info
                }
            else:
                # Process dead? Check if we should restart?
                return {"status": "not_running", "message": "Process died"}
                
        except Exception as e:
            return {"status": "error", "message": f"Status check failed: {e}"}
    
    def estimate_daily_earnings(self) -> float:
        """Estimate daily earnings based on pricing"""
        avg_price = (self.config["min_price_per_hour"] + self.config["max_price_per_hour"]) / 2
        # Assume 18 hours/day utilization (75%)
        utilization_hours = 18
        return avg_price * utilization_hours
    
    def run(self):
        """Main execution"""
        print("[IO.NET] 💎 GPU Monetization Manager")
        
        # Check worker status
        status = self.check_worker_status()
        
        if status["status"] == "not_running":
            # Try to start worker
            result = self.start_worker()
            
            if result and result["status"] == "running":
                daily_estimate = self.estimate_daily_earnings()
                monthly_estimate = daily_estimate * 30
                
                print(f"[IO.NET] 💰 Estimated earnings: ${daily_estimate:.2f}/day (${monthly_estimate:.2f}/month)")
                
                self._report("GREEN", f"Worker active - est. ${monthly_estimate:.2f}/mo")
                
                return {
                    "status": "active",
                    "daily_estimate": daily_estimate,
                    "monthly_estimate": monthly_estimate
                }
            else:
                self._report("YELLOW", result.get("message", "Setup required"))
                return result
        else:
            print(f"[IO.NET] ✅ Worker already running (PID: {status.get('pid')})")
            self._report("GREEN", "Worker running")
            
            return {
                "status": "active",
                "worker_pid": status.get("pid")
            }
    
    def _report(self, status, message):
        """Report to sentinel"""
        data = {
            "agent": "ionet_gpu_manager",
            "status": status,
            "message": message,
            "estimated_monthly": self.estimate_daily_earnings() * 30,
            "timestamp": datetime.now().isoformat()
        }
        
        with open(self.sentinel_dir / "ionet_gpu_manager.done", 'w') as f:
            json.dump(data, f, indent=2)

if __name__ == "__main__":
    manager = IoNetGPUManager()
    result = manager.run()
    
    print("\n" + "=" * 60)
    print("🎮 IO.NET GPU MANAGER - STATUS")
    print("=" * 60)
    
    if result.get("status") == "active":
        if "daily_estimate" in result:
            print(f"💰 Daily Estimate: ${result['daily_estimate']:.2f}")
            print(f"💰 Monthly Estimate: ${result['monthly_estimate']:.2f}")
        print("✅ Worker active and earning")
    else:
        print(f"⚠️ Status: {result.get('status', 'unknown')}")
        print(f"💡 {result.get('message', 'Check configuration')}")
    
    print("=" * 60)
