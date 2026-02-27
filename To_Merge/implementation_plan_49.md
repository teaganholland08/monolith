# Phase 4: Sentinel & Governance System - Implementation Plan

## Goal Description

With the Operator (Phase 2) and Factory (Phase 3) active, the system is powerful but dangerous.
**Phase 4 Goal:** Harden the `Sentinel` layer to prevent the system from spending money it doesn't have, hallucinating facts, or breaking loops.

## Proposed Changes

### System.Agents

#### [NEW] [sentinel_swarm.py](file:///c:/Users/Teagan%20Holland/Desktop/Monolith_v4.5_Immortal/System/Agents/sentinel_swarm.py)

Decompose `monolith_sentinel.py` into specialized sub-sentinels:

1. **RealitySentinel:** Verifies data against external truth (Blockchain, trusted APIs).
2. **FinancialSentinel:** Enforces "Spend < Revenue" and "Zero Credit" rules.
3. **LoopSentinel:** Prevents infinite loops and CPU hogs.

#### [MODIFY] [monolith_sentinel.py](file:///c:/Users/Teagan%20Holland/Desktop/Monolith_v4.5_Immortal/System/Agents/monolith_sentinel.py)

- **Integration:** Act as the Supervisor, delegating checks to the Swarm.
- **Override:** Allow "God Mode" override only with cryptographic signature (or admin flag).

### System.Config

#### [NEW] [governance_constitution.json](file:///c:/Users/Teagan%20Holland/Desktop/Monolith_v4.5_Immortal/System/Config/governance_constitution.json)

- Hardcoded laws (e.g., "Cannot edit System/Core/monolith_omega.py").

## Verification Plan

1. **Insolvency Test:** Try to spend $1000 with $0 balance. Sentinel MUST block.
2. **Hallucination Test:** Try to log a fake fact without citation. RealitySentinel should flag.
