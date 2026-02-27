# Project Monolith - Master Autonomous Execution Plan

## Goal Description

Unify Project Monolith into a single, sovereign, autonomous system "Project Monolith v5.5 IMMORTAL".
Replace fragmented scripts (`monolith_prime.py`, `monolith.py`) with a centralized Master Entry Point (`monolith_omega.py`) that utilizes the robust `System/Core` library.
Ensure "God Rules" are universally enforced via a unified Sentinel configuration.
Connect the Revenue Orchestrator to the Master Scheduler.

## User Review Required
>
> [!IMPORTANT]
> This plan deprecates `monolith_prime.py` and `monolith.py` in favor of `monolith_omega.py` as the single source of truth.

> [!WARNING]
> "God Rules" will be enforced system-wide. Ensure `System/Config/treasurer_god_rules.json` is configured correctly, or the system may block all spending.

## Proposed Changes

### 1. Unified Entry Point (`monolith_omega.py`)

Create a new master script that:

- Initializes `MonolithCore`.
- Loads `RevenueOrchestrator`.
- Runs a "Genesis Boot" sequence (Identity check, Wallet check, Sentinel sweep).
- Enters the `MonolithCore.run_forever()` loop.
- **Location**: Root directory

### 2. Sentinel Configuration Hardening

Update `System/Agents/monolith_sentinel.py` to:

- Load `treasurer_god_rules.json` from `System/Config` instead of using hardcoded defaults.
- Enforce the "Survival Buffer" and "Max Auto Spend" rules dynamically.

### 3. Revenue Orchestrator Integration

Update `System/Core/revenue_orchestrator.py` to:

- Accept a `scheduler` instance in `__init__`.
- Instead of running tasks directly, `.add_task()` to the `MonolithScheduler`.
- This ensures the Core execution loop handles the actual processing (subject to Sentinel checks).

### 4. Scheduler Enhancement

Update `System/Core/monolith_core.py` to:

- Integrate `RevenueOrchestrator` logic into the `run_forever` loop (e.g., periodic scan).

## Verification Plan

### Automated Tests

1. **Config Loading Test**: Verify `MonolithSentinel` correctly loads limits from `treasurer_god_rules.json`.
2. **Task Flow Test**:
    - Trigger `RevenueOrchestrator` to generate a task.
    - Verify task appears in `ledger.db` (tasks table).
    - Run `MonolithCore` for 1 distinct loop.
    - Verify task is executed (or blocked/marked complete).

### Manual Verification

1. Run `python monolith_omega.py --test-genesis` (I will add this flag).
2. Observe "Genesis Sequence" in terminal.
3. Confirm "Sentinel Status: ONLINE".
4. Confirm "Revenue Orchestrator: SCANNING".
