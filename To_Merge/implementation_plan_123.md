# Phase Alpha-Zero Execution Plan

## Goal

Execute "Phase Alpha-Zero": Audit, Harden, and Activate Revenue. Transition Project Monolith to a live, "best-in-world" operational state.

## Proposed Changes

### [Infrastructure Hardening]

#### [NEW] [monolith_install.ps1](file:///c:/Users/Teagan/Holland/Desktop/Monolith_v4.5_Immortal/monolith_install.ps1)

- **Robustness**: Cross-platform checks, Python wheel verification, Environment Variable injection (HOME).
- **Function**: Replaces the old batch/powershell hybrid with a clean, idempotent installer.

#### [NEW] [System/Core/pre_flight_audit.py](file:///c:/Users/Teagan/Holland/Desktop/Monolith_v4.5_Immortal/System/Core/pre_flight_audit.py)

- **Function**: Checks for "Zombie" states, ensures sudo/admin permissions where needed (or handles lack thereof gracefully), verifies network connectivity.

### [Missing Layers]

#### [NEW] [System/Core/agent_ops.py](file:///c:/Users/Teagan/Holland/Desktop/Monolith_v4.5_Immortal/System/Core/agent_ops.py)

- **Feature**: Real-time telemetry, drift detection (token burn efficiency), and execution success tracking.

#### [NEW] [System/Agents/academy_agent.py](file:///c:/Users/Teagan/Holland/Desktop/Monolith_v4.5_Immortal/System/Agents/academy_agent.py)

- **Feature**: Automated knowledge scraper (Medical, Engineering, Tactical). Uses available search tools/APIs.

#### [NEW] [System/Agents/trade_protocol.py](file:///c:/Users/Teagan/Holland/Desktop/Monolith_v4.5_Immortal/System/Agents/trade_protocol.py)

- **Feature**: Barter and Crypto-Arbitrage engine logic.

### [Revenue Execution ($0 Start)]

#### [NEW] [System/Agents/content_agency.py](file:///c:/Users/Teagan/Holland/Desktop/Monolith_v4.5_Immortal/System/Agents/content_agency.py)

- **Logic**: Niche identification -> Content Generation -> Site Structure creation.

#### [NEW] [System/Agents/cloud_arbitrage.py](file:///c:/Users/Teagan/Holland/Desktop/Monolith_v4.5_Immortal/System/Agents/cloud_arbitrage.py)

- **Logic**: Scans for spot instances (logic for AWS/Azure APIs) and "resells" (calculates arbitrage margin).

#### [NEW] [System/Agents/bounty_swarm.py](file:///c:/Users/Teagan/Holland/Desktop/Monolith_v4.5_Immortal/System/Agents/bounty_swarm.py)

- **Logic**: GitHub API scanner for `help-wanted` + `bounty` tags.

### [Dashboard Upgrade]

#### [NEW] [monolith_api.py](file:///c:/Users/Teagan/Holland/Desktop/Monolith_v4.5_Immortal/monolith_api.py)

- **Tech**: FastAPI.
- **Endpoints**: `/status`, `/revenue`, `/agents/start`, `/agents/stop`.

#### [NEW] [UI/dashboard_modern.html](file:///c:/Users/Teagan/Holland/Desktop/Monolith_v4.5_Immortal/UI/dashboard_modern.html)

- **Tech**: Single-file HTML/JS (Vue.js via CDN for reliability).
- **Features**: Real-time stats, log streaming.

## Verification Plan

### Automated

1. Run `monolith_install.ps1` - Verify strict success.
2. Run `pre_flight_audit.py` - Check output.
3. Start `monolith_api.py` - Check health endpoint `localhost:8000/health`.
4. Run `content_agency.py` - Verify output directory of "generated" content.
5. Run `bounty_swarm.py` - Verify GitHub API connection (even if read-only).

### Manual

- User to open `UI/dashboard_modern.html` to see the Live Command Center.
