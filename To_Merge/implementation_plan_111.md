# Sovereign Architecture Reconstruction Plan

## Goal Description

Rebuild the missing "Real World" layers of Project Monolith to achieve zero-touch autonomous operation. This includes a Sovereign Identity foundation, a specialized Sentinel Swarm for governance, and the actual code for revenue agents that are currently just placeholders in the Orchestrator.

## User Review Required
>
> [!IMPORTANT]
> **Identity & Financial Connection**: The system will require interaction with real-world wallets and APIs. I will build the `IdentityPrime` and `WalletManager` structures, but you (or the system via `notify_user`) will need to provide the actual keys/seeds during the activation phase.

> [!WARNING]
> **Sentinel Authority**: The new `SentinelSwarm` will have the authority to HALT the system if financial or legal parameters are violated. This is designed to prevent "burn" and "hallucination".

## Proposed Changes

### 1. Identity Layer [NEW]

Create `System/Identity/` to handle sovereign credentials and wallets.

#### [NEW] [identity_prime.py](file:///c:/Users/Teagan%20Holland/Desktop/Monolith_v4.5_Immortal/System/Identity/identity_prime.py)

- Root identity manager. Stores hashed credentials, manages "Proof of Life".

#### [NEW] [wallet_manager.py](file:///c:/Users/Teagan%20Holland/Desktop/Monolith_v4.5_Immortal/System/Identity/wallet_manager.py)

- secure interface for crypto wallets (Brave/Metamask/Hardware).

### 2. Sentinel Swarm [NEW]

Populate `System/Agents/Sentinels/` (currently empty) with specialized guardians.

#### [MODIFY] [monolith_sentinel.py](file:///c:/Users/Teagan%20Holland/Desktop/Monolith_v4.5_Immortal/System/Agents/monolith_sentinel.py)

- Refactor to become the "Orchestrator of Sentinels" rather than doing everything itself.

#### [NEW] [legal_sentinel.py](file:///c:/Users/Teagan%20Holland/Desktop/Monolith_v4.5_Immortal/System/Agents/Sentinels/legal_sentinel.py)

- Checks TOS compliance and jurisdictional risk.

#### [NEW] [financial_sentinel.py](file:///c:/Users/Teagan%20Holland/Desktop/Monolith_v4.5_Immortal/System/Agents/Sentinels/financial_sentinel.py)

- Real-time ROI and burn-rate monitor. Enforces "Profitability First".

### 3. Revenue Agents [NEW]

Implement the missing agents referenced in `revenue_orchestrator.py`.

#### [NEW] [ionet_gpu_manager.py](file:///c:/Users/Teagan%20Holland/Desktop/Monolith_v4.5_Immortal/System/Agents/ionet_gpu_manager.py)

- Agent to manage IO.net GPU worker nodes.

#### [NEW] [grass_node_manager.py](file:///c:/Users/Teagan%20Holland/Desktop/Monolith_v4.5_Immortal/System/Agents/grass_node_manager.py)

- Agent to manage GetGrass bandwidth sharing.

#### [NEW] [trade_protocol.py](file:///c:/Users/Teagan%20Holland/Desktop/Monolith_v4.5_Immortal/System/Agents/trade_protocol.py)

- Basic interface for CEX/DEX trading (low-risk starts).

## Verification Plan

### Automated Tests

1. **Identity Verification**: Run `identity_prime.verify_sovereignty()` (expect False initially, then True after mock key injection).
2. **Sentinel Block Test**: Trigger a fake $1M spend task via `monolith_core`. Verify `FinancialSentinel` blocks it.
3. **Revenue Agent Dry-Run**: Run `ionet_gpu_manager.py --dry-run` to ensure API connection logic is sound.

### Manual Verification

- Review `task.md` updates.
- Confirm "GENESIS COMPLETE" message in `monolith_omega.py` output encompasses the new layers.
