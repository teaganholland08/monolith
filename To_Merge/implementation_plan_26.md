# Project Monolith Phase Alpha-Zero Implementation Plan

## User Review Required
>
> [!IMPORTANT]
> **Real Money Execution**: The system is migrating to live execution. Ensure all API keys (if any are added later) are valid.
> **Permission Audit**: The system will explicitly check for elevated privileges (Admin/Sudo) to prevent "Zombie Loops".

## Proposed Changes

### Core System Upgrades (`System/Core`)

#### [NEW] [agent_ops.py](file:///C:/Users/Teagan%20Holland/Desktop/Monolith_v4.5_Immortal/System/Core/agent_ops.py)

- **Purpose**: Real-time telemetry monitoring for agents.
- **Features**: Drift detection, success rate tracking, automatic "zombie" process cleaning.

#### [NEW] [mcp_bridge.py](file:///C:/Users/Teagan%20Holland/Desktop/Monolith_v4.5_Immortal/System/Core/mcp_bridge.py)

- **Purpose**: Standardized Model Context Protocol bridge.
- **Features**: Interface for agents to call external tools (Search, Python) natively.

### Intelligence & Finance Layers

#### [NEW] [academy.py](file:///C:/Users/Teagan%20Holland/Desktop/Monolith_v4.5_Immortal/System/Intelligence/academy.py)

- **Purpose**: "The Academy" - Automated knowledge scraper.
- **Location**: `System/Intelligence`

#### [NEW] [trade_protocol.py](file:///C:/Users/Teagan%20Holland/Desktop/Monolith_v4.5_Immortal/System/Finance/trade_protocol.py)

- **Purpose**: "Trade Protocol" - Barter/Arbitrage engine logic.
- **Location**: `System/Finance`

### Monolith Prime (`monolith_prime.py`)

#### [MODIFY] [monolith_prime.py](file:///C:/Users/Teagan%20Holland/Desktop/Monolith_v4.5_Immortal/monolith_prime.py)

- **Fix**: Inject `HOME` environment variable into subprocesses (Antigravity fix).
- **Fix**: Add Pre-Flight Permission Audit in `bootstrap`.
- **Feature**: Integrate `AgentOps` for monitoring `run_agent` calls.

### Monolith Dashboard (`monolith_api.py`)

#### [MODIFY] [monolith_api.py](file:///C:/Users/Teagan%20Holland/Desktop/Monolith_v4.5_Immortal/monolith_api.py)

- Ensure endpoints connect to the new `AgentOps` telemetry if available.

### Installation & Config

#### [MODIFY] [monolith_install.ps1](file:///C:/Users/Teagan%20Holland/Desktop/Monolith_v4.5_Immortal/monolith_install.ps1)

- Add verification step for Python wheels/dependencies to prevent syntax errors.

## Verification Plan

### Automated Verification

- **Unit Tests**:
  - Create `tests/test_agent_ops.py` to verify telemetry recording.
  - Create `tests/test_mcp_bridge.py` to verify tool interface.
- **System Check**:
  - Run `python final_integrity_check.py` (will update this script to include new layers).

### Manual Verification

- **Boot Test**: Run `python monolith_prime.py` and observe:
  - No "Missing HOME" errors.
  - "Pre-Flight" permission check output.
  - Agents being spawned and monitored by AgentOps.
- **Dashboard**: Run `python monolith_api.py` and check `localhost:8000/status` to see real-time agent data.
