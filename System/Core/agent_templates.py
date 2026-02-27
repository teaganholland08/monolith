"""
AGENT TEMPLATES - Project Monolith v5.0 IMMORTAL
Templates for all agent archetypes following 2026 AI standards.
"""

from datetime import datetime

# === AGENT ARCHETYPE TEMPLATES ===

REACTIVE_TEMPLATE = '''"""
{agent_name} - REACTIVE AGENT
Domain: {domain} | Specialization: {spec}
Type: Simple Reflex Agent - Stimulus/Response pattern
Generated: {timestamp}
"""
import json
from pathlib import Path
from datetime import datetime

class {class_name}:
    """
    Reactive Agent: Responds to immediate stimuli based on condition-action rules.
    No memory of past states - pure stimulus/response.
    """
    def __init__(self):
        self.root = Path(__file__).parent.parent
        self.sentinel_dir = self.root / "Sentinels"
        self.sentinel_dir.mkdir(exist_ok=True)
        self.rules = self._load_rules()
    
    def _load_rules(self):
        """Load condition-action rules for this domain."""
        return {{
            "default": lambda x: self._default_action(x)
        }}
    
    def _default_action(self, percept):
        return {{"action": "processed", "input": str(percept)[:100]}}
    
    def perceive(self, environment):
        """Get current percepts from environment."""
        return environment
    
    def act(self, percept):
        """React to percept based on rules."""
        for condition, action in self.rules.items():
            if condition == "default" or self._matches(percept, condition):
                return action(percept)
        return self._default_action(percept)
    
    def _matches(self, percept, condition):
        return condition in str(percept)
    
    def run(self, environment=None):
        percept = self.perceive(environment or {{}})
        result = self.act(percept)
        self._report("GREEN", f"Processed: {{result}}")
        return result
    
    def _report(self, status, message):
        data = {{
            "agent": "{agent_name}",
            "type": "reactive",
            "domain": "{domain}",
            "status": status,
            "message": message,
            "timestamp": datetime.now().isoformat()
        }}
        with open(self.sentinel_dir / "{agent_name}.done", 'w') as f:
            json.dump(data, f, indent=2)

if __name__ == "__main__":
    {class_name}().run()
'''

GOAL_BASED_TEMPLATE = '''"""
{agent_name} - GOAL-BASED AGENT
Domain: {domain} | Specialization: {spec}
Type: Goal-Based Agent - Plans actions to achieve objectives
Generated: {timestamp}
"""
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

class {class_name}:
    """
    Goal-Based Agent: Plans sequences of actions to achieve goals.
    Considers future consequences of actions.
    """
    def __init__(self):
        self.root = Path(__file__).parent.parent
        self.sentinel_dir = self.root / "Sentinels"
        self.memory_dir = self.root.parent / "Memory" / "{agent_name}"
        self.sentinel_dir.mkdir(exist_ok=True)
        self.memory_dir.mkdir(parents=True, exist_ok=True)
        
        self.goals: List[Dict] = []
        self.plan: List[str] = []
        self.state: Dict[str, Any] = {{}}
    
    def set_goal(self, goal: Dict):
        """Set a goal to achieve."""
        self.goals.append(goal)
    
    def plan_actions(self) -> List[str]:
        """Create a plan to achieve goals."""
        plan = []
        for goal in self.goals:
            steps = self._decompose_goal(goal)
            plan.extend(steps)
        self.plan = plan
        return plan
    
    def _decompose_goal(self, goal: Dict) -> List[str]:
        """Break down goal into actionable steps."""
        return [f"step_{{i}}_for_{{goal.get('name', 'unknown')}}" for i in range(3)]
    
    def execute_plan(self) -> Dict:
        """Execute the planned actions."""
        results = []
        for step in self.plan:
            result = self._execute_step(step)
            results.append(result)
            self.state[step] = result
        return {{"completed": len(results), "results": results}}
    
    def _execute_step(self, step: str) -> Dict:
        """Execute a single step."""
        return {{"step": step, "status": "completed"}}
    
    def run(self, goals=None):
        if goals:
            for g in goals:
                self.set_goal(g)
        
        if not self.goals:
            self.set_goal({{"name": "default_{spec}_goal", "priority": 1}})
        
        self.plan_actions()
        result = self.execute_plan()
        self._report("GREEN", f"Goals achieved: {{len(self.goals)}}")
        return result
    
    def _report(self, status, message):
        data = {{
            "agent": "{agent_name}",
            "type": "goal_based",
            "domain": "{domain}",
            "status": status,
            "message": message,
            "goals_completed": len(self.goals),
            "timestamp": datetime.now().isoformat()
        }}
        with open(self.sentinel_dir / "{agent_name}.done", 'w') as f:
            json.dump(data, f, indent=2)

if __name__ == "__main__":
    {class_name}().run()
'''

