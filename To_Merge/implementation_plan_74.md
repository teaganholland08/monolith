# Implementation Plan - Hardening Monolith Core

# Goal Description

Transition Project Monolith from a simulation-heavy state to a "Real-World Execution" state. This involves hardening the `monolith_omega.py` integrator, ensuring `TradeProtocol` communicates effectively with the `BraveWalletAdapter`, and enforcing "God Rules" via the Treasurer.

## User Review Required
>
> [!IMPORTANT]
> This transition removes safety nets. The system will attempt to execute REAL transactions if funds are available.
> Confirm `treasurer_god_rules.json` contains appropriate safety limits (currently auditable).

## Proposed Changes

### System Core

#### [MODIFY] [monolith_omega.py](file:///c:/Users/Teagan Holland/Desktop/Monolith_v4.5_Immortal/monolith_omega.py)

- Remove any lingering `simulation_mode=True` defaults.
- Integrate `TradeProtocol` directly into the main loop.
- Add strict "Sentinel Checks" before any execution step.

### Finance System

#### [MODIFY] [trade_protocol.py](file:///c:/Users/Teagan Holland/Desktop/Monolith_v4.5_Immortal/System/Finance/trade_protocol.py)

- Ensure `execute_order` calls `BraveWalletAdapter` correctly.
- Implement proper return handling for failed real-world transactions.

#### [MODIFY] [brave_wallet_adapter.py](file:///c:/Users/Teagan Holland/Desktop/Monolith_v4.5_Immortal/System/Finance/brave_wallet_adapter.py)

- Verify `is_configured` logic checks for actual key presence/connection.
- Ensure `swap` or `send` methods exist and throw specific errors if execution fails (rather than generic crashes).

## Verification Plan

### Automated Tests

- Run `monolith_omega.py` in a dry-run mode (if preserved) to verify logic flow.
- Unit test `TradeProtocol` with a mock wallet to ensure error handling works.
