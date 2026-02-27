# Sovereign Reconstruction Plan - Project Monolith

## Goal Description

Project Monolith is currently bloated with ~600 simulation agents and "fake" sentinels that do not generate real revenue. The goal is to **PURGE** this noise and rebuild the system around a **Hyper-Real Core**.

We will:

1. Archive all unverified agents.
2. Establish a "God Layer" Sentinel that enforces real-world checks (Crypto Wallet, API Keys).
3. Implement a single, verified "Zero Capital" revenue stream (Micro-Tasking/Fiverr Assets).

## User Review Required
>
> [!IMPORTANT]
> **THE GREAT PURGE**: I will be moving ~90% of the files in `System/Agents` and `System/Sentinels` to a `Legacy_Archive` folder. This is destructive to the "simulation" but necessary for "reality".

> [!WARNING]
> **God Mode**: The new Sentinel will BLOCK execution if no Wallet Address or Revenue Config is found. The system will refuse to "play pretend".

## Proposed Changes

### System/Core

#### [MODIFY] [monolith_core.py](file:///c:/Users/Teagan%20Holland/Desktop/Monolith_v4.5_Immortal/System/Core/monolith_core.py)

- Integrate "Hardened Sentinel" checks directly into the task loop.
- Remove "Mock Spending" logic.

### System/Agents (The Purge)

#### [NEW] `System/Agents/Legacy_Archive/` (Directory)

- All unverified agents moved here.

#### [KEEP] Verified Agents

- `micro_task_executor.py` (Real Money)
- `fiverr_gig_manager.py` (Real Assets)
- `gumroad_bridge.py` (Real Bridge)

### System/Sentinels (The God Layer)

#### [MODIFY] [monolith_sentinel.py](file:///c:/Users/Teagan%20Holland/Desktop/Monolith_v4.5_Immortal/System/Agents/monolith_sentinel.py)

- **New Feature**: `verify_sovereignty()` - Checks for `BraveWallet` or `BTC_Address`.
- **New Feature**: `enforce_profitability()` - Halts system if Daily Burn > Daily Revenue.

### System/Identity

#### [NEW] `System/Identity/identity_prime.py`

- Stores "Proof of Life" (Wallet Addresses, API Keys).
- No more sqlite files for "Identity"; uses Environment Variables and Keyfiles.

## Verification Plan

### Automated Tests

- **Purge Verification**: Run `ls System/Agents` to ensure only <10 files remain.
- **Sentinel Check**: Run `python System/Agents/monolith_sentinel.py` and verify it fails (due to missing wallet) or passes (if configured).
- **Revenue Test**: Run `python System/Agents/micro_task_executor.py --check` to verify API connection.

### Manual Verification

- User must provide a valid Crypto Address or API Key to lift the Sentinel Block.
