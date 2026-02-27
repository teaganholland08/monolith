# IMPLEMENTATION PLAN: PHASE 4 & 5 (SOVEREIGNTY & REVENUE)

## Goal

Establish cryptographic sovereignty (Real Wallet) and activate the first line of revenue (Zero-Capital Streams).

## User Review Required
>
> [!IMPORTANT]
> **Real Keys**: We will generate a REAL Ethereum wallet. The Private Key will be encrypted locally in `SecureData/Identity/vault.json`.
> **Loss Risk**: If this local file is deleted, the identity is lost forever.

## Proposed Changes

### System/Identity (Sovereignty)

#### [MODIFY] [identity_prime.py](file:///c:/Users/Teagan%20Holland/Desktop/Monolith_v4.5_Immortal/System/Identity/identity_prime.py)

- Integrate `eth_account`.
- Implement `generate_sovereign_wallet()`:
  - Generates new ETH Account.
  - Encrypts Private Key with a local system salt.
  - Saves to `vault.enc`.

### System/Core (Revenue)

#### [MODIFY] [revenue_orchestrator.py](file:///c:/Users/Teagan%20Holland/Desktop/Monolith_v4.5_Immortal/System/Core/revenue_orchestrator.py)

- Auto-enable `micro_task_executor` if wallet exists.

## Verification Plan

### Automated Tests

1. **Wallet Gen**: Run `identity_prime.py` and verify `vault.enc` is created and `verify_sovereignty()` returns True.
2. **Sentinel Check**: Run `verify_sentinels.py` again. Financial checks should now PASS (because wallet exists).

### Manual Verification

- Check specific file paths for keys.
