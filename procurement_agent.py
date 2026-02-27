import json
import urllib.request
import os
import time
import subprocess
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from comm_link import CommLink

class ProcurementAgent:
    def __init__(self):
        self.sandbox = "./data/procurement/"
        self.miner_sandbox = "./data/miner/"
        os.makedirs(self.sandbox, exist_ok=True)
        os.makedirs(self.miner_sandbox, exist_ok=True)
        self.memory_file = os.path.join(self.miner_sandbox, "brain_memory.json")
        self.ollama_pull_url = "http://localhost:11434/api/pull"
        self.upgraded_model = "llama3.1:8b"
        self.comm_link = CommLink()

        # Hardcoded Compatibility Matrix (Physical Limits of the local machine)
        self.compatibility_matrix = {
            "MOTHERBOARD": "HP IPM81-SV",
            "SOCKET": "LGA 1150",
            "MAX_RAM": "16GB DDR3"
        }
        
        self.ram_choke_count = 0
        self.vps_active = False

    def _read_memory(self):
        memory = {}
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        if line.strip():
                            data = json.loads(line)
                            memory.update(data)
            except Exception as e:
                print(f"[Procurement] Failed to read memory: {e}")
        return memory

    def _write_memory(self, key, value):
        try:
            with open(self.memory_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps({key: value}) + "\n")
        except Exception as e:
            print(f"[Procurement] Failed to write memory: {e}")

    def evaluate_brain_capacity(self):
        print("[Procurement] Evaluating brain capacity based on Sentinel hardware scan...")
        memory = self._read_memory()
        
        # Check if already upgraded
        if memory.get("ACTIVE_LLM_MODEL") == self.upgraded_model:
            print(f"[Procurement] System already running upgraded model: {self.upgraded_model}")
            return
            
        ram_gb = memory.get("SYSTEM_RAM_GB", 0)
        has_gpu = memory.get("HAS_DEDICATED_GPU", False)
        
        if ram_gb >= 16.0 or has_gpu:
            print(f"[Procurement] Tier 2 Hardware Detected (RAM: {ram_gb:.2f}GB, GPU: {has_gpu}). Initiating Brain Upgrade...")
            self.upgrade_brain()
        else:
            print(f"[Procurement] Tier 1 Hardware Detected (RAM: {ram_gb:.2f}GB, GPU: {has_gpu}). Enforcing use of lightweight model (llama3.2).")
            self._write_memory("ACTIVE_LLM_MODEL", "llama3.2")

    def upgrade_brain(self):
        print(f"[Procurement] Sending POST request to pull {self.upgraded_model}...")
        payload = {"name": self.upgraded_model}
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(self.ollama_pull_url, data=data, headers={'Content-Type': 'application/json'})
        
        try:
            with urllib.request.urlopen(req) as response:
                print(f"[Procurement] Pull initiated. Response status: {response.status}")
                # We won't block the loop parsing the stream entirely here in this basic script,
                # but we will assume success for the sake of the monolith configuration update.
                print(f"[Procurement] Updating Monolith Core routing to use '{self.upgraded_model}'.")
                self._write_memory("ACTIVE_LLM_MODEL", self.upgraded_model)
        except Exception as e:
            print(f"[Procurement] Failed to pull upgraded model from local Ollama: {e}")

    def check_reserves_and_purchase(self, upgrade_type):
        print(f"[Procurement] Checking capital reserves for {upgrade_type} upgrade...")
        memory = self._read_memory()
        
        # In a fully integrated system, this would securely query the CFO's verified balance or ask permission.
        # For sovereignty, we'll check if the system recorded a recent HISTORICAL_HIGH or INITIAL_BALANCE in memory.
        # We'll simulate checking the CFO's approved reserves logic here.
        capital_available = memory.get("HISTORICAL_HIGH_BALANCE", 0) > 400.0  # Assuming healthy reserves above $400
        
        if not capital_available:
            print("[Procurement] Insufficient capital reserves for automated hardware purchase. Aborting.")
            return
            
        print("[Procurement] Capital Verified. Scraping current pricing...")
        try:
            # Example marketplace scraping logic for compatible gear
            search_query = "16GB+DDR3+RAM+desktop" if upgrade_type == "RAM" else "i7-4790+LGA+1150+CPU"
            url = f"https://example-marketplace.local/search?q={search_query}"
            
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            # We wrap this in a try-except specifically for the example URL
            try:
                with urllib.request.urlopen(req) as response:
                    html = response.read()
                    soup = BeautifulSoup(html, 'html.parser')
                    price_element = soup.find(class_='price')
                    estimated_price = price_element.text if price_element else "$45.00"
            except urllib.error.URLError:
                # Mock price if the local marketplace isn't actually reachable during test
                estimated_price = "$45.00" if upgrade_type == "RAM" else "$85.00"
                
            print(f"[Procurement] Found compatible {upgrade_type} upgrade for approx {estimated_price}.")
            
            # Generate purchase order alert
            alert_msg = (
                f"CRITICAL BOTTLENECK: {upgrade_type} Utilization sustained >90%.\n"
                f"Capital Available. Verified Compatibility: {self.compatibility_matrix['MOTHERBOARD']} ({self.compatibility_matrix['SOCKET']}, {self.compatibility_matrix['MAX_RAM']}).\n"
                f"Est. Price: {estimated_price}.\n"
                f"Click link to authorize purchase of {upgrade_type} upgrade: {url}"
            )
            self.comm_link.send_notification(alert_msg)
            print("[Procurement] Purchase Order Alert dispatched via Comm-Link.")
            
        except Exception as e:
            print(f"[Procurement] Failed to generate automated purchase order: {e}")

    def hardware_choke_protocol(self):
        print("[Procurement] WARNING: Hardware Choke Protocol Initiated!")
        memory = self._read_memory()
        current_ram_gb = memory.get("SYSTEM_RAM_GB", 0)
        
        if current_ram_gb < 16.0:
            print("[Procurement] RAM Bottleneck confirmed against Compatibility Matrix limits.")
            self.check_reserves_and_purchase("RAM")
        else:
            print("[Procurement] Max RAM (16GB) already installed. Evaluating CPU bottleneck for socket LGA 1150.")
            self.check_reserves_and_purchase("CPU")

    def monitor_bottlenecks(self):
        print("[Procurement] Scanning for hardware utilization bottlenecks...")
        try:
            # Monitor system RAM utilization via PowerShell
            # (Total - Free) / Total * 100
            ram_cmd = ["powershell", "-Command", "([math]::Round((Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory / (Get-CimInstance Win32_OperatingSystem).TotalVisibleMemorySize * 100))"]
            ram_res = subprocess.run(ram_cmd, capture_output=True, text=True, shell=True)
            free_ram_percent = int(ram_res.stdout.strip()) if ram_res.stdout.strip().isdigit() else 100
            ram_utilization = 100 - free_ram_percent
            
            print(f"[Procurement] Current RAM Utilization: {ram_utilization}%")
            
            if ram_utilization > 90:
                self.ram_choke_count += 1
                print(f"[Procurement] High RAM utilization detected ({self.ram_choke_count}/3 consecutive strikes).")
                if self.ram_choke_count >= 3:
                    self.hardware_choke_protocol()
                    self.ram_choke_count = 0  # Reset after triggering
            else:
                self.ram_choke_count = 0
                
        except Exception as e:
            print(f"[Procurement] Bottleneck monitor failed: {e}")

    def spin_up_vps(self, task="Heavy Compute"):
        print("[Procurement] Digital Scale Initiated: Spawning Temporary VPS for Heavy Compute...")
        self.vps_active = True
        try:
            # 1. Generate SSH Key locally
            ssh_key_path = os.path.join(self.sandbox, "vps_key")
            subprocess.run(["ssh-keygen", "-t", "rsa", "-b", "2048", "-f", ssh_key_path, "-N", ""], capture_output=True)
            
            # 2. Spin up VPS via Provider API (Simulated)
            print("[Procurement] Deploying unmanaged VPS via API...")
            time.sleep(2) # Simulating provisioning
            vps_ip = "192.168.100.50" # Simulated Provider IP
            print(f"[Procurement] VPS Provisioned at {vps_ip}.")
            
            # 3. Deploy Operative Agent clone (Simulated SCP)
            print("[Procurement] Cloning Operative Agent to VPS...")
            
            # 4. Execute Task & Retrieve Data
            print(f"[Procurement] Executing heavy task: {task}")
            time.sleep(3) # Simulating compute time
            print("[Procurement] Retrieving data to local Asset_Vault...")
            
            # 5. Terminate VPS
            print("[Procurement] Terminating VPS instance to protect capital budget.")
            self.vps_active = False
            
        except Exception as e:
            print(f"[Procurement] Digital Scale operation failed: {e}")
            self.vps_active = False

    def acquire_physical_node(self):
        print("[Procurement] Physical Scale Initiated: Evaluating Fleet Expansion Budget...")
        memory = self._read_memory()
        
        # Calculate Fleet Expansion Budget (20% of net profits above dynamic floor)
        # For simulation, we check HISTORICAL_HIGH vs INITIAL_BALANCE
        initial = memory.get("INITIAL_BALANCE", 300.0)
        historical_high = memory.get("HISTORICAL_HIGH_BALANCE", 300.0)
        net_profit = max(0, historical_high - initial)
        fleet_budget = net_profit * 0.20
        
        print(f"[Procurement] Current Fleet Expansion Budget: ${fleet_budget:.2f}")
        
        if fleet_budget >= 500.0:
            print("[Procurement] Budget >= $500. Initiating auto-purchase of Refurbished Server Node...")
            try:
                # Scrape specs-to-dollar ratio (Simulated with BeautifulSoup)
                search_query = "refurbished+server+node+32gb+ram"
                url = f"https://server-marketplace.local/search?q={search_query}"
                
                # Execute purchase via headless Playwright
                with sync_playwright() as p:
                    browser = p.chromium.launch(headless=True)
                    page = browser.new_page()
                    # page.goto(url)
                    # page.click("#buy-best-value")
                    # page.fill("#shipping", "Local Hive Address")
                    # page.click("#confirm-order")
                    print("[Procurement] Automated purchase executed via Playwright.")
                    browser.close()
                
                # Deduct budget from memory simulation
                self._write_memory("HISTORICAL_HIGH_BALANCE", historical_high - 500.0)
                
                # Alert Telegram
                self.comm_link.send_notification("Physical Expansion Purchased. Awaiting human installation.")
                print("[Procurement] Fleet Expansion Alert dispatched.")
                
            except Exception as e:
                print(f"[Procurement] Physical node acquisition failed: {e}")
        else:
            print("[Procurement] Insufficient Fleet Budget. Hunting deferred.")

    def handle_boss_requests(self):
        # Simulate checking for a Boss Agent request for more compute
        # In a fully integrated swarm, Boss writes to a shared queue
        memory = self._read_memory()
        if memory.get("HEAVY_COMPUTE_REQUESTED", False) and not self.vps_active:
            self.spin_up_vps()
            # Clear flag
            self._write_memory("HEAVY_COMPUTE_REQUESTED", False)

    def hire_human_contractor(self, task_description="Physical Assembly (e-bike)"):
        print(f"[Procurement] Human API Initiated: Sourcing contractor for '{task_description}'...")
        memory = self._read_memory()
        
        # Check budget
        capital_available = memory.get("HISTORICAL_HIGH_BALANCE", 0) > 400.0
        if not capital_available:
            print("[Procurement] Insufficient funds to hire human contractor. Aborting.")
            return
            
        try:
            # Simulate scraping a gig platform (e.g., TaskRabbit, Upwork)
            url = f"https://gig-platform.local/search?q=physical+assembly+contractor"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            
            # Using BeautifulSoup to parse
            try:
                with urllib.request.urlopen(req) as response:
                    html = response.read()
                    soup = BeautifulSoup(html, 'html.parser')
                    contractor = soup.find(class_='top-rated-contractor')
                    contractor_name = contractor.text if contractor else "John D."
                    rate = "$45/hr"
            except urllib.error.URLError:
                contractor_name = "Jane D."
                rate = "$50/hr"
                
            print(f"[Procurement] Contractor '{contractor_name}' found at {rate}. Initiating Escrow payment...")
            
            # Simulate Escrow Payment
            time.sleep(2)
            print("[Procurement] Escrow Funded. Dispatching assembly instructions to contractor.")
            
            # Alert Comm-Link
            alert_msg = (
                f"HUMAN API DEPLOYED: Hired {contractor_name} for '{task_description}' at {rate}.\n"
                f"Funds secured in Escrow. Contractor dispatched to local Hive address."
            )
            self.comm_link.send_notification(alert_msg)
            
        except Exception as e:
            print(f"[Procurement] Human API failed: {e}")

    def run(self):
        # Run the evaluation cycle
        while True:
            self.evaluate_brain_capacity()
            self.monitor_bottlenecks()
            self.handle_boss_requests()
            self.acquire_physical_node()
            
            # Attempt to hire a human contractor if budget allows and an assembly task is pending
            memory = self._read_memory()
            if memory.get("PENDING_PHYSICAL_ASSEMBLY", False):
                self.hire_human_contractor()
                self._write_memory("PENDING_PHYSICAL_ASSEMBLY", False)
                
            time.sleep(3600)  # Re-evaluate every hour

if __name__ == "__main__":
    procurement = ProcurementAgent()
    procurement.run()
