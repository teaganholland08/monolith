# implementation_plan.md - Monolith "Real Revenue" Upgrade

Purge all simulation code and replace with real-world tracking and opportunity detection.

## User Review Required

> [!IMPORTANT]
> **SIMULATION PURGE**: The "RevenueHunter" currently fakes $0.15 earnings per loop. This will be removed. Revenue will theoretically drop to $0.00 until *real* income sources (Bandwidth apps, Freelance gigs) generate verified external returns.

> [!WARNING]
> **SUBSIDY HUNTER**: Government sites cannot be checked autonomously without login credentials. The `subsidy_hunter.py` will be converted from a "Fake Eligibility Checker" to a "Sovereign Compliance Checklist" that tracks your *manual* progress on these claims.

## Proposed Changes

### Core System

#### [MODIFY] [monolith_sentinel.py](file:///c:/Users/Teagan%20Holland/Desktop/Monolith_v4.5_Immortal/System/Agents/monolith_sentinel.py)

- **RevenueHunter**: Remove lines 109-113 (Simulated $0.15).
- **RevenueHunter**: Add logic to read `Logs/revenue.json` (from Hydra) and `sentinel_dir/bandwidth_farmer.status`.
- **IdentityBridge**: Add comment warning that "Proxy-ID" is currently a placeholder concept.

#### [MODIFY] [hydra.py](file:///c:/Users/Teagan%20Holland/Desktop/Monolith_v4.5_Immortal/Brain/hydra.py)

- Remove `if True:` override hacks; use proper configuration.
- Remove "Simulated/Fallback" blocks. If no RSS feed or Web3 connection, report "NO SIGNAL" instead of fake data.
- Ensure `log_revenue` writes to `Logs/revenue.json`.

### Agents

#### [MODIFY] [subsidy_hunter.py](file:///c:/Users/Teagan%20Holland/Desktop/Monolith_v4.5_Immortal/System/Agents/subsidy_hunter.py)

- Remove hardcoded "Powell River" return list.
- Implement a JSON-based checklist system (`Data/subsidy_tracker.json`).
- `check_eligibility` will now read the tracker and report "PENDING" items, prompting the user (via Sentinel log) to take action.

#### [NEW] [System/Agents/Active/bandwidth_farmer.py](file:///c:/Users/Teagan%20Holland/Desktop/Monolith_v4.5_Immortal/System/Agents/Active/bandwidth_farmer.py)

- (Already verified as real, but we will ensure it is called by Genesis/Sentinel). *No changes needed if Genesis calls it.*
- *Note*: Genesis calls `GrassNodeManager` and `IoNetGPUManager` but maybe not `BandwidthFarmer`? Need to check.

## Verification Plan

### Automated Tests

- **Run `hydra.py`**: Verify it scans RSS without crashing and writes to `OPPORTUNITY_INBOX.md`.
- **Run `monolith_sentinel.py`**: Verify `RevenueHunter` reports $0.00 (correct behavior) instead of fake money.

### Manual Verification

- **Check `Logs/revenue.json`**: Ensure no fake entries appear.
- **Run `subsidy_hunter.py`**: Verify it generates/reads the new `subsidy_tracker.json`.
