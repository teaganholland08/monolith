"""
UNIVERSAL AGENT FACTORY - Project Monolith v5.0 IMMORTAL
The factory that can spawn ANY agent for ANY domain in the world.
"""
import os
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
import json

# Add project root to path
ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT))

from universal_domain_registry import DOMAINS, SENTINEL_TYPES, get_all_agent_names, get_domain_count
from agent_templates import TEMPLATES, get_template, format_template


class AgentFactory:
    """
    Universal Agent Factory - Creates agents for ANY domain.
    
    Capabilities:
    - Spawn individual agents for any domain/specialization
    - Spawn entire domain swarms
    - Spawn all agents in the registry
    - Create custom agents with specific archetypes
    """
    
    def __init__(self):
        self.root = ROOT
        self.agents_dir = self.root / "System" / "Agents"
        self.sentinels_dir = self.root / "System" / "Sentinels"
        self.generated_dir = self.agents_dir / "Generated"
        self.domain_dirs = {}
        
        # Ensure directories exist
        self.agents_dir.mkdir(parents=True, exist_ok=True)
        self.sentinels_dir.mkdir(parents=True, exist_ok=True)
        self.generated_dir.mkdir(parents=True, exist_ok=True)
        
        # Create domain subdirectories
        for domain in DOMAINS.keys():
            domain_dir = self.generated_dir / domain.title()
            domain_dir.mkdir(exist_ok=True)
            self.domain_dirs[domain] = domain_dir
        
        self.spawn_log: List[Dict] = []
    
    def spawn_agent(self, domain: str, specialization: str, 
                    archetype: str = "reactive", overwrite: bool = False) -> Path:
        """
        Spawn a single agent for a specific domain and specialization.
        
        Args:
            domain: Domain category (e.g., 'finance', 'health')
            specialization: Specific area (e.g., 'trading', 'diagnosis')
            archetype: Agent archetype ('reactive', 'goal_based', 'learning', 'utility', 'swarm')
            overwrite: Whether to overwrite existing agent
            
        Returns:
            Path to the created agent file
        """
        if domain not in DOMAINS:
            raise ValueError(f"Unknown domain: {domain}. Available: {list(DOMAINS.keys())}")
        
        if specialization not in DOMAINS[domain]:
            raise ValueError(f"Unknown specialization: {specialization} for domain {domain}")
        
        # Get template and format it
        template = get_template(archetype)
        code = format_template(template, domain, specialization)
        
        # Determine output path
        agent_name = f"{domain}_{specialization}_agent"
        output_dir = self.domain_dirs.get(domain, self.generated_dir)
        output_path = output_dir / f"{agent_name}.py"
        
        if output_path.exists() and not overwrite:
            print(f"[FACTORY] Agent exists: {agent_name} (use overwrite=True to replace)")
            return output_path
        
        # Write agent file
        output_path.write_text(code, encoding='utf-8')
        
        # Log spawn
        self.spawn_log.append({
            "agent": agent_name,
            "domain": domain,
            "specialization": specialization,
            "archetype": archetype,
            "path": str(output_path),
            "timestamp": datetime.now().isoformat()
        })
        
        print(f"[FACTORY] Spawned: {agent_name} ({archetype})")
        return output_path
    
    def spawn_sentinel(self, domain: str, sentinel_type: str, overwrite: bool = False) -> Path:
        """
        Spawn a sentinel for a domain.
        """
        if domain not in DOMAINS:
            raise ValueError(f"Unknown domain: {domain}")
        
        if sentinel_type not in SENTINEL_TYPES:
            raise ValueError(f"Unknown sentinel type: {sentinel_type}")
        
        sentinel_name = f"{domain}_{sentinel_type}"
        output_path = self.sentinels_dir / f"{sentinel_name}.py"
        
        if output_path.exists() and not overwrite:
            return output_path
        
        # Create sentinel code
        code = f'''"""
{sentinel_name.upper()} - DOMAIN SENTINEL
Domain: {domain} | Type: {sentinel_type}
Generated: {datetime.now().isoformat()}
"""
import json
from pathlib import Path
from datetime import datetime

class {sentinel_name.replace("_", " ").title().replace(" ", "")}:
    """Sentinel monitoring {domain} domain for {sentinel_type}."""
    
    def __init__(self):
        self.root = Path(__file__).parent.parent
        self.domain = "{domain}"
        self.sentinel_type = "{sentinel_type}"
        self.agents_dir = self.root / "Agents" / "Generated" / "{domain.title()}"
        self.output_dir = self.root / "Sentinels"
        self.output_dir.mkdir(exist_ok=True)
    
    def scan(self):
        """Scan domain agents and report status."""
        agents = list(self.agents_dir.glob("*.py")) if self.agents_dir.exists() else []
        
        status = "GREEN"
        alerts = []
        
        for agent in agents:
            # Check if agent has reported
            sentinel_file = self.output_dir / f"{{agent.stem}}.done"
            if sentinel_file.exists():
                try:
                    data = json.loads(sentinel_file.read_text())
                    if data.get("status") == "RED":
                        status = "RED"
                        alerts.append(agent.stem)
                except:
                    pass
        
        return {{
            "domain": self.domain,
            "type": self.sentinel_type,
            "status": status,
            "agents_monitored": len(agents),
            "alerts": alerts
        }}
    
    def run(self):
        result = self.scan()
        self._report(result["status"], result)
        return result
    
    def _report(self, status, data):
        report = {{
            "sentinel": "{sentinel_name}",
            "status": status,
            "data": data,
            "timestamp": datetime.now().isoformat()
        }}
        with open(self.output_dir / "{sentinel_name}.done", 'w') as f:
            json.dump(report, f, indent=2)

if __name__ == "__main__":
    {sentinel_name.replace("_", " ").title().replace(" ", "")}().run()
'''
        output_path.write_text(code, encoding='utf-8')
        print(f"[FACTORY] Spawned Sentinel: {sentinel_name}")
        return output_path
    
    def spawn_domain(self, domain: str, archetype: str = "reactive", 
                     overwrite: bool = False) -> List[Path]:
        """Spawn all agents for a specific domain."""
        if domain not in DOMAINS:
            raise ValueError(f"Unknown domain: {domain}")
        
        paths = []
        for spec in DOMAINS[domain]:
            path = self.spawn_agent(domain, spec, archetype, overwrite)
            paths.append(path)
        
        # Also spawn sentinels for this domain
        for sentinel_type in SENTINEL_TYPES:
            self.spawn_sentinel(domain, sentinel_type, overwrite)
        
        print(f"[FACTORY] Domain '{domain}' complete: {len(paths)} agents + {len(SENTINEL_TYPES)} sentinels")
        return paths
    
    def spawn_all(self, archetype: str = "reactive", overwrite: bool = False) -> Dict:
        """
        SPAWN EVERY AGENT AND SENTINEL IN THE WORLD.
        
        This creates agents for ALL domains and ALL specializations.
        """
        print("=" * 60)
        print("🌍 UNIVERSAL AGENT GENESIS - SPAWNING ALL AGENTS")
        print("=" * 60)
        
        stats = get_domain_count()
        print(f"Target: {stats['potential_agents']} agents + {stats['potential_sentinels']} sentinels")
        print()
        
        all_paths = {}
        total_agents = 0
        total_sentinels = 0
        
        for domain in DOMAINS.keys():
            print(f"[{domain.upper()}] Spawning {len(DOMAINS[domain])} agents...")
            
            paths = []
            for spec in DOMAINS[domain]:
                path = self.spawn_agent(domain, spec, archetype, overwrite)
                paths.append(path)
                total_agents += 1
            
            # Spawn sentinels
            for sentinel_type in SENTINEL_TYPES:
                self.spawn_sentinel(domain, sentinel_type, overwrite)
                total_sentinels += 1
            
            all_paths[domain] = paths
        
        print()
        print("=" * 60)
        print(f"✅ GENESIS COMPLETE")
        print(f"   Agents Created: {total_agents}")
        print(f"   Sentinels Created: {total_sentinels}")
        print(f"   Total: {total_agents + total_sentinels}")
        print("=" * 60)
        
        # Save spawn manifest
        manifest = {
            "timestamp": datetime.now().isoformat(),
            "total_agents": total_agents,
            "total_sentinels": total_sentinels,
            "domains": {d: len(p) for d, p in all_paths.items()},
            "archetype": archetype
        }
        manifest_path = self.generated_dir / "GENESIS_MANIFEST.json"
        manifest_path.write_text(json.dumps(manifest, indent=2))
        
        return {
            "agents": total_agents,
            "sentinels": total_sentinels,
            "paths": all_paths,
            "manifest": str(manifest_path)
        }
    
    def list_domains(self) -> Dict[str, List[str]]:
        """List all available domains and their specializations."""
        return DOMAINS
    
    def get_stats(self) -> Dict:
        """Get factory statistics."""
        return get_domain_count()


