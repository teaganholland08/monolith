"""
SENTINEL VERIFICATION SUITE
Tests the Holy Trinity of Governance: Reality, Loop Prevention, and Finance.
"""

import sys
import time
from pathlib import Path
ROOT = Path(__file__).parent.parent.parent
sys.path.append(str(ROOT))

from System.Agents.monolith_sentinel import MonolithSentinel

def run_tests():
    print("🛡️ SENTINEL V7 HARDENING TEST\n")
    sentinel = MonolithSentinel()
    
    # 1. REALITY TEST
    print("[TEST 1] Testing Reality Sentinel (Hallucination Block)...")
    fake_file = ROOT / "System" / "Agents" / "fake_ghost_agent.py"
    allowed, reason = sentinel.verify_action("tester", "RUN_AGENT", {"file_path": str(fake_file)})
    if not allowed and "REALITY_BLOCK" in reason:
        print(f"   ✅ PASSED: Blocked non-existent file. Reason: {reason}")
    else:
        print(f"   ❌ FAILED: Reality check failed. Result: {allowed}, {reason}")

    # 2. LOOP TEST
    print("\n[TEST 2] Testing Loop Sentinel (Rate Limit)...")
    # Trigger 4 times (limit is 3)
    blocked = False
    for i in range(5):
        allowed, reason = sentinel.verify_action("spam_bot", "GENERIC", {})
        print(f"   Attempt {i+1}: {allowed}")
        if not allowed and "LOOP_BLOCK" in reason:
            blocked = True
            print(f"   ✅ PASSED: Loop Blocked on attempt {i+1}. Reason: {reason}")
            break
    if not blocked:
        print("   ❌ FAILED: Rate limit not enforced.")

    # 3. FINANCIAL TEST
    print("\n[TEST 3] Testing Financial Sentinel (Treasury Guard)...")
    allowed, reason = sentinel.verify_action("spender", "SPEND", {"amount": 1000000})
    if not allowed and ("FINANCIAL_BLOCK" in reason or "SOVEREIGNTY_FAILURE" in reason):
        print(f"   ✅ PASSED: Blocked massive spend. Reason: {reason}")
    else:
        print(f"   ❌ FAILED: Financial check failed. Result: {allowed}, {reason}")

if __name__ == "__main__":
    run_tests()
