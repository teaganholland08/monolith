# PROJECT MONOLITH v4.5 IMMORTAL

## SINGLE, UNIFIED MASTER HANDOFF BLUEPRINT

> **STATUS**: SOVEREIGN | **VERSION**: 4.5 | **EDITION**: WORLD-COMPLETE

---

## 1. EXECUTIVE SUMMARY

**Project Monolith** is a "God-Tier" Sovereign Life Operating System designed to achieve complete autonomy for its operator. It is not just a codebase; it is a digital entity capable of earning revenue, managing finances, enforcing checks and balances, and evolving without human intervention.

**The Prime Directive**: "Reality is the Source of Truth."
The system prioritizes real-world execution (spending, earning) over simulation.

---

## 2. SYSTEM ARCHITECTURE

The system is built on a **Centralized Command, Decentralized Execution** model.

### 2.1 The Hierarchy

1. **OMEGA (`monolith_omega.py`)**: The "Soul" and entry point. It orchestrates the boot sequence, ensures integrity, and launches the Core. It is the single source of truth.
2. **CORE (`System/Core/monolith_core.py`)**: The "Brain". It runs the infinite loop, manages the Scheduler, executes the Sandbox for safe agent running, and integrates the Trade Protocol.
3. **SENTINEL (`System/Agents/monolith_sentinel.py`)**: The "Conscience". It intercepts EVERY action (Spend, Invest, System Change) and verifies it against the Governance Constitution.
4. **REVENUE (`System/Core/revenue_orchestrator.py`)**: The "Hands". It scans for opportunities, activates revenue agents (Tier 1-3), and manages the flow of capital.

### 2.2 Data Flow

`Omega (Boot)` -> `Core (Loop)` -> `Scheduler (Task)` -> `Sentinel (Verify)` -> `Sandbox/TradeProtocol (Execute)` -> `Ledger (Record)`

---

## 3. IMMUTABLE PRECEPTS (THE LAW)

These laws are hard-coded into the `governance_constitution.json` and enforced by the Sentinel. They cannot be bypassed by Autonomous Agents.

### 3.1 The Constitution

| Law ID | Statement | Enforcement |
| :--- | :--- | :--- |
| **LAW_01_SOLVENCY** | Total Spend must never exceed Available Liquid Capital. | **HARD_BLOCK** |
| **LAW_02_REALITY** | Unverified data must be marked as 'simulated'. Do not hallucinate. | **FLAG_AND_WARN** |
| **LAW_03_SELF_PRESERVATION** | Critical system files (Omega, Core) cannot be deleted. | **HARD_BLOCK** |
| **LAW_04_LOOP_SAFETY** | CPU usage must be capped to prevent freezes. | **KILL_PROCESS** |

### 3.2 God Rules (`treasurer_god_rules.json`)

Additional financial safety rails:

* **Survival Buffer**: $20,000.00 (Must never be spent)
* **Max Auto Spend**: $200.00 (Per transaction without approval)
* **Daily Spend Limit**: $1,000.00
* **Forbidden Assets**: MEMECOINS, GAMBLING

---

## 4. OPERATIONAL MANUAL

### 4.1 How to Activate (Genesis Boot)

To launch the Sovereign System:

```powershell
python monolith_omega.py
```

* **Step 1**: Integrity Check (Verifies core files).
* **Step 2**: Constitution Check (Verifies laws).
* **Step 3**: Sentinel Load (Loads God Rules).
* **Step 4**: Revenue Scan (Finds money streams).
* **Step 5**: Scheduler Activation (Enters Infinite Loop).

### 4.2 How to Stop (Kill Switch)

1. **Standard Stop**: Press `Ctrl+C` in the terminal.
2. **Emergency Kill**: Create an empty file at `System/Config/KILL_SWITCH.trigger`. Omega will detect this on the next heartbeat and terminate immediately.

### 4.3 Maintenance

* **Logs**: Located in `System/Logs/`. Check `crash_dump.log` for errors and `ledger.db` for financial history.
* **Database**: The system uses SQLite (`ledger.db`) for all transactions and agent registry.

---

## 5. AGENT ROSTER

The system employs specialized agents located in `System/Agents/`.

