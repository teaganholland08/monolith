"""
SOVEREIGN IDENTITY SETUP
Run this to unlock Project Monolith.
Securely saves credentials to System/Config/brave_wallet.json and .env
"""

import json
import os
import sys
from pathlib import Path

# Fix Windows encoding
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = Path(__file__).parent.parent.parent
CONFIG_DIR = ROOT / "System" / "Config"
CONFIG_DIR.mkdir(parents=True, exist_ok=True)
WALLET_FILE = CONFIG_DIR / "brave_wallet.json"

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def save_wallet(network, address):
    data = {}
    if WALLET_FILE.exists():
        try:
            data = json.loads(WALLET_FILE.read_text())
        except:
            pass
    
    if "addresses" not in data:
        data["addresses"] = {}
        
    data["addresses"][network] = address.strip()
    
    WALLET_FILE.write_text(json.dumps(data, indent=2))
    print(f"✅ Saved {network} Address securely.")

def main():
    clear()
    print("="*60)
    print("🔐 SOVEREIGN IDENTITY SETUP")
    print("="*60)
    print("The System is currently LOCKED.")
    print("To establish Sovereignty and unlock the Revenue Orchestrator,")
    print("you must prove ownership of a valid crypto wallet.")
    print("-" * 60)
    
    print("\n[1] Enter Ethereum Address (Brave/Metamask)")
    print("[2] Enter Bitcoin Address")
    print("[3] Skip (System remains Locked)")
    print("[4] I don't have one - GENERATE NEW IDENTITY (Recommended)")
    
    choice = input("\nSelect Option [1-4]: ").strip()
    
    if choice == "1":
        addr = input("\nPaste ETH Address: ").strip()
        if addr.startswith("0x") and len(addr) > 20:
            save_wallet("ETH", addr)
            print("\n🎉 SOVEREIGNTY ESTABLISHED. SYSTEM UNLOCKED.")
        else:
            print("\n❌ Invalid ETH Address format.")
            
    elif choice == "2":
        addr = input("\nPaste BTC Address: ").strip()
        if len(addr) > 20:
            save_wallet("BTC", addr)
            print("\n🎉 SOVEREIGNTY ESTABLISHED. SYSTEM UNLOCKED.")
        else:
            print("\n❌ Invalid BTC Address format.")

    elif choice == "4":
        try:
            from wallet_generator import generate_identity
            generate_identity()
            print("\n🎉 SOVEREIGNTY ESTABLISHED. SYSTEM UNLOCKED.")
        except ImportError:
            # Fallback if running from different dir context
            sys.path.append(str(Path(__file__).parent))
            try:
                from wallet_generator import generate_identity
                generate_identity()
                print("\n🎉 SOVEREIGNTY ESTABLISHED. SYSTEM UNLOCKED.")
            except Exception as e:
                print(f"\n❌ Generation Failed: {e}")
                print("ensure requirements.txt is installed: pip install web3 bip-utils")
            
    else:
        print("\n⚠️  Setup Aborted. System remains in Restricted Mode.")

    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()
