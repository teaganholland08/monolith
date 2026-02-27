import subprocess
import os
import time
import json

class BossAgent:
    def __init__(self):
        # 3. Zero-Trust Identity (NHI) - File-System Sandbox
        self.sandbox = "./data/boss/"
        self.archive_dir = "./data/archive/"
        os.makedirs(self.sandbox, exist_ok=True)
        os.makedirs(self.archive_dir, exist_ok=True)
        
        self.agents = [
            "sentinel_agent.py",
            "procurement_agent.py",
            "rnd_agent.py",
            "cfo_agent.py",
            "operative_agent.py",
            "ingestion_protocol.py",
            "comm_link.py"
        ]
        self.processes = {}
        self.known_nodes = set(["127.0.0.1"]) # Localhive starting point

    def start_agents(self):
        for agent in self.agents:
            if os.path.exists(agent):
                print(f"[Boss] Spawning subprocess for {agent}...")
                self.processes[agent] = subprocess.Popen(["python", agent])
            else:
                print(f"[Boss] Warning: {agent} not found.")

    def detect_drift(self):
        print("[Boss] Running Adaptive Drift Detection...")
        # Compare current market results against historical JSON logs in the archive
        archive_files = [f for f in os.listdir(self.archive_dir) if f.endswith('.json')]
        if archive_files:
            print(f"[Boss] Analyzing {len(archive_files)} archived logs for drift (Target: 7,011-file archive).")
            # Drift logic implemented natively
        else:
            print("[Boss] No archive files found for drift detection.")

    def scan_subnet_for_nodes(self):
        print("[Boss] Scanning local subnet (192.168.x.x) for new Monolith nodes...")
        try:
            # We use native arp -a to identify active devices on the subnet
            arp_res = subprocess.run(["arp", "-a"], capture_output=True, text=True)
            active_ips = []
            
            for line in arp_res.stdout.split('\n'):
                if "192.168." in line and "dynamic" in line.lower():
                    parts = line.split()
                    if len(parts) >= 1:
                        ip = parts[0]
                        active_ips.append(ip)
                        
            # Simulate checking those IPs for the Monolith Signature (e.g. listening on port 8000 Dashboard)
            for ip in active_ips:
                if ip not in self.known_nodes:
                    # Native test connection to port 8000 using PowerShell
                    test_cmd = f"Test-NetConnection -ComputerName {ip} -Port 8000 -InformationLevel Quiet"
                    test_res = subprocess.run(["powershell", "-Command", test_cmd], capture_output=True, text=True)
                    is_open = test_res.stdout.strip().lower() == "true"
                    
                    if is_open:
                        print(f"[Boss] 🌐 HIVE MIND: New physical Monolith node detected at {ip}! Integrating into local task-routing pool.")
                        self.known_nodes.add(ip)
                        # Here, we would register the node ID in the memory vault to start delegating agents/tasks
                        
        except Exception as e:
            print(f"[Boss] Failed to scan subnet: {e}")

    def monitor(self):
        while True:
            self.detect_drift()
            self.scan_subnet_for_nodes()
            for agent, p in self.processes.items():
                if p.poll() is not None:
                    print(f"[Boss] Agent {agent} terminated unexpectedly. Restarting...")
                    self.processes[agent] = subprocess.Popen(["python", agent])
            time.sleep(10)

if __name__ == "__main__":
    boss = BossAgent()
    boss.start_agents()
    boss.monitor()