LEARNING_TEMPLATE = '''"""
{agent_name} - LEARNING AGENT
Domain: {domain} | Specialization: {spec}
Type: Learning Agent - Improves from experience
Generated: {timestamp}
"""
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

class {class_name}:
    """
    Learning Agent: Improves performance over time through experience.
    Has learning element, performance element, critic, and problem generator.
    """
    def __init__(self):
        self.root = Path(__file__).parent.parent
        self.sentinel_dir = self.root / "Sentinels"
        self.memory_dir = self.root.parent / "Memory" / "{agent_name}"
        self.sentinel_dir.mkdir(exist_ok=True)
        self.memory_dir.mkdir(parents=True, exist_ok=True)
        
        self.knowledge_base: Dict[str, Any] = self._load_knowledge()
        self.experience_log: List[Dict] = []
        self.performance_history: List[float] = []
    
    def _load_knowledge(self) -> Dict:
        """Load existing knowledge from memory."""
        kb_path = self.memory_dir / "knowledge_base.json"
        if kb_path.exists():
            return json.loads(kb_path.read_text())
        return {{"rules": [], "patterns": [], "feedback": []}}
    
    def _save_knowledge(self):
        """Persist knowledge to memory."""
        kb_path = self.memory_dir / "knowledge_base.json"
        kb_path.write_text(json.dumps(self.knowledge_base, indent=2))
    
    def perceive(self, environment: Dict) -> Dict:
        """Observe the environment."""
        return environment
    
    def perform(self, percept: Dict) -> Dict:
        """Take action based on current knowledge."""
        # Use knowledge base to make decision
        action = self._select_action(percept)
        result = self._execute_action(action)
        return result
    
    def _select_action(self, percept: Dict) -> str:
        """Select best action based on knowledge."""
        # Simple pattern matching against knowledge
        for pattern in self.knowledge_base.get("patterns", []):
            if pattern.get("trigger") in str(percept):
                return pattern.get("action", "default_action")
        return "default_action"
    
    def _execute_action(self, action: str) -> Dict:
        """Execute the selected action."""
        return {{"action": action, "success": True}}
    
    def learn(self, feedback: Dict):
        """Learn from feedback on performance."""
        self.knowledge_base["feedback"].append(feedback)
        
        # Extract new pattern if positive feedback
        if feedback.get("score", 0) > 0.7:
            pattern = {{
                "trigger": feedback.get("context", ""),
                "action": feedback.get("action", ""),
                "confidence": feedback.get("score", 0.5)
            }}
            self.knowledge_base["patterns"].append(pattern)
        
        self._save_knowledge()
    
    def critique(self, result: Dict) -> Dict:
        """Evaluate performance."""
        # Simple scoring based on result
        score = 1.0 if result.get("success") else 0.0
        self.performance_history.append(score)
        return {{"score": score, "result": result}}
    
    def generate_problems(self) -> List[Dict]:
        """Generate new problems to explore."""
        return [{{"type": "exploration", "domain": "{domain}"}}]
    
    def run(self, environment=None):
        env = environment or {{}}
        
        # Perceive
        percept = self.perceive(env)
        
        # Perform
        result = self.perform(percept)
        
        # Critique
        evaluation = self.critique(result)
        
        # Learn
        self.learn({{
            "context": str(percept)[:50],
            "action": result.get("action"),
            "score": evaluation.get("score", 0.5)
        }})
        
        self._report("GREEN", f"Learned from experience. Patterns: {{len(self.knowledge_base['patterns'])}}")
        return result
    
    def _report(self, status, message):
        data = {{
            "agent": "{agent_name}",
            "type": "learning",
            "domain": "{domain}",
            "status": status,
            "message": message,
            "patterns_learned": len(self.knowledge_base.get("patterns", [])),
            "timestamp": datetime.now().isoformat()
        }}
        with open(self.sentinel_dir / "{agent_name}.done", 'w') as f:
            json.dump(data, f, indent=2)

if __name__ == "__main__":
    {class_name}().run()
'''