# === CONVENIENCE FUNCTIONS ===

def spawn(domain: str, spec: str, archetype: str = "reactive") -> Path:
    """Quick spawn a single agent."""
    return AgentFactory().spawn_agent(domain, spec, archetype)

def spawn_all(archetype: str = "reactive") -> Dict:
    """Spawn all agents in the world."""
    return AgentFactory().spawn_all(archetype)

def list_domains() -> Dict[str, List[str]]:
    """List all domains."""
    return AgentFactory().list_domains()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Universal Agent Factory")
    parser.add_argument("--spawn-all", action="store_true", help="Spawn all agents")
    parser.add_argument("--domain", type=str, help="Spawn all agents for a domain")
    parser.add_argument("--agent", type=str, help="Spawn specific agent (format: domain.spec)")
    parser.add_argument("--archetype", type=str, default="reactive", 
                        choices=["reactive", "goal_based", "learning", "utility", "swarm"])
    parser.add_argument("--stats", action="store_true", help="Show registry stats")
    parser.add_argument("--list", action="store_true", help="List all domains")
    
    args = parser.parse_args()
    factory = AgentFactory()
    
    if args.stats:
        stats = factory.get_stats()
        print(f"📊 Registry Stats:")
        print(f"   Domains: {stats['domains']}")
        print(f"   Specializations: {stats['specializations']}")
        print(f"   Potential Agents: {stats['potential_agents']}")
        print(f"   Potential Sentinels: {stats['potential_sentinels']}")
    
    elif args.list:
        for domain, specs in factory.list_domains().items():
            print(f"\n{domain.upper()} ({len(specs)} specializations):")
            print(f"  {', '.join(specs)}")
    
    elif args.spawn_all:
        factory.spawn_all(args.archetype)
    
    elif args.domain:
        factory.spawn_domain(args.domain, args.archetype)
    
    elif args.agent:
        parts = args.agent.split(".")
        if len(parts) == 2:
            agent_path = factory.spawn_agent(parts[0], parts[1], args.archetype)
            
            # Execute the generated agent
            import subprocess
            import os
            print(f"[FACTORY] Bootstrapping Agent: {agent_path.name}")
            
            kwargs = {}
            if os.name == 'nt':
                kwargs['creationflags'] = subprocess.CREATE_NO_WINDOW
                
            log_path = factory.generated_dir.parent / f"{agent_path.stem}_execution.log"
            
            with open(log_path, "a") as log_file:
                subprocess.Popen(["python", str(agent_path)], stdout=log_file, stderr=subprocess.STDOUT, **kwargs)
            
            # Log to telemetry for dashboard
            try:
                telemetry = {
                    "agent": agent_path.stem,
                    "status": "ONLINE",
                    "earnings": 0.0,
                    "timestamp": datetime.now().isoformat()
                }
                with open("agent_telemetry.json", "a") as f:
                    f.write(json.dumps(telemetry) + "\n")
            except Exception as e:
                print(f"[FACTORY] Telemetry log failed: {e}")
                
        else:
            print("Agent format: domain.specialization (e.g., finance.trading)")
    
    else:
        parser.print_help()
