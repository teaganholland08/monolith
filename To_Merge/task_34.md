# Task: Hardening Monolith Core - Real-World Execution

## Phase 1: Core Audit & Hardening

- [ ] Audit `monolith_omega.py` (Core Orchestrator) for simulation logic [/]
- [ ] Audit `trade_protocol.py` for execution gaps [/]
- [ ] Audit `brave_wallet_adapter.py` for connection readiness
- [ ] Define "God Rules" integration points in Core

## Phase 2: Integration & Sentinel Enforcement

- [ ] Refactor `monolith_omega.py` to strictly enforce `Treasurer` rules
- [ ] Connect `RevenueOrchestrator` to `TradeProtocol` (Real Mode)
- [ ] Verify `BraveWalletAdapter` can sign/execute (or handles failure gracefully)

## Phase 3: Verification

- [ ] Verify System Start with NO simulation flags
- [ ] Verify "Hardware Sentinel" constraints
