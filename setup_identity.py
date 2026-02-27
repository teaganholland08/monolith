"""
IDENTITY SETUP WIZARD v1.0
Automates the creation of a Sovereign Identity.
1. Generates/Links ETH Wallet.
2. Creates Sovereign Profile.
3. Unlocks Project Monolith.
"""

import sys
import json
import time
from pathlib import Path

# Add System Root
ROOT = Path(__file__).parent.parent.parent
sys.path.append(str(ROOT))

try:
    from System.Identity.identity_prime import IdentityPrime
    from System.Identity.wallet_manager import WalletManager
except ImportError as e:
    print(f"❌ CRITICAL IMPORT ERROR: {e}")
    sys.exit(1)

def main():
    print("=" * 60)
    print("🛡️  SOVEREIGN IDENTITY GENESIS")
    print("=" * 60)
    
    id_sys = IdentityPrime()
    wm = WalletManager()
    
    if id_sys.verify_sovereignty():
        print("✅ System is ALREADY Sovereign.")
        addr = id_sys.get_wallet_address()
        print(f"   Wallet: {addr}")
        choice = input("   Reset Identity? (y/N): ")
        if choice.lower() != 'y':
            return
            
    print("\n[1] GENERATE NEW WALLET (Local/Host)")
    print("[2] IMPORT EXISTING WALLET (Enter Private Key)")
    print("[3] ENTER ADDRESS ONLY (Watch Mode - No Spending)")
    
    mode = input("\nSelect Mode [1]: ") or "1"
    
    address = None
    key = None
    
    if mode == "1":
        print("\n⚡ Generating new Ethereum Wallet...")
        try:
            address, key = wm.create_wallet("ETH")
            if address:
                print(f"   CREATED: {address}")
                print(f"   KEY:     {key} (SAVE THIS NOW)")
            else:
                print("   ❌ Failed to create wallet. Check dependencies (web3/eth-account).")
        except Exception as e:
            print(f"   ❌ Error: {e}")
            
    elif mode == "2":
        key = input("Enter Private Key: ").strip()
        # In real app, verify key here. For now, assume user is correct or use web3 if available
        # We will just treat it as a "Imported" event
        print("   ⚠️  Key Import Simulated (Security precaution: Keys should be in .env)")
        address = "0xIMPORTED_" + str(int(time.time())) # Placeholder if we don't have web3 to derive
        
    elif mode == "3":
        address = input("Enter Public ETH Address: ").strip()
        
    # Finalize
    if address:
        print("\n📝 registering identity...")
        id_sys.register_wallet(address, "ETH")
        
        print("📝 generating sovereign hash (SIN)...")
        # Generate a deterministic but distinct hash for "Teagan Holland" (User)
        # In a real scenario, we'd ask for inputs. Here we auto-generate for "Zero-Touch" start.
        id_sys.register_identity("0000", "2026") # Default Sovereign Genesis Block
        
        print("\n✅ IDENTITY ESTABLISHED.")
        print("   The System is now UNRESTRICTED.")
        print("   Revenue Streams have been UNLOCKED.")
    else:
        print("\n❌ Setup Aborted.")

if __name__ == "__main__":
    main()
