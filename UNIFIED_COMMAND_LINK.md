# 🔗 UNIFIED COMMAND LINK: DUAL-MOBILE SETUP

**Objective**: Build a Zero-Trust Bridge between Samsung (Engine) and iPhone (Shield).
**Result**: One Brain, Two Nodes.

---

## 🏗️ 1. THE PRIVATE TUNNEL (Tailscale)

*Securely access your home server (and execution dashboard) from anywhere.*

1. **Install Tailscale**: On Workstation (Hub), Samsung, and iPhone.
2. **Authenticate**: Use your Project Monolith Google identity.
3. **Activate "Exit Node"**:
    * Set your Home Workstation as the `Exit Node`.
    * *Effect*: Your iPhone traffic now routes through your home fortress, encrypting it from public WiFi.
4. **Access the HUD**:
    * Run `streamlit run monolith_ui.py` on your Workstation/Samsung.
    * Get the **Tailscale IP** (e.g., `100.x.x.x:8501`).
    * Open this IP in Safari (iPhone) or Samsung Internet.
    * **Result**: The Monolith Command Center is live on both screens.

---

## 📂 2. THE OFFLINE MIRROR (Syncthing)

*Sync the 8TB Ark and Python Scripts without the Cloud.*

1. **Install Syncthing**:
    * **Android (Samsung)**: "Syncthing" from Play Store.
    * **iOS (iPhone)**: "Möbius Sync" (Syncthing client).
    * **PC**: "Syncthing" desktop app.
2. **Link Devices**: Scan QR codes to introduce the phones to the Workstation.
3. **Create Folder**: `PROJECT_MONOLITH`.
4. **Sync Policy**: "Send & Receive".
5. **Result**: If you edit `auto_monolith.py` on your Samsung, the change appears on your iPhone instantly.

---

## 📱 3. DEVICE ROLES (The Doctrine)

### 🐍 The Samsung (Engine Mode)

* **App**: Termux.
* **Role**: Running python scripts, compiling code, analyzing logs.
* **UI Mode**: "ENGINE" (Technical Dashboard).

### 🛡️ The iPhone (Shield Mode)

* **App**: Safari (Tailscale IP) + Signal + Ledger Live.
* **Role**: Examining Yield, Approving Airdrops, Banking.
* **UI Mode**: "SHIELD" (Glossophobic/Minimal).

---

**COMMANDER**:
The Bridge is Built.
The System is One.
**SYNC COMPLETE.**
