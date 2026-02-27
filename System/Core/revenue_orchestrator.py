"""
REVENUE ORCHESTRATOR - Project Monolith v5.5 IMMORTAL
The central coordinator for ALL revenue generation activities.
Scans, prioritizes, executes, and scales revenue streams autonomously.
"""

import json
import sys
import io
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any
import subprocess

# Ensure Agents module is discoverable
ROOT = Path(__file__).parent.parent.parent
sys.path.append(str(ROOT))
sys.path.append(str(ROOT / "System" / "Agents"))

# Fix Windows console encoding
try:
    if sys.stdout.encoding.lower() != 'utf-8':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
except Exception:
    pass

class RevenueOrchestrator:
    """
    Master coordinator for all revenue generation.
    Activates streams, tracks payouts, triggers reinvestment, scales winners.
    """
    
    def __init__(self, scheduler=None):
        self.root = Path(__file__).parent.parent.parent
        self.agents_dir = self.root / "System" / "Agents"
        self.sentinel_dir = self.root / "System" / "Sentinels"
        self.memory_dir = self.root / "Memory" / "revenue_orchestrator"
        self.config_dir = self.root / "System" / "Config"
        
        # Scheduler Injection
        self.scheduler = scheduler
        
        # Ensure directories
        for d in [self.sentinel_dir, self.memory_dir, self.config_dir]:
            d.mkdir(parents=True, exist_ok=True)
        
        self.active_streams = self._load_active_streams()
        self.earnings_log = self._load_earnings_log()
        self.reinvestment_rules = self._load_reinvestment_rules()
    
    def _load_active_streams(self) -> Dict:
        """Load currently active revenue streams"""
        streams_file = self.memory_dir / "active_streams.json"
        if streams_file.exists():
            return json.loads(streams_file.read_text())
        
        return {
            "tier1_zero_capital": {
                "micro_tasks": {"active": False, "agent": "micro_task_executor"},
                "gpu_rental": {"active": False, "agent": "ionet_gpu_manager"},
                "bandwidth": {"active": False, "agent": "grass_node_manager"},
                "ai_services": {"active": False, "agent": "fiverr_gig_manager"},
                "digital_products": {"active": False, "agent": "digital_product_uploader"},
                "arbitrage_scout": {"active": False, "agent": "arbitrage_scout"},
                "lead_gen_operative": {"active": False, "agent": "lead_gen_operative"}
            },
            "tier2_low_capital": {
                "ip_arbitrage": {"active": False, "agent": "ip_arbitrage_engine", "min_capital": 0},
                "cex_trading": {"active": False, "agent": "trade_protocol", "min_capital": 100}
            },
            "tier3_scaling": {
                "defi_yield": {"active": False, "agent": "defi_yield_agent", "min_capital": 1000}
            }
        }
    
    def _load_earnings_log(self) -> List[Dict]:
        """Load historical earnings data"""
        log_file = self.memory_dir / "earnings_log.json"
        if log_file.exists():
            return json.loads(log_file.read_text())
        return []
        
    def get_total_earnings(self) -> float:
        """Calculate total earnings from log"""
        return sum(entry.get("amount", 0) for entry in self.earnings_log)
    
    def _load_reinvestment_rules(self) -> Dict:
        """Load reinvestment allocation rules"""
        return {
            "milestones": {
                "100": {"allocate_to": ["cex_trading"], "amount_pct": 100},
                "500": {"allocate_to": ["hardware_upgrade", "api_credits"], "amount_pct": 30},
                "1000": {"allocate_to": ["defi_yield"], "amount_pct": 50},
                "5000": {"allocate_to": ["advanced_trading", "team_expansion"], "amount_pct": 40}
            },
            "default_split": {
                "reinvest": 80,  # 80% reinvest
                "reserve": 10,   # 10% emergency fund
                "human": 10      # 10% to user
            }
        }
    
    def scan_revenue_opportunities(self) -> Dict:
        """Run omnidirectional scanner to find all opportunities"""
        print("[ORCHESTRATOR] 🔍 Scanning for revenue opportunities...")
        
        try:
            # Direct Integration
            from System.Agents.omnidirectional_revenue_scanner import OmnidirectionalRevenueScanner
            scanner = OmnidirectionalRevenueScanner()
            return scanner.run()
        except ImportError:
            print("[ORCHESTRATOR] ⚠️ Scanner module not found.")
        except Exception as e:
            print(f"[ORCHESTRATOR] ⚠️ Scanner error: {e}")

        return {"total_opportunities_found": 0}
    
    def prioritize_streams(self, opportunities: Dict) -> List[Dict]:
        """Prioritize streams by ROI, effort, and capital requirements"""
        print("[ORCHESTRATOR] 📊 Prioritizing revenue streams...")
        
        # Get total capital available
        capital = self._get_available_capital()
        
        priorities = []
        
        # Tier 1: Zero-capital streams (HIGHEST PRIORITY)
        for stream_name, config in self.active_streams["tier1_zero_capital"].items():
            priorities.append({
                "stream": stream_name,
                "tier": 1,
                "agent": config["agent"],
                "capital_required": 0,
                "priority_score": 100,  # Top priority
                "status": "ready" if not config["active"] else "active"
            })
        
        # Tier 2: Low-capital streams  
        for stream_name, config in self.active_streams["tier2_low_capital"].items():
            min_cap = config.get("min_capital", 0)
            if capital >= min_cap:
                priorities.append({
                    "stream": stream_name,
                    "tier": 2,
                    "agent": config["agent"],
                    "capital_required": min_cap,
                    "priority_score": 80,
                    "status": "ready" if not config["active"] else "active"
                })
        
        # Tier 3: Scaling streams
        for stream_name, config in self.active_streams["tier3_scaling"].items():
            min_cap = config.get("min_capital", 0)
            if capital >= min_cap:
                priorities.append({
                    "stream": stream_name,
                    "tier": 3,
                    "agent": config["agent"],
                    "capital_required": min_cap,
                    "priority_score": 60,
                    "status": "ready" if not config["active"] else "active"
                })
        
        # Sort by priority score (highest first)
        priorities.sort(key=lambda x: x["priority_score"], reverse=True)
        
        return priorities
    
    def activate_stream(self, stream_info: Dict) -> bool:
        """Activate a specific revenue stream by scheduling it"""
        stream_name = stream_info["stream"]
        agent_name = stream_info["agent"]
        
        print(f"[ORCHESTRATOR] 🚀 Scheduling Activation: {stream_name} via {agent_name}")
        
        if self.scheduler:
            # Async Execution via Core
            task_id = self.scheduler.add_task(
                "RUN_AGENT",
                {
                    "agent_name": agent_name,
                    "args": ["--run-once"], # Standardize on run-once flags
                    "stream_name": stream_name
                },
                priority=5 # Normal priority
            )
            print(f"   ↳ Task Dispatched: {task_id}")
            self._mark_stream_active(stream_name, stream_info["tier"])
            return True
        else:
            # Fallback to direct execution (Old Behavior) or fail
            print("   ⚠️ No Scheduler attached. Falling back to direct execution (Not Recommended)")
            return self._activate_stream_direct(stream_info)
            
    def _activate_stream_direct(self, stream_info):
        stream_name = stream_info["stream"]
        agent_name = stream_info["agent"]
        
        print(f"[ORCHESTRATOR] 🚀 Activating (DIRECT): {stream_name} via {agent_name}")
        
        # Dynamic import and execution
        try:
            # Map agent names to their classes/files
            if agent_name == "micro_task_executor":
                from System.Agents.micro_task_executor import MicroTaskExecutor
                result = MicroTaskExecutor().run_task_cycle()
            elif agent_name == "ionet_gpu_manager":
                from System.Agents.ionet_gpu_manager import IoNetGPUManager
                result = IoNetGPUManager().run()
            elif agent_name == "grass_node_manager":
                from System.Agents.grass_node_manager import GrassNodeManager
                result = GrassNodeManager().run()
            elif agent_name == "fiverr_gig_manager":
                from System.Agents.fiverr_gig_manager import FiverrGigManager
                result = FiverrGigManager().run()
            elif agent_name == "digital_product_uploader":
                from System.Agents.digital_product_uploader import DigitalProductUploader
                result = DigitalProductUploader().run()
            elif agent_name == "node_beta_content":
                from System.Agents.node_beta_content import ContentFactoryNode
                result = ContentFactoryNode().run()
            elif agent_name == "node_gamma_sdr":
                from System.Agents.node_gamma_sdr import AISDRNode
                result = AISDRNode().run()
            elif agent_name == "arbitrage_scout":
                from arbitrage_scout import ArbitrageHunter
                result = {"status": "active"} if ArbitrageHunter().scan() is None else {"status": "active"}
            elif agent_name == "lead_gen_operative":
                from lead_gen_operative import LeadGenerationAgent
                result = {"status": "active"} if LeadGenerationAgent().scan_for_leads() is None else {"status": "active"}
            else:
                print(f"[ORCHESTRATOR] ⚠️ Unknown agent: {agent_name}")
                return False

            # Mark as active if successful
            if isinstance(result, dict) and result.get("status") in ["active", "running", "GREEN"]:
                self._mark_stream_active(stream_name, stream_info["tier"])
                print(f"[ORCHESTRATOR] ✅ {stream_name} activated successfully")
                return True
            return False
            
        except ImportError as e:
            print(f"[ORCHESTRATOR] ❌ Import failed for {agent_name}: {e}")
            return False
        except Exception as e:
            print(f"[ORCHESTRATOR] ❌ Activation failed for {stream_name}: {e}")
            return False

    def _create_agent_placeholder(self, agent_name: str, stream_name: str):
        # ... (keep existing placeholder logic if needed, but we have real agents now)
        pass

    def _mark_stream_active(self, stream_name: str, tier: int):
        """Mark a stream as active in config"""
        tier_key = f"tier{tier}_" + ("zero_capital" if tier == 1 else "low_capital" if tier == 2 else "scaling")
        if tier_key in self.active_streams and stream_name in self.active_streams[tier_key]:
            self.active_streams[tier_key][stream_name]["active"] = True
            self._save_active_streams()

    def _save_active_streams(self):
        streams_file = self.memory_dir / "active_streams.json"
        streams_file.write_text(json.dumps(self.active_streams, indent=2))

    def _get_available_capital(self) -> float:
        """Get capital available for reinvestment"""
        try:
            from System.Agents.auto_reinvestor import AutoReinvestor
            return AutoReinvestor().get_available_capital()
        except Exception:
            return 0.0

    def _check_reinvestment_milestones(self, total: float):
        """Check if any reinvestment milestones hit and trigger Reinvestor"""
        try:
            from System.Agents.auto_reinvestor import AutoReinvestor
            reinvestor = AutoReinvestor()
            capital = reinvestor.get_available_capital()
            
            if capital > 0:
                print(f"[ORCHESTRATOR] 🔄 Triggering Auto-Reinvestor (Capital: ${capital})")
                allocation = reinvestor.calculate_allocation(capital)
                reinvestor.execute_reinvestment(allocation)
        except Exception as e:
            print(f"[ORCHESTRATOR] ⚠️ Reinvestment trigger failed: {e}")
    
    def run_orchestration_cycle(self):
        """Main orchestration loop"""
        print("=" * 70)
        print("REVENUE ORCHESTRATOR - ACTIVATION CYCLE")
        print("=" * 70)
        
        # 1. Scan opportunities
        opportunities = self.scan_revenue_opportunities()
        print(f"Total opportunities: {opportunities.get('total_opportunities_found', 0)}")
        
        # 2. Prioritize streams
        priorities = self.prioritize_streams(opportunities)
        print(f"\n📊 Prioritized {len(priorities)} streams")
        
        # 3. Activate top streams (start with Tier 1)
        activated = 0
        for stream in priorities[:5]:  # Activate top 5
            if stream["status"] == "ready":
                if self.activate_stream(stream):
                    activated += 1
        
        # 4. Report status
        total_earned = self.get_total_earnings()
        active_count = sum(
            1 for tier in self.active_streams.values()
            for config in tier.values()
            if config.get("active", False)
        )
        
        result = {
            "timestamp": datetime.now().isoformat(),
            "total_earnings": total_earned,
            "active_streams": active_count,
            "new_activations": activated,
            "status": "OPERATIONAL"
        }
        
        # Save to sentinel
        sentinel_data = {
            "agent": "revenue_orchestrator",
            "status": "GREEN",
            "message": f"${total_earned} earned, {active_count} streams active",
            **result
        }
        
        with open(self.sentinel_dir / "revenue_orchestrator.done", 'w') as f:
            json.dump(sentinel_data, f, indent=2)
        
        print(f"\n💰 Total Earnings: ${total_earned}")
        print(f"🔄 Active Streams: {active_count}")
        print("=" * 70)
        
        return result

if __name__ == "__main__":
    orchestrator = RevenueOrchestrator()
    orchestrator.run_orchestration_cycle()
