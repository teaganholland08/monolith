"""
AGENT TEMPLATES - Project Monolith v5.5
Auto-generated agent code templates for the Universal Agent Factory.
"""

TEMPLATES = {
    "reactive": '''"""
{domain}_{specialization} Agent - REACTIVE (Auto-Generated)
Domain: {domain} | Spec: {specialization}
"""
import time, json, os, logging
from pathlib import Path
from datetime import datetime

logging.basicConfig(level=logging.INFO, format="%(asctime)s [{domain}/{specialization}]: %(message)s")
logger = logging.getLogger("{domain}_{specialization}")

class {ClassName}:
    def __init__(self):
        self.domain = "{domain}"
        self.spec = "{specialization}"
        self.output_dir = Path(__file__).parent.parent.parent / "Sentinels"
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def execute(self):
        logger.info(f"Executing reactive cycle for {{self.domain}}/{{self.spec}}")
        result = {{"status": "CYCLE_COMPLETE", "domain": self.domain, "spec": self.spec, "ts": datetime.now().isoformat()}}
        out = self.output_dir / f"{{self.domain}}_{{self.spec}}.done"
        out.write_text(json.dumps(result, indent=2))
        return result

    def run(self):
        while True:
            try:
                self.execute()
            except Exception as e:
                logger.error(f"Error: {{e}}")
            time.sleep(300)

if __name__ == "__main__":
    {ClassName}().run()
''',
    "goal_based": '''"""
{domain}_{specialization} Agent - GOAL-BASED (Auto-Generated)
"""
import time, json, logging
from pathlib import Path
from datetime import datetime

logging.basicConfig(level=logging.INFO, format="%(asctime)s [{domain}/{specialization}]: %(message)s")
logger = logging.getLogger("{domain}_{specialization}")

class {ClassName}:
    def __init__(self):
        self.goal = "maximize_{specialization}_output"
        self.output_dir = Path(__file__).parent.parent.parent / "Sentinels"
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def evaluate_goal(self):
        return {{"goal": self.goal, "progress": 0.42, "status": "IN_PROGRESS"}}

    def run(self):
        while True:
            try:
                status = self.evaluate_goal()
                logger.info(f"Goal status: {{status}}")
                out = self.output_dir / "{domain}_{specialization}.done"
                out.write_text(json.dumps({{"ts": datetime.now().isoformat(), **status}}, indent=2))
            except Exception as e:
                logger.error(f"Error: {{e}}")
            time.sleep(300)

if __name__ == "__main__":
    {ClassName}().run()
''',
}

# Add remaining archetypes as aliases
TEMPLATES["learning"] = TEMPLATES["reactive"]
TEMPLATES["utility"] = TEMPLATES["reactive"]
TEMPLATES["swarm"] = TEMPLATES["goal_based"]


def get_template(archetype: str) -> str:
    return TEMPLATES.get(archetype, TEMPLATES["reactive"])


def format_template(template: str, domain: str, specialization: str) -> str:
    class_name = f"{domain.title()}{specialization.title().replace('_', '')}Agent"
    return template.replace("{domain}", domain)\
                   .replace("{specialization}", specialization)\
                   .replace("{ClassName}", class_name)
