# Implementation Plan - Project Monolith: Real Revenue Activation

# Goal Description

The goal is to transition Project Monolith from a "Simulation/Placeholder" state to **Real-World Revenue Generation**. Currently, agents like `micro_task_executor` use mock data (`time.sleep(1)`). We will upgrade them to use **Real APIs** (Amazon MTurk via `boto3`) and robust "Companion Mode" workflows for platforms without APIs (Outlier, Appen). We will also harden the `sentinel_agent` to remove simulated checks and implement actual system integrity verification. Finally, we will verify the "Best in World" status by ensuring the Dashboard reflects *real* data.

## User Review Required
>
> [!IMPORTANT]
> **Real Money Requires Real Credentials**: This update adds code to use `boto3` for Amazon MTurk. You MUST provide your AWS Access Key and Secret Key in `System/Config/micro_tasks.json` for this to work. I cannot bypass Amazon's auth.

> [!WARNING]
> **Browser Automation**: For platforms like Outlier, the agent will guide you to perform tasks. Fully autonomous "botting" of these platforms often leads to bans. The "Best in World" approach for 2026 is **Augmentation** (Agent prepares work, Human approves), not undetectable botting.

## Proposed Changes

### System/Agents

#### [MODIFY] [micro_task_executor.py](file:///c:/Users/Teagan%20Holland/Desktop/Monolith_v4.5_Immortal/System/Agents/micro_task_executor.py)

- **Remove**: Mock task lists and simulated `time.sleep` execution.
- **Add**: `boto3` integration to fetch *real* MTurk tasks (HITs).
- **Add**: Logic to filter HITs by reward amount (e.g., >$0.05).
- **Add**: "Companion Mode" prompt for Outlier/Appen that opens the specific task URL and waits for user confirmation of completion.

#### [MODIFY] [sentinel_agent.py](file:///c:/Users/Teagan%20Holland/Desktop/Monolith_v4.5_Immortal/System/Agents/sentinel_agent.py)

- **Remove**: "Simulated" jurisdiction checks.
- **Add**: Real file integrity hashing (SHA-256) of core agent files to detect unauthorized changes.
- **Add**: Real disk space and memory monitoring (removing stubbed checks).

### System/Config

#### [MODIFY] [micro_tasks.json](file:///c:/Users/Teagan%20Holland/Desktop/Monolith_v4.5_Immortal/System/Config/micro_tasks.json)

- **Update**: Ensure structure supports new `boto3` keys and "Companion Mode" flags.

### Dependencies

#### [MODIFY] [requirements.txt](file:///c:/Users/Teagan%20Holland/Desktop/Monolith_v4.5_Immortal/requirements.txt)

- **Add**: `boto3` (AWS SDK), `rich` (for "Best in World" terminal UI).

## Verification Plan

### Automated Tests

- **MTurk Connectivity**: Run `micro_task_executor.py` with a flag `--test-connection`. It should attempt `mturk.get_account_balance()` and report success or specific auth error (not generic failure).
- **Sentinel Integrity**: Run `sentinel_agent.py`. It should generate a real hash of `micro_task_executor.py` and print it. Modifying `micro_task_executor.py` and rerunning Sentinel should trigger an alert.

### Manual Verification

1. **Config Setup**: User (or Agent via instruction) adds dummy keys to `micro_tasks.json` to verify the "setup required" logic is replaced by "auth failed" (proving it tried to connect).
2. **Dashboard**: Launch `monolith_dashboard.py` and verify it shows "Real" mode active.
