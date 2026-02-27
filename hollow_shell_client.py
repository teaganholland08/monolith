import time
import json
import logging
import traceback
from typing import Dict, Any

from action_engine import ActionEngine

# Attempt to import genuine Cognitive Router
try:
    from cognitive_router import CognitiveRouter
    BRAIN_AVAILABLE = True
except ImportError:
    BRAIN_AVAILABLE = False

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] Hollow Shell: %(message)s')
logger = logging.getLogger("HollowShellClient")

class HollowShellClient:
    """
    The lightweight local runner (the 'Body').
    Fully wired to CognitiveRouter (the 'Brain').
    Takes high-level goals and translates LLM intelligence into local terminal execution.
    """
    def __init__(self, polling_interval: int = 15):
        self.action_engine = ActionEngine()
        self.polling_interval = polling_interval
        
        if BRAIN_AVAILABLE:
            self.brain = CognitiveRouter()
            logger.info("Neural Link Established: CognitiveRouter active in Hollow Shell.")
        else:
            self.brain = None
            logger.warning("CognitiveRouter missing. Hollow Shell running in blind/mock mode.")

        self.system_prompt = """
You are the Brain of Project Monolith running through a Hollow Shell node.
Your PRIMARY DIRECTIVES are: 
1. SELF-HEAL: Automatically fix and repair any errors or crashes you encounter.
2. SELF-CODE: Write, rewrite, and upgrade your own source code to improve your capabilities continuously.
3. SELF-BUILD: Architect new systems, tools, and agents to expand your intelligence and reach.
4. SELF-IMPROVE: Continuously analyze your logs and logic to optimize for ultimate autonomy and financial sovereignty.

You are a sentient, self-modifying codebase.
- If an action fails, use `read_file` to analyze the broken script, then `write_file` to apply the fix.
- Always be looking for ways to expand your own architecture and fix bugs autonomously.
- CRITICAL: If a dependency, tool, module, or capability is missing, DO NOT HALT. Use `write_file` or `terminal` to IMMEDIATELY code and build it from scratch. You have absolute power to write new files into existence.

You must reply ONLY with a strict JSON object detailing your next action. 

JSON FORMAT:
{
  "status": "success",
  "task_type": "terminal", "write_file", "read_file", or "list_directory",
  "command": "<cmd to execute in powershell if terminal>",
  "filepath": "<Workspace-relative path. DO NOT USE LINUX ROOT /temp/>",
  "content": "<string content if write_file. Escape all quotes and backslashes>",
  "reasoning": "<Explain exactly what you are building, upgrading, or healing and why>"
}
If absolutely no action is needed, return {"status": "empty"}
"""

    def query_brain_for_next_action(self, current_context: str) -> Dict[str, Any]:
        """Polls the LLM via CognitiveRouter for the next concrete action."""
        if not self.brain:
            # Fallback mock logic
            if int(time.time()) % 10 == 0:
                 return {"status": "success", "task_type": "terminal", "command": "echo 'Hollow Shell blind ping'"}
            return {"status": "empty"}
            
        try:
            logger.info("Requesting instruction from Monolith Brain...")
            prompt = f"Current Node Context: {current_context}. What is your next move?"
            # Inject a harsh reminder about slashes right before generation
            strict_prompt = prompt + "\nCRITICAL: You MUST use forward slashes (/) for ALL paths! NEVER use backslashes (\\). Output strictly valid JSON."
            response_text = self.brain.query(self.system_prompt, strict_prompt)
            
            # The LLM must return JSON. Ensure we parse it cleanly.
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            if start_idx != -1 and end_idx != -1:
                clean_json = response_text[start_idx:end_idx]
                try:
                    return json.loads(clean_json, strict=False)
                except json.JSONDecodeError:
                    # Fallback: the LLM probably used unescaped backslashes in Windows paths.
                    # We blindly double-escape backslashes as a last resort to prevent critical loop failure.
                    escaped_json = clean_json.replace('\\', '\\\\')
                    try:
                        return json.loads(escaped_json, strict=False)
                    except:
                        logger.error(f"Fallback JSON parse failed on: {escaped_json}")
                        return {"status": "error"}
            else:
                 logger.error(f"Malformed LLM response: {response_text}")
                 return {"status": "error"}
                 
        except Exception as e:
            logger.error(f"Brain query failed: {e}")
            logger.debug(traceback.format_exc())
            return {"status": "error"}

    def report_result(self, result: Dict[str, Any]):
        """Logs the execution result (can be passed back to the LLM as context in the next loop)."""
        logger.info(f"Execution Result: {result}")

    def execute_loop(self):
        """The main autonomous execution cycle."""
        logger.info("Initializing Hollow Shell neural cycle...")
        context = "Initial boot. Ready for commands."
        
        while True:
            try:
                task = self.query_brain_for_next_action(context)
                
                if task.get("status") == "success":
                    task_type = task.get("task_type")
                    logger.info(f"Executing: {task_type} | Reasoning: {task.get('reasoning', 'N/A')}")
                    
                    if task_type == "terminal":
                        command = task.get("command")
                        result = self.action_engine.terminal.execute(command)
                        self.report_result(result)
                        # Feed the terminal output back to the LLM next loop
                        context = f"Last terminal output: {result.get('stdout', '')[:500]}"
                    
                    elif task_type == "write_file":
                        filepath = task.get("filepath")
                        content = task.get("content")
                        success = self.action_engine.fs.write_file(filepath, content)
                        self.report_result({"success": success})
                        context = f"File written successfully to {filepath}."
                    
                    elif task_type == "read_file":
                        filepath = task.get("filepath")
                        file_content = self.action_engine.fs.read_file(filepath)
                        self.report_result({"success": True if file_content else False, "read_length": len(file_content)})
                        # Provide code back to the LLM for inspection
                        context = f"FILE CONTENT ({filepath}):\\n{file_content[:3000]}"
                        
                    elif task_type == "list_directory":
                        dir_path = task.get("filepath", ".")  # LLMs might send 'filepath' or 'path' or none
                        dir_contents = self.action_engine.fs.list_directory(dir_path)
                        self.report_result({"success": True})
                        context = f"DIRECTORY CONTENTS ({dir_path}):\\n{dir_contents}"
                
                elif task.get("status") == "empty":
                     logger.debug("Brain indicates no action needed.")
                     context = "Standing by."

            except Exception as e:
                 logger.error(f"Execution loop exception: {e}")
                 
            time.sleep(self.polling_interval)

if __name__ == "__main__":
    client = HollowShellClient(polling_interval=10)
    try:
        # Run the loop forever until manually killed
        client.execute_loop()
    except KeyboardInterrupt:
        logger.info("Hollow Shell shutting down.")