UTILITY_TEMPLATE = '''"""
{agent_name} - UTILITY-BASED AGENT
Domain: {domain} | Specialization: {spec}
Type: Utility-Based Agent - Optimizes utility function
Generated: {timestamp}
"""
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

class {class_name}:
    """
    Utility-Based Agent: Maximizes a utility function.
    Makes trade-offs and optimizes outcomes.
    """
    def __init__(self):
        self.root = Path(__file__).parent.parent
        self.sentinel_dir = self.root / "Sentinels"
        self.sentinel_dir.mkdir(exist_ok=True)
        
        self.utility_weights = {{
            "efficiency": 0.3,
            "quality": 0.3,
            "speed": 0.2,
            "cost": 0.2
        }}
    
    def calculate_utility(self, state: Dict) -> float:
        """Calculate utility of a state."""
        utility = 0.0
        for factor, weight in self.utility_weights.items():
            utility += state.get(factor, 0.5) * weight
        return utility
    
    def get_possible_actions(self, state: Dict) -> List[Dict]:
        """Get all possible actions from current state."""
        return [
            {{"name": "action_a", "predicted_state": {{"efficiency": 0.8, "quality": 0.7, "speed": 0.6, "cost": 0.5}}}},
            {{"name": "action_b", "predicted_state": {{"efficiency": 0.6, "quality": 0.9, "speed": 0.4, "cost": 0.7}}}},
            {{"name": "action_c", "predicted_state": {{"efficiency": 0.7, "quality": 0.6, "speed": 0.9, "cost": 0.3}}}}
        ]
    
    def select_best_action(self, state: Dict) -> Dict:
        """Select action that maximizes expected utility."""
        actions = self.get_possible_actions(state)
        best_action = None
        best_utility = -float('inf')
        
        for action in actions:
            utility = self.calculate_utility(action["predicted_state"])
            if utility > best_utility:
                best_utility = utility
                best_action = action
        
        return {{"action": best_action, "expected_utility": best_utility}}
    
    def run(self, state=None):
        current_state = state or {{"efficiency": 0.5, "quality": 0.5, "speed": 0.5, "cost": 0.5}}
        
        selection = self.select_best_action(current_state)
        
        self._report("GREEN", f"Selected: {{selection['action']['name']}} (utility: {{selection['expected_utility']:.2f}})")
        return selection
    
    def _report(self, status, message):
        data = {{
            "agent": "{agent_name}",
            "type": "utility_based",
            "domain": "{domain}",
            "status": status,
            "message": message,
            "timestamp": datetime.now().isoformat()
        }}
        with open(self.sentinel_dir / "{agent_name}.done", 'w') as f:
            json.dump(data, f, indent=2)

if __name__ == "__main__":
    {class_name}().run()
'''

SWARM_TEMPLATE = '''"""
{agent_name} - SWARM AGENT
Domain: {domain} | Specialization: {spec}
Type: Swarm Agent - Coordinates with other agents
Generated: {timestamp}
"""
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List

class {class_name}:
    """
    Swarm Agent: Works as part of a collective.
    Coordinates with other agents to achieve complex goals.
    """
    def __init__(self, swarm_id="default"):
        self.root = Path(__file__).parent.parent
        self.sentinel_dir = self.root / "Sentinels"
        self.swarm_dir = self.root.parent / "Memory" / "swarm" / swarm_id
        self.sentinel_dir.mkdir(exist_ok=True)
        self.swarm_dir.mkdir(parents=True, exist_ok=True)
        
        self.swarm_id = swarm_id
        self.agent_id = "{agent_name}"
        self.neighbors: List[str] = []
    
    def broadcast(self, message: Dict):
        """Broadcast message to swarm."""
        msg_file = self.swarm_dir / f"{{self.agent_id}}_broadcast.json"
        message["from"] = self.agent_id
        message["timestamp"] = datetime.now().isoformat()
        msg_file.write_text(json.dumps(message, indent=2))
    
    def receive_messages(self) -> List[Dict]:
        """Receive messages from other swarm members."""
        messages = []
        for msg_file in self.swarm_dir.glob("*_broadcast.json"):
            if self.agent_id not in msg_file.name:
                try:
                    messages.append(json.loads(msg_file.read_text()))
                except:
                    pass
        return messages
    
    def coordinate(self, task: Dict) -> Dict:
        """Coordinate with swarm on a task."""
        # Broadcast intention
        self.broadcast({{"type": "intention", "task": task.get("name", "unknown")}})
        
        # Check what others are doing
        messages = self.receive_messages()
        
        # Simple coordination: avoid duplicating work
        claimed_tasks = [m.get("task") for m in messages if m.get("type") == "intention"]
        
        if task.get("name") in claimed_tasks:
            return {{"status": "deferred", "reason": "task claimed by another agent"}}
        
        return {{"status": "executing", "task": task}}
    
    def run(self, task=None):
        task = task or {{"name": "{spec}_task", "priority": 1}}
        
        result = self.coordinate(task)
        
        self._report("GREEN", f"Swarm coordination: {{result['status']}}")
        return result
    
    def _report(self, status, message):
        data = {{
            "agent": "{agent_name}",
            "type": "swarm",
            "domain": "{domain}",
            "swarm_id": self.swarm_id,
            "status": status,
            "message": message,
            "timestamp": datetime.now().isoformat()
        }}
        with open(self.sentinel_dir / "{agent_name}.done", 'w') as f:
            json.dump(data, f, indent=2)

if __name__ == "__main__":
    {class_name}().run()
'''

# Template registry
TEMPLATES = {
    "reactive": REACTIVE_TEMPLATE,
    "goal_based": GOAL_BASED_TEMPLATE,
    "learning": LEARNING_TEMPLATE,
    "utility": UTILITY_TEMPLATE,
    "swarm": SWARM_TEMPLATE
}

def get_template(archetype: str) -> str:
    """Get template for specified archetype."""
    return TEMPLATES.get(archetype, TEMPLATES["reactive"])

def format_template(template: str, domain: str, spec: str) -> str:
    """Format template with domain and specialization."""
    agent_name = f"{domain}_{spec}_agent"
    class_name = "".join(word.title() for word in f"{domain}_{spec}_agent".split("_"))
    
    return template.format(
        agent_name=agent_name,
        class_name=class_name,
        domain=domain,
        spec=spec,
        timestamp=datetime.now().isoformat()
    )
