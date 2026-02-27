"""
Harness to run test_limits.py inside MonolithSandbox.
"""
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))
from sandbox_win import MonolithSandbox

def run_test():
    sandbox = MonolithSandbox()
    test_script = Path(__file__).parent / "test_limits.py"
    
    print(f"[HARNESS] Running {test_script} in Sandbox...")
    result = sandbox.run_agent(test_script, timeout=30)
    
    print("\n[HARNESS] Result:")
    print(f"Success: {result['success']}")
    print(f"Exit Code: {result['exit_code']}")
    print(f"Stdout:\n{result['stdout']}")
    print(f"Stderr:\n{result['stderr']}")
    
    if result['exit_code'] != 0:
        print("\n[HARNESS] PASS: Process killed.")
    elif "MemoryError" in result['stderr'] or "MemoryError" in result['stdout']:
        print("\n[HARNESS] PASS: Memory Limit triggered.")
    else:
        print("\n[HARNESS] ❓ INCONCLUSIVE.")

if __name__ == "__main__":
    run_test()
