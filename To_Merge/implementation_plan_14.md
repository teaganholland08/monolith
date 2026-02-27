# Implementation Plan - Phase Alpha-Real: Wallet & Compute

# Goal Description

1. **Generate Crypto Authority**: The user has "no wallet". I will generate a secure Solana Keypair (local file) so the system has a destination for payments.
2. **Fix IO.net Manager**: The `ionet_gpu_manager.py` calls a `start_worker()` method that does not exist. I will implement this method to download/install/run the IO.net worker binary.

## User Review Required
>
> [!IMPORTANT]
> **Wallet Generation**: I will generate a **Solana Keypair**. The Private Key will be saved to `C:\Users\Teagan Holland\Desktop\Monolith_v4.5_Immortal\Brain\vault_key.json`. **YOU MUST BACK THIS UP.** If you lose this file, you lose the funds.

## Proposed Changes

### Financial Identity

#### [NEW] [generate_wallet.py](file:///c:/Users/Teagan%20Holland/Desktop/Monolith_v4.5_Immortal/System/Core/generate_wallet.py)

- Script to generate a fresh Solana Keypair.
- Save Public Key to `System/Config/ionet_config.json` (for Treasurer/IO.net).
- Save Private Key to `Brain/vault_key.json` (Encrypted/Restricted if possible, but JSON for now as per "Speed" request).

### Compute Monetization

#### [MODIFY] [ionet_gpu_manager.py](file:///c:/Users/Teagan%20Holland/Desktop/Monolith_v4.5_Immortal/System/Agents/ionet_gpu_manager.py)

- **Implement `start_worker()`**:
  - Check for `launcher.py` or binary.
  - If missing, download from IO.net (or simulate the command if download is complex without auth).
  - Execute the worker process.
  - Save PID to `worker_process.json`.

## Verification Plan

### Automated Tests

- Run `generate_wallet.py` -> Verify `ionet_config.json` contains a valid address.
- Run `ionet_gpu_manager.py` -> Verify it attempts to start the worker and doesn't crash on "Method Not Found".
