"""
IDENTITY PRIME v2.0 (LIVE)
The Root of Sovereign Identity for Project Monolith.
Manages credentials, keys, and "Proof of Life" without relying on central databases.
NOW GENERATES REAL CRYPTOGRAPHIC KEYS.
"""

import json
import hashlib
import os
import base64
from pathlib import Path
from datetime import datetime
from cryptography.fernet import Fernet
from eth_account import Account

class IdentityPrime:
    def __init__(self):
        self.root = Path(__file__).parent.parent.parent
        self.secure_dir = self.root / "SecureData" / "Identity"
        self.secure_dir.mkdir(parents=True, exist_ok=True)
        
        self.profile_path = self.secure_dir / "sovereign_profile.json"
        self.vault_path = self.secure_dir / "vault.enc"
        self.key_path = self.secure_dir / "master.key"
        
        # Initialize Crypto
        self.cipher = self._load_or_create_key()
        
        # Initialize Profile
        self.profile = self._load_profile()
        
        # Auto-Bootstrap if needed
        if not self.verify_sovereignty():
            print("[IDENTITY] Sovereignty missing. bootstrapping new identity...")
            self.generate_sovereign_wallet()
        
    def _load_or_create_key(self):
        """Load or create Fernet Master Key for local encryption"""
        if self.key_path.exists():
            return Fernet(self.key_path.read_bytes())
        else:
            key = Fernet.generate_key()
            self.key_path.write_bytes(key)
            # Set hidden attribute on Windows
            os.system(f"attrib +h {self.key_path}")
            return Fernet(key)

    def _load_profile(self):
        if self.profile_path.exists():
            try:
                return json.loads(self.profile_path.read_text())
            except:
                return {}
        return {}

    def verify_sovereignty(self):
        """
        Boolean check: Does the system have the means to transact?
        Checks for Wallet existence.
        """
        return self.profile.get("primary_wallet_address") is not None and self.vault_path.exists()

    def generate_sovereign_wallet(self):
        """
        Generates a BRAND NEW Ethereum Wallet.
        Encrypts Private Key immediately.
        """
        print("[IDENTITY] Generating Sovereign Keypair (Entropy Gathering)...")
        # Enable Mnemonic features if available, otherwise raw key
        Account.enable_unaudited_hdwallet_features()
        acct, mnemonic = Account.create_with_mnemonic()
        
        address = acct.address
        private_key = acct.key.hex()
        
        # Encrypt
        encrypted_pk = self.cipher.encrypt(private_key.encode()).decode()
        encrypted_mnemonic = self.cipher.encrypt(mnemonic.encode()).decode()
        
        # Save Vault
        vault_data = {
            "eth_private_key_enc": encrypted_pk,
            "mnemonic_enc": encrypted_mnemonic,
            "created_at": datetime.now().isoformat()
        }
        self.vault_path.write_text(json.dumps(vault_data, indent=2))
        
        # Update Profile (Public Data Only)
        self.profile["primary_wallet_address"] = address
        self.profile["primary_chain"] = "ETH"
        self.profile["sovereignty_level"] = "GENESIS"
        self._save_profile()
        
        print(f"[IDENTITY] Wallet Created: {address}")
        print(f"[IDENTITY] Private Key Encrypted & Vaulted.")

    def get_wallet_address(self):
        return self.profile.get("primary_wallet_address")

    def _save_profile(self):
        self.profile_path.write_text(json.dumps(self.profile, indent=2))

if __name__ == "__main__":
    # Test Routine
    id_sys = IdentityPrime()
    print(f"Sovereignty Status: {id_sys.verify_sovereignty()}")
    print(f"Address: {id_sys.get_wallet_address()}")

