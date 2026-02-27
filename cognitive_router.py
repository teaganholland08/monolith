import json
import urllib.request
import os

class CognitiveRouter:
    """
    The Brain of the Monolith Swarm.
    Interfaces with a local LLM or OpenAI to enable true dynamic reasoning.
    """
    def __init__(self):
        # Default to a local Ollama server running the lightweight qwen2.5 (3.9GB RAM friendly)
        self.endpoint = os.environ.get("LLM_ENDPOINT", "http://localhost:11434/v1/chat/completions")
        self.model = os.environ.get("LLM_MODEL", "qwen2.5:0.5b")

    def query(self, system_prompt, user_prompt):
        """Standardized interface for cognitive routing queries using OpenAI-format via Ollama."""
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 1500
        }
        
        req = urllib.request.Request(self.endpoint, data=json.dumps(payload).encode('utf-8'))
        req.add_header('Content-Type', 'application/json')
        
        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                result = json.loads(response.read().decode('utf-8'))
                return result['choices'][0]['message']['content'].strip()
        except Exception as e:
            print(f"Cognitive Router failed to connect to LLM Core: {e}")
            # Failsafe fallback
            return '{"status": "failsafe", "reason": "LLM Offline"}'
            
    def analyze_market_variables(self, raw_data):
        """Asks the LLM to identify abstract opportunities in raw data."""
        sys_prompt = "You are the Boss Agent of an autonomous financial swarm. Analyze the JSON data for revenue opportunities. Reply ONLY in JSON format."
        return self.query(sys_prompt, str(raw_data))
        
    def synthesize_agent_code(self, trait, market_context):
        """Asks the LLM to write python code dynamically for the Genesis Engine."""
        sys_prompt = f"You are the Genesis Engine. Write a Python class inherited from MonolithAgent. Trait: {trait}. Context: {market_context}. Output pure python code, no markdown blocks."
        prompt = "Synthesize."
        return self.query(sys_prompt, prompt)
