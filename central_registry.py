"""
CENTRAL REGISTRY - Project Monolith v5.5 (Global)
Purpose: The "Phone Book" and "Event Bus" for the Global Agent Network.
Functionality: 
- Agents register their capabilities here.
- Agents query this to find other capable agents.
- Central coordination point for the "Kill Switch".
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

class CentralRegistry:
    def __init__(self):
        self.root = Path(__file__).parent.parent
        self.registry_file = self.root / "Agents" / "registry.json"
        
        # Ensure registry exists
        if not self.registry_file.exists():
            self._save_registry({"agents": {}, "events": [], "kill_switch": False})

    def _load_registry(self) -> Dict:
        try:
            with open(self.registry_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {"agents": {}, "events": [], "kill_switch": False}

    def _save_registry(self, data: Dict):
        with open(self.registry_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)

    def register_agent(self, agent_name: str, capabilities: List[str], contact_point: str = "local"):
        """
        Registers an agent's existence and skills.
        """
        data = self._load_registry()
        
        data["agents"][agent_name] = {
            "status": "ACTIVE",
            "capabilities": capabilities,
            "contact_point": contact_point,
            "last_heartbeat": datetime.now().isoformat()
        }
        
        print(f"[REGISTRY] ✅ Registered Agent: {agent_name}")
        self._save_registry(data)

    def find_agent_by_capability(self, capability: str) -> List[str]:
        """
        Returns a list of agent names that have the requested capability.
        """
        data = self._load_registry()
        matches = []
        for name, info in data["agents"].items():
            if capability in info.get("capabilities", []) and info.get("status") == "ACTIVE":
                matches.append(name)
        return matches

    def post_event(self, source_agent: str, event_type: str, payload: Dict):
        """
        Publishes an event to the bus.
        """
        data = self._load_registry()
        
        event = {
            "id": f"evt_{datetime.now().timestamp()}",
            "source": source_agent,
            "type": event_type,
            "payload": payload,
            "timestamp": datetime.now().isoformat()
        }
        
        # Keep only last 50 events to avoid bloat
        data["events"].append(event)
        if len(data["events"]) > 50:
            data["events"] = data["events"][-50:]
            
        print(f"[REGISTRY] 📢 Event: {event_type} from {source_agent}")
        self._save_registry(data)

    def check_kill_switch(self) -> bool:
        """
        Returns True if the global kill switch is active (STOP EVERYTHING).
        """
        data = self._load_registry()
        return data.get("kill_switch", False)
        
    def set_kill_switch(self, active: bool):
        data = self._load_registry()
        data["kill_switch"] = active
        self._save_registry(data)
        state = "ENGAGED" if active else "DISENGAGED"
        print(f"[REGISTRY] ⚠️ KILL SWITCH {state} ⚠️")

if __name__ == "__main__":
    # Test Run
    registry = CentralRegistry()
    registry.register_agent("test_agent_01", ["testing", "debug"])
    registry.post_event("test_agent_01", "TEST_EVENT", {"message": "Hello World"})
    print(f"Agents with 'testing': {registry.find_agent_by_capability('testing')}")
