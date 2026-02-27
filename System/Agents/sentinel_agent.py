import subprocess
import time
import os
import sys
import json
import re
from comm_link import CommLink

class SentinelAgent:
    def __init__(self):
        self.sandbox = "./data/sentinel/"
        self.miner_sandbox = "./data/miner/"
        os.makedirs(self.sandbox, exist_ok=True)
        os.makedirs(self.miner_sandbox, exist_ok=True)
        self.memory_file = os.path.join(self.miner_sandbox, "brain_memory.json")
        self.comm_link = CommLink()

    def enforce_network_perimeter(self):
        print("[Sentinel] Configuring Ironclad OS-Level Firewall...")
        try:
            # Rule 1: Block inbound connections to python.exe except from localhost
            python_path = sys.executable
            
            # Remove any existing rules with this name to prevent duplicates
            subprocess.run(["netsh", "advfirewall", "firewall", "delete", "rule", "name=Monolith_Python_Block"], capture_output=True)
            subprocess.run(["netsh", "advfirewall", "firewall", "delete", "rule", "name=Monolith_Python_AllowLocal"], capture_output=True)
            
            # Allow strictly 127.0.0.1
            subprocess.run([
                "netsh", "advfirewall", "firewall", "add", "rule", 
                "name=Monolith_Python_AllowLocal", "dir=in", "action=allow", 
                f"program={python_path}", "remoteip=127.0.0.1"
            ], capture_output=True)
            
            # Block all other inbound for this executable
            subprocess.run([
                "netsh", "advfirewall", "firewall", "add", "rule", 
                "name=Monolith_Python_Block", "dir=in", "action=block", 
                f"program={python_path}"
            ], capture_output=True)
            
            # Rule 2: Explicitly block Ports 11434 (Ollama) and Dashboard (assuming 8000 for dashboard) from external
            subprocess.run(["netsh", "advfirewall", "firewall", "delete", "rule", "name=Monolith_Port_Block"], capture_output=True)
            subprocess.run([
                "netsh", "advfirewall", "firewall", "add", "rule", 
                "name=Monolith_Port_Block", "dir=in", "action=block", 
                "protocol=TCP", "localport=11434,8000"
            ], capture_output=True)
            
            print("[Sentinel] Firewall rules enforced via netsh.")
        except Exception as e:
            print(f"[Sentinel] Failed to configure firewall: {e}")

    def monitor_connections(self):
        print("[Sentinel] Active Connection Monitor sweeping perimeter...")
        try:
            # Get all process IDs associated with python (simulating swarm PIDs)
            pid_cmd = ["powershell", "-Command", "Get-Process -Name python,ollama | Select-Object -ExpandProperty Id"]
            pid_res = subprocess.run(pid_cmd, capture_output=True, text=True, shell=True)
            swarm_pids = [pid.strip() for pid in pid_res.stdout.split('\n') if pid.strip().isdigit()]
            
            # Run netstat to check connections
            netstat = subprocess.run(["netstat", "-ano"], capture_output=True, text=True)
            
            for line in netstat.stdout.split('\n'):
                if "TCP" in line and "ESTABLISHED" in line:
                    parts = line.split()
                    if len(parts) >= 5:
                        proto, local_addr, remote_addr, state, pid = parts[0], parts[1], parts[2], parts[3], parts[4]
                        
                        # Check if connection belongs to swarm
                        if pid in swarm_pids:
                            remote_ip = remote_addr.split(':')[0]
                            # If connection is established from outside localhost to our processes
                            if remote_ip != "127.0.0.1" and remote_ip != "0.0.0.0":
                                print(f"[Sentinel] 🚨 FOREIGN CONNECTION DETECTED! IP: {remote_ip} on PID {pid}")
                                
                                # Instantly drop the connection by terminating the exact process (or using CurrPorts/TCPKill logic; here we drop process for safety)
                                subprocess.run(["taskkill", "/F", "/PID", pid], capture_output=True)
                                print(f"[Sentinel] Terminated PID {pid} to drop outer connection.")
                                
                                # Log threat
                                threat_log = os.path.join(self.sandbox, "threat_intel.json")
                                entry = {"timestamp": time.time(), "foreign_ip": remote_ip, "targeted_pid": pid, "action": "DROPPED"}
                                with open(threat_log, 'a') as f:
                                    f.write(json.dumps(entry) + "\n")
                                
                                # Send Telegram Alert
                                self.comm_link.send_notification(f"🚨 Perimeter Breach Blocked! Foreign IP {remote_ip} attempted to connect to Swarm PID {pid}. Process terminated and logged.")
                                
        except Exception as e:
             print(f"[Sentinel] Connection monitor error: {e}")
    def guard_hardware(self):
        print("[Sentinel] Hardware guard active. Monitoring MSAcpi_ThermalZoneTemperature...")
        self.enforce_network_perimeter()
        self.poll_hardware()
        
        # Track cycles for netstat sweeps (runs every 3rd cycle = ~45 seconds)
        cycle = 0
        while True:
            temp = self.get_cpu_temp()
            print(f"[Sentinel] Current CPU Temp: {temp:.2f}°C")
            if temp > 80.0:
                print("[Sentinel] CRITICAL: Temperature exceeds 80°C. Terminating Ollama to save motherboard!")
                subprocess.run(["taskkill", "/F", "/IM", "ollama.exe"], capture_output=True)
                subprocess.run(["taskkill", "/F", "/IM", "ollama_llama_server.exe"], capture_output=True)
                
            cycle += 1
            if cycle >= 3:
                self.monitor_connections()
                cycle = 0
                
            time.sleep(15)

if __name__ == "__main__":
    sentinel = SentinelAgent()
    sentinel.guard_hardware()
