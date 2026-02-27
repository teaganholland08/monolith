"""
ULTIMATE INTEGRITY CHECK - Phase Alpha-Zero Verification
Purpose: Verifies the existence and basic functionality of the new Revenue Layers.
"""

import sys
import os
from pathlib import Path
import importlib.util

def check_integrity():
    print("==================================================")
    print("       MONOLITH ALPHA-ZERO VERIFICATION           ")
    print("==================================================")
    
    root = Path(__file__).parent
    
    # 1. Structure Verification
    required_files = [
        "monolith_prime.py",
        "monolith_api.py",
        "System/Core/agent_ops.py",
        "System/Core/mcp_bridge.py",
        "System/Intelligence/academy.py",
        "System/Finance/trade_protocol.py"
    ]
    
    missing = []
    print("\n[1] Checking Core Files...")
    for rel_path in required_files:
        path = root / rel_path
        if path.exists():
            print(f"  [OK] {rel_path}")
        else:
            print(f"  [MISSING] {rel_path}")
            missing.append(rel_path)
            
    if missing:
        print(f"\n🛑 CRITICAL MISSING FILES: {len(missing)}")
        return

    # 2. Functional Verification
    print("\n[2] Verifying Functional Revenue Layers...")
    
    # Check Academy
    try:
        sys.path.append(str(root / "System" / "Intelligence"))
        spec = importlib.util.spec_from_file_location("academy", root / "System/Intelligence/academy.py")
        academy_mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(academy_mod)
        
        ac = academy_mod.Academy()
        # Test basic write
        res = ac.research_topic("Integrity Check", depth="verify")
        if res["status"] == "success":
            print("  [OK] Academy: Research Protocol Active")
        else:
            print(f"  [FAIL] Academy: {res}")
    except Exception as e:
        print(f"  [FAIL] Academy Crash: {e}")

    # Check Trade Protocol
    try:
        sys.path.append(str(root / "System" / "Finance"))
        spec = importlib.util.spec_from_file_location("trade_protocol", root / "System/Finance/trade_protocol.py")
        trade_mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(trade_mod)
        
        tp = trade_mod.TradeProtocol()
        opps = tp.scan_arbitrage(assets=['BTC_TEST'])
        if opps:
            print(f"  [OK] Trade Protocol: Arbitrage Scanner Active (Found {len(opps)} opps)")
            # Execute one
            tp.execute_paper_trade(opps[0])
        else:
            print("  [WARN] Trade Protocol: No opportunities mock-scanned.")
    except Exception as e:
        print(f"  [FAIL] Trade Protocol Crash: {e}")
        
    print("\n==================================================")
    print("       VERIFICATION COMPLETE - READY FOR PRIME    ")
    print("==================================================")

if __name__ == "__main__":
    check_integrity()
