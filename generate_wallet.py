"""
WALLET GENERATOR - Project Monolith
Generates a Solana-compatible Keypair for revenue collection.
"""

import json
import os
import secrets
from pathlib import Path

# Try to import cryptography for Ed25519
try:
    from cryptography.hazmat.primitives.asymmetric import ed25519
    from cryptography.hazmat.primitives import serialization
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False

def generate_wallet():
    print("🔐 GENERATING SECURE WALLET...")
    
    root = Path(__file__).parent.parent.parent
    brain_dir = root / "Brain"
    config_dir = root / "System" / "Config"
    
    brain_dir.mkdir(exist_ok=True)
    config_dir.mkdir(exist_ok=True)
    
    if not CRYPTO_AVAILABLE:
        print("⚠️ CRITICAL: 'cryptography' library not found. Installing...")
        import subprocess
        subprocess.check_call(["python", "-m", "pip", "install", "cryptography"])
        from cryptography.hazmat.primitives.asymmetric import ed25519
        from cryptography.hazmat.primitives import serialization
    else:
        # Use valid global imports if available
        from cryptography.hazmat.primitives.asymmetric import ed25519
        from cryptography.hazmat.primitives import serialization

    # Generate Ed25519 Keypair (Solana Standard)
    private_key = ed25519.Ed25519PrivateKey.generate()
    public_key = private_key.public_key()
    
    # Get bytes
    priv_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PrivateFormat.Raw,
        encryption_algorithm=serialization.NoEncryption()
    )
    pub_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw
    )
    
    # Solana Keypair format is usually just the 64-byte secret key (priv + pub)
    # or sometimes a JSON array of integers.
    # We will save as the standard JSON array format [int, int, ...] used by Phantom/Solana CLI
    
    full_keypair = priv_bytes + pub_bytes
    keypair_list = list(full_keypair)
    
    # Save Private Key (Vault)
    vault_path = brain_dir / "vault_key.json"
    if vault_path.exists():
        print(f"⚠️ WALLET ALREADY EXISTS at {vault_path}")
        print("   Skipping generation to prevent overwrite of funds.")
        return
        
    with open(vault_path, 'w') as f:
        json.dump(keypair_list, f)
    
    # Create Public Address (Mocking base58 encoding if libs missing, but we need real)
    # Since we don't have base58 lib guaranteed, we will try to install it or use a simple implementation
    
    try:
        import base58
    except ImportError:
        import subprocess
        subprocess.check_call(["python", "-m", "pip", "install", "base58"])
        import base58

    pub_b58 = base58.b58encode(pub_bytes).decode('ascii')
    
    print(f"✅ WALLET GENERATED!")
    print(f"   Public Address: {pub_b58}")
    print(f"   Private Key:    Saved to Brain/vault_key.json (KEEP SAFE)")
    
    # Save Config for Agents
    config_data = {
        "wallet_address": pub_b58,
        "network": "mainnet-beta"
    }
    
    with open(config_dir / "ionet_config.json", 'w') as f:
        json.dump(config_data, f, indent=2)
        
    print("   -> Config updated for IO.net and Treasurer.")

if __name__ == "__main__":
    generate_wallet()
