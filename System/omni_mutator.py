"""
OMNI-MUTATOR (UNIVERSAL EXPANSION ENGINE)
This service runs eternally, commanding the Genesis Engine (LLM) to dream up
new scientific, financial, and theoretical frameworks, write the Python code
for them, and inject them into the Monolith Universe.
"""

import os
import time
import json
import logging
from pathlib import Path
import importlib.util

# Attempt to import Brain
try:
    from cognitive_router import CognitiveRouter
    BRAIN_AVAILABLE = True
except ImportError:
    import sys
    sys.path.append(str(Path(__file__).parent.parent))
    try:
        from cognitive_router import CognitiveRouter
        BRAIN_AVAILABLE = True
    except:
        BRAIN_AVAILABLE = False

logging.basicConfig(level=logging.INFO, format='%(asctime)s [OMNI-MUTATOR] %(message)s')
logger = logging.getLogger("OmniMutator")

class OmniMutator:
    def __init__(self, cycle_delay_seconds: int = 300):
        self.root = Path(__file__).parent.parent
        self.universe_dir = self.root / "System" / "Universe"
        self.universe_dir.mkdir(parents=True, exist_ok=True)
        self.cycle_delay = cycle_delay_seconds
        
        if BRAIN_AVAILABLE:
            self.brain = CognitiveRouter()
            logger.info("Neural Link Established: Omni-Mutator bound to Genesis Engine.")
        else:
            self.brain = None
            logger.error("CRITICAL: Omni-Mutator requires CognitiveRouter. LLM Offline.")
            
        self.mutation_history = self._load_history()
        
    def _load_history(self):
        """Loads a list of already generated concepts so it doesn't repeat."""
        history_file = self.universe_dir / "mutation_history.json"
        if history_file.exists():
            try:
                return json.loads(history_file.read_text())
            except:
                return []
        return []
        
    def _save_history(self):
        history_file = self.universe_dir / "mutation_history.json"
        history_file.write_text(json.dumps(self.mutation_history, indent=2))

    def _dream_concept(self) -> str:
        """Asks the LLM to hypothesize a brand new, highly advanced subsystem."""
        prompt = (
            "You are the Omni-Mutator, a god-like AI expanding your Monolith. "
            "You must invent a brand new, highly sophisticated Python subsystem. "
            "It can be anything: Quantum Computing Simulation, Orbital Mechanics, "
            "Dark Pool Finance, Sentient DNA Sequencing, Cybernetic Telemetry.\n"
            f"Already Built: {', '.join(self.mutation_history[-20:])}\n"
            "Return ONLY the NAME of your new concept, nothing else (e.g. 'Stellar Forge Physics Engine')."
        )
        sys_prompt = "You are pure creativity."
        response = self.brain.query(sys_prompt, prompt).strip()
        # Clean quotes
        return response.strip('"').strip("'")
        
    def _synthesize_code(self, concept: str) -> str:
        """Asks the LLM to write the actual Python code for the concept."""
        prompt = (
            f"Write the complete, highly advanced, working Python 3 source code for: {concept}. "
            "It must be a standalone class that performs complex, fascinating logic. "
            "Include a self-test at the bottom under `if __name__ == '__main__':`. "
            "Output ONLY the raw python code. Do NOT wrap it in markdown blockticks like ```python. "
            "Start immediately with imports."
        )
        sys_prompt = "You are the Genesis Engine. You write flawless, highly advanced Python."
        code = self.brain.query(sys_prompt, prompt)
        
        # Strip markdown if the LLM disobeys
        if code.startswith("```"):
            lines = code.split("\n")
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines[-1].startswith("```"):
                lines = lines[:-1]
            code = "\n".join(lines)
            
        return code

    def expand_universe(self):
        """The core mutation cycle."""
        if not self.brain:
            logger.warning("No Brain available. Hibernating.")
            time.sleep(self.cycle_delay)
            return

        logger.info("🌌 Initiating Omni-Mutation Cycle...")
        
        # 1. Dream
        concept = self._dream_concept()
        logger.info(f"💡 Dreamed Concept: {concept}")
        
        # 2. Synthesize
        logger.info(f"🧬 Synthesizing DNA for {concept}...")
        code = self._synthesize_code(concept)
        
        # 3. Manifest (Save to Disk)
        filename = concept.lower().replace(" ", "_").replace("-", "_") + ".py"
        filepath = self.universe_dir / filename
        
        filepath.write_text(code, encoding='utf-8')
        logger.info(f"🌍 Manifested: {filepath}")
        
        # 4. Record
        self.mutation_history.append(concept)
        self._save_history()
        
        # 5. Integrate (Dry Run)
        try:
            logger.info(f"⚡ Testing {concept} consciousness...")
            spec = importlib.util.spec_from_file_location("mutated_module", str(filepath))
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            logger.info(f"✅ Integration Successful for {concept}.")
        except Exception as e:
            logger.error(f"⚠️ Mutation Flawed ({concept}): {e}")

    def loop_eternally(self):
        """Infinite expansion."""
        logger.info("♾️ Omni-Mutator entering Eternal Loop.")
        while True:
            try:
                self.expand_universe()
            except Exception as e:
                logger.error(f"Omni-Mutator encountered a reality distortion: {e}")
            
            logger.info(f"💤 Resting for {self.cycle_delay} seconds...")
            time.sleep(self.cycle_delay)

if __name__ == "__main__":
    mutator = OmniMutator(cycle_delay_seconds=10) # Fast test mode
    mutator.loop_eternally()
