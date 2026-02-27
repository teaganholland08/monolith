# IMPEMENTATION PLAN - PROJECT MONOLITH: OMNISCOUT-PRIME UPGRADE

Based on the "Master Instruction Set" directive, this plan consolidates the system into a single sovereign autonomous entity.

## User Review Required

> [!IMPORTANT]
> This plan merges `monolith.py` (Executor) and `monolith_prime.py` (Builder) into a single `monolith_core.py`.
> It also enforces "God Rules" at the kernel level.
> Confirm if any existing hardcoded rules in `monolith.py` (like $20k buffer) should be adjusted for the "Start from $0" directive. (Assumption: We will lower buffer for Genesis phase).

## Proposed Changes

### 1. Unification: The Monolith Core

Merge the recursive building capability of `Prime` with the safety/execution loop of `Orchestrator`.

#### [NEW] [System/Core/monolith_core.py](file:///c:/Users/Teagan%20Holland/Desktop/Monolith_v4.5_Immortal/System/Core/monolith_core.py)

- **Class**: `MonolithCore`
- **Responsibilities**:
  - Master Event Loop (Pulse)
  - Database Management (Memory)
  - Agent Orchestration (Spawn/Kill)
  - Sentinel Enforcement (Safety)
- **Features**:
  - `scheduler`: Priority queue for tasks.
  - `sandbox`: Wrapper for `subprocess` with resource limits.
  - `router`: Internal API routing between agents.

### 2. Sentinel Layer Enhancement

Upgrade the Sentinel to be a blocking gatekeeper for ALL actions.

#### [MODIFY] [System/Agents/monolith_sentinel.py](file:///c:/Users/Teagan%20Holland/Desktop/Monolith_v4.5_Immortal/System/Agents/monolith_sentinel.py)

- Integrate `GodRules` logic directly from `monolith.py`.
- Add `verify_execution(plan)` method that agents must call before acting.
- Add `monitor_resources()` to kill runaway processes.

### 3. Missing Infrastructure

#### [NEW] [System/Core/scheduler.py](file:///c:/Users/Teagan%20Holland/Desktop/Monolith_v4.5_Immortal/System/Core/scheduler.py)

- Simple, persistent task queue using SQLite.
- Supports Cron-like recurring tasks.

#### [NEW] [System/Core/sandbox_win.py](file:///c:/Users/Teagan%20Holland/Desktop/Monolith_v4.5_Immortal/System/Core/sandbox_win.py)

- Windows-specific process isolation (Job Objects if possible, or strict PID monitoring).

### 4. Revenue Activation Upgrades

#### [MODIFY] [Brain/hydra.py](file:///c:/Users/Teagan%20Holland/Desktop/Monolith_v4.5_Immortal/Brain/hydra.py)

- Ensure it uses the new `monolith_core` for task dispatch.
- Remove any remaining simulation stubs.

## Verification Plan

### Automated Verification

1. **Core Loop Test**
    - Run `python System/Core/monolith_core.py --test`
    - Verify it creates the DB, spawns a test agent, and respects a mock Sentinel block.
2. **Sentinel Blocking Test**
    - Submit a "Spend $1M" task.
    - Verify Sentinel rejects it with "Insufficient Funds/buffer".

### Manual Verification

1. **Dashboard Check**: Launch `monolith_dashboard.py` and verify it connects to the new `monolith_core` DB.
2. **Process Monitor**: Verify agents are spawned as subprocesses and killed correctly by the Sentinel.
