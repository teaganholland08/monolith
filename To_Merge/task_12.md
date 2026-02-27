# Project Monolith Audit & Recovery

## System Audit

- [x] Audit Core Loop (`System/Core/genesis.py`, `Brain/hydra.py`) <!-- id: 0 -->
- [x] Audit Sentinel Layer (`System/Sentinels`) <!-- id: 1 -->
- [x] Audit Revenue Agents (`System/Agents/*.py`) <!-- id: 2 -->
  - [x] `subsidy_hunter.py`
  - [x] `omnidirectional_revenue_scanner.py`
  - [x] `bandwidth_farmer.py`
- [x] Check for hardcoded/simulation logic <!-- id: 3 -->

## Strategic Evolution (Fixes)

- [x] Replace hardcoded locations in `subsidy_hunter.py` with dynamic config <!-- id: 4 -->
- [x] Implement/Update `SubsidyHunter` to be fully operational <!-- id: 5 -->
- [x] Ensure `Sentinel` oversight is active <!-- id: 6 -->

## Revenue & Scale

- [x] Verify `bandwidth_farmer.py` functionality <!-- id: 7 -->
- [x] Verify `omnidirectional_revenue_scanner.py` functionality <!-- id: 8 -->

## Identity & Banking

- [ ] Assess current state of Identity/Banking modules <!-- id: 9 -->
