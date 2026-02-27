"""
MONEY BUTTON - INSTANT REVENUE TRIGGER
Project Monolith v6.0
Action: Forces execution of all Revenue Streams immediately.
"""
import subprocess
import sys
import json
import io
import time
from pathlib import Path
from datetime import datetime

# Fix Windows console encoding
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

class MoneyButton:
    def __init__(self):
        self.root = Path(__file__).parent.parent
        self.agents_dir = self.root / "Agents"
        self.sentinel_dir = self.root / "Sentinels"
        
        self.revenue_agents = [
            "Active/ionet_manager.py",          # Stream: Crypto (Solana)
            "bounty_arbitrageur.py",     # Stream: Nuclei Swarm (Bounties)
            "cloud_arbitrage.py",        # Stream: Compute Vault (Resale)
            "content_agency.py",         # Stream: GEO Hegemony (Affiliate)
            "web_gig_scanner.py"         # Stream: Freelance Gigs
        ]
        
    def press(self):
        print("\n" + "🟢"*15)
        print("  💲 MONEY BUTTON PRESSED  💲")
        print("🟢"*15 + "\n")
        
        total_payout_est = 0.0
        
        for agent_rel_path in self.revenue_agents:
            script_path = self.agents_dir / agent_rel_path
            
            if not script_path.exists():
                print(f"⚠️ MISSING: {script_path.name}")
                continue
                
            print(f"🚀 TRIGGERING: {script_path.name}...")
            start = time.time()
            
            try:
                # Run the agent
                result = subprocess.run(
                    ["python", str(script_path)],
                    capture_output=True,
                    text=True,
                    timeout=60,
                    encoding='utf-8' # Force utf-8 reading
                )
                
                # Check Sentinel for results
                sentinel_name = script_path.stem + ".done"
                sentinel_file = self.sentinel_dir / sentinel_name
                
                value = 0.0
                status = "UNKNOWN"
                
                if sentinel_file.exists():
                    try:
                        data = json.loads(sentinel_file.read_text(encoding='utf-8'))
                        status = data.get("status", "UNKNOWN")
                        # Try to extract value from message or specific fields
                        import re
                        msg = data.get("message", "")
                        # Simple regex to find $ amounts
                        amounts = re.findall(r'\$([\d,]+\.?\d*)', msg)
                        if amounts:
                             # Sum up found amounts (rough estimate)
                             value = sum(float(a.replace(",", "")) for a in amounts)
                        
                        # Special handling for known agents
                        if "cloud_arbitrage" in sentinel_name:
                             # Value is per hr * 24
                             count = data.get("opportunities_found", 0)
                             value = count * 40.0 # Daily est
                             
                        if "bounty" in sentinel_name:
                             # Already extracted in message usually, but let's be safe
                             pass
                             
                    except Exception as e:
                        print(f"   (Sentinel Read Error: {e})")
                
                if result.returncode == 0:
                    print(f"   ✅ EXECUTED ({time.time()-start:.1f}s) | Status: {status}")
                    if value > 0:
                        print(f"   💰 Est. Yield: ${value:,.2f}")
                        total_payout_est += value
                else:
                    print(f"   ❌ FAILED")
                    print(result.stderr[:200])   
                    
            except Exception as e:
                print(f"   🔥 ERROR: {e}")
                
        print("\n" + "="*40)
        print(f"💵 TOTAL SESSION YIELD (EST): ${total_payout_est:,.2f}")
        print("="*40 + "\n")

if __name__ == "__main__":
    MoneyButton().press()