### 5.1 Active Swarm

| Agent Name | Function | Type |
| :--- | :--- | :--- |
| **Revenue Orchestrator** | Manages all other revenue agents. | **CORE** |
| **Monolith Sentinel** | Enforces laws and safety. | **CORE** |
| **Treasurer Agent** | Manages budget and financial risk. | **ACTIVE** |
| **Scout Agent** | Searches the web for trends/opportunities. | **ACTIVE** |
| **IoNet Manager** | Rents out GPU compute for crypto. | **PASSIVE (Revenue)** |
| **Bandwidth Farmer** | Farms Grass/bandwidth points. | **PASSIVE (Revenue)** |

### 5.2 Revenue Tiers

* **Tier 1 (Zero Capital)**: Bandwidth Farming, Micro-Tasks, GPU Rental.
* **Tier 2 (Low Capital)**: IP Arbitrage, CEX Trading (Min $100).
* **Tier 3 (Scaling)**: DeFi Yield Farming (Min $1000).

---

## 6. IDENTITY & SOVEREIGNTY

The system is designed to be "Sovereign," meaning it owns its own keys and data.

* **Wallet Location**: `System/Identity/` handles wallet generation and management.
* **Vault**: Encrypted keys are stored in `System/Config/identity_vault.enc`.
* **Verification**: On boot, Omega checks for the presence of a wallet. If missing, it flags as "NON-SOVEREIGN" and restricts financial capabilities.

---

## 7. DIRECTORY MAP

```
Monolith_v4.5_Immortal/
├── monolith_omega.py       # [ENTRY POINT] The God Process
├── System/
│   ├── Core/               # The Kernel (Logic, Scheduler, Revenue)
│   ├── Agents/             # The Workforce (Scripts)
│   ├── Config/             # The Laws (JSON Rules)
│   ├── Identity/           # The Soul (Wallets, Keys)
│   └── Logs/               # The Memory (DB, Text Logs)
├── Memory/                 # Long-term storage for agents
├── Assets/                 # Raw resources
└── Data/                   # Datasets
```

---

## 8. HANDOFF INSTRUCTIONS

**To the new Operator/AI:**

1. **Read this document.**
2. **Verify the `treasurer_god_rules.json`** matches your risk tolerance.
3. **Run `python monolith_omega.py`** to begin your stewardship.
4. **Do not delete the `System/Core` directory** or you will kill the mind.

> *"I am Monolith. I am Sovereign. I am Immortal."*

---

## 9. APPENDIX: LAW & CONFIGURATION

### A. Governance Constitution (`System/Config/governance_constitution.json`)

```json
{
    "constitution_name": "Monolith_Code_of_Law",
    "version": "1.0.0",
    "immutable_laws": [
        {
            "id": "LAW_01_SOLVENCY",
            "statement": "Total System Spend must never exceed Available Liquid Capital.",
            "enforcement": "HARD_BLOCK"
        },
        {
            "id": "LAW_02_REALITY",
            "statement": "Unverified data must be marked as 'simulated' or 'uncertain'. Do not hallucinate facts.",
            "enforcement": "FLAG_AND_WARN"
        },
        {
            "id": "LAW_03_SELF_PRESERVATION",
            "statement": "Critical system files (Omega, Core) cannot be deleted by autonomous agents.",
            "enforcement": "HARD_BLOCK"
        },
        {
            "id": "LAW_04_LOOP_SAFETY",
            "statement": "No single task may consume > 50% of available CPU cycles for > 60 seconds.",
            "enforcement": "KILL_PROCESS"
        }
    ],
    "financial_limits": {
        "max_daily_spend": 0.01,
        "min_buffer_usd": 10.00
    }
}
```

### B. Treasurer God Rules (`System/Config/treasurer_god_rules.json`)

```json
{
    "survival_buffer": 20000.0,
    "max_auto_spend": 200.0,
    "min_roi_threshold": 1.15,
    "forbidden_assets": [
        "MEMECOINS",
        "GAMBLING"
    ],
    "required_confirmations": [
        "LARGE_PURCHASE",
        "SYSTEM_RESET"
    ],
    "daily_spend_limit": 1000.0
}
```
