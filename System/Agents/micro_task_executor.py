"""
MICRO-TASK EXECUTOR - Project Monolith v5.5 (REAL MONEY MODE)
Automates micro-task completion via REAL APIs (MTurk) and Companion Workflows.
Target: $500-2000/month from RLHF, data labeling, and AI training tasks.
"""

import json
import time
import webbrowser
import boto3
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
from rich.console import Console
from rich.prompt import Confirm
from rich.panel import Panel

console = Console()

class MicroTaskExecutor:
    """
    Executes micro-tasks via Real APIs.
    - Tier 1: Amazon MTurk (via Boto3 API)
    - Tier 2: Manual "Companion Mode" for Outlier/Appen (Browser Automation Assistance)
    """
    
    def __init__(self):
        self.root = Path(__file__).parent.parent
        self.sentinel_dir = self.root / "Sentinels"
        self.memory_dir = self.root.parent / "Memory" / "micro_task_executor"
        self.config_dir = self.root / "Config"
        
        for d in [self.sentinel_dir, self.memory_dir]:
            d.mkdir(parents=True, exist_ok=True)
        
        self.platforms = self._load_platform_config()
        self.completed_tasks = self._load_task_history()
        self.mturk_client = None

    def _load_platform_config(self) -> Dict:
        config_file = self.config_dir / "micro_tasks.json"
        if config_file.exists():
            return json.loads(config_file.read_text())
        return {}

    def _load_task_history(self) -> List[Dict]:
        history_file = self.memory_dir / "task_history.json"
        if history_file.exists():
            return json.loads(history_file.read_text())
        return []

    def _init_mturk(self):
        """Initialize connection to Amazon MTurk via Boto3"""
        config = self.platforms.get("mturk", {})
        if not config.get("enabled"):
            return False

        if "YOUR_AWS" in str(config.get("access_key")):
            console.print("[yellow]⚠️ MTurk enabled but Keys are placeholders. Please update System/Config/micro_tasks.json[/yellow]")
            return False

        try:
            self.mturk_client = boto3.client(
                'mturk',
                region_name=config.get('region', 'us-east-1'),
                aws_access_key_id=config.get('access_key'),
                aws_secret_access_key=config.get('secret_key')
            )
            # Connectivity check
            balance = self.mturk_client.get_account_balance()
            console.print(f"[green]✅ MTurk Connected. Balance: {balance['AvailableBalance']}[/green]")
            return True
        except Exception as e:
            console.print(f"[red]❌ MTurk Connection Failed: {e}[/red]")
            return False

    def scan_available_tasks(self, platform: str) -> List[Dict]:
        """Fetch REAL tasks from APIs"""
        if platform == "mturk" and self.mturk_client:
            try:
                response = self.mturk_client.list_hits(
                    MaxResults=10,
                    Reward={"Comparator": "GreaterThan", "Value": "0.01"}
                )
                hits = response.get('HITs', [])
                tasks = []
                for hit in hits:
                    tasks.append({
                        "id": hit['HITId'],
                        "title": hit['Title'],
                        "platform": "mturk",
                        "pay": float(hit['Reward']),
                        "details": hit['Description'],
                        "url": f"https://worker.mturk.com/projects/{hit['HITGroupId']}/tasks"
                    })
                return tasks
            except Exception as e:
                console.print(f"[red]Error fetching HITs: {e}[/red]")
                return []
        
        elif platform in ["outlier", "appen"]:
            # Companion Mode: Suggest "Do a task now?" to user
            return [{
                "id": f"manual_{platform}_{int(time.time())}",
                "title": f"Manual Session: {platform.title()}",
                "platform": platform,
                "pay": "Variable",
                "details": "Launch browser and work for 20 mins",
                "url": self.platforms[platform].get("setup_url")
            }]
            
        return []

    def execute_task(self, task: Dict) -> Optional[Dict]:
        """Execute task: API accept or Manual Browser Launch"""
        
        console.print(f"\n[bold blue]🔨 Task Selected: {task['title']} ({task['pay']})[/bold blue]")
        
        if task['platform'] == "mturk":
            console.print(f"   [dim]Ref: {task['url']}[/dim]")
            # For MTurk, complex tasks usually require browser anyway.
            # We open it for the user to complete.
            webbrowser.open(task['url'])
            console.print("[green]   -> Opened in Browser. Complete it there.[/green]")
            return None # Cannot verify API completion easily without local server
            
        else:
            # Manual Companion Mode
            if Confirm.ask(f"Open {task['platform']} to start earning?"):
                webbrowser.open(task['url'])
                console.print(f"[green]   -> Launched {task['platform']}.[/green]")
                console.print("[yellow]   Waiting for you to complete a task...[/yellow]")
                
                # Mock result for manual confirmation
                earned = console.input("   [bold]Enter amount earned (or 0 if skipped): $[/bold] ")
                try:
                    earned_val = float(earned)
                    if earned_val > 0:
                        return {
                            "task_id": task["id"],
                            "status": "completed",
                            "earnings": earned_val,
                            "timestamp": datetime.now().isoformat(),
                            "platform": task["platform"]
                        }
                except:
                    pass
        return None

    def _report_earnings(self, result: Dict):
        """Report earnings to central tracking"""
        earnings_file = self.memory_dir.parent / "revenue_orchestrator" / "earnings_log.json"
        earnings_file.parent.mkdir(parents=True, exist_ok=True)
        
        earnings_log = []
        if earnings_file.exists():
            earnings_log = json.loads(earnings_file.read_text())
        
        earnings_log.append({
            "timestamp": result["timestamp"],
            "stream": "micro_tasks",
            "amount": result["earnings"],
            "currency": "USD",
            "platform": result["platform"]
        })
        
        earnings_file.write_text(json.dumps(earnings_log, indent=2))
        self.completed_tasks.append(result)
        self._save_task_history()

    def _save_task_history(self):
        history_file = self.memory_dir / "task_history.json"
        history_file.write_text(json.dumps(self.completed_tasks, indent=2))

    def run_task_cycle(self):
        """Main execution loop"""
        console.rule("[bold green]MICRO-TASK EXECUTOR (REAL MONEY)[/bold green]")
        
        # 1. Init APIs
        mturk_active = self._init_mturk()
        
        # 2. Check other platforms
        enabled_platforms = [p for p, c in self.platforms.items() if c.get('enabled') and p != 'mturk']
        if mturk_active: enabled_platforms.append('mturk')
        
        if not enabled_platforms:
            console.print(Panel("[red]NO PLATFORMS ENABLED[/red]\nUpdate System/Config/micro_tasks.json"))
            return {"status": "setup_required"}

        total_earned = 0
        
        for platform in enabled_platforms:
            tasks = self.scan_available_tasks(platform)
            if not tasks:
                continue
                
            for task in tasks[:3]: # Limit to top 3 suggestions
                result = self.execute_task(task)
                if result:
                    self._report_earnings(result)
                    total_earned += result['earnings']
        
        console.print(f"\n[bold green]💰 Session Total: ${total_earned}[/bold green]")
        return {"status": "completed", "earned": total_earned}

if __name__ == "__main__":
    executor = MicroTaskExecutor()
    executor.run_task_cycle()
