# Implementation Plan - Monolith 'Real Mode' Activation

Transform 'Simulated' agents into 'Real World' assets and trigger immediate revenue generation.

## User Review Required

> [!IMPORTANT]
> This plan initiates **REAL** system scans and process launches.
>
> - **Tax Shield** will scan your actual hardware ID/Components.
> - **Ion.net** will be launched to start generating Crypto (Solana).
> - **Browser** will open for immediate signup to revenue platforms.

## Proposed Changes

### 1. Upgrade Agents to 'Real Mode'

#### [System/Agents/tax_shield_agent.py]

- **Current**: Scans hardcoded dictionary of assets.
- **Upgrade**: Implement `subprocess` calls to `wmic` / `powershell` to detect **ACTUAL** GPU (RTX 5090?), CPU, and RAM for tax write-off eligibility.

#### [System/Agents/accountant_agent.py]

- **Current**: Scrapers are simulated stubs.
- **Upgrade**: Add file-ingestion capability. Create a watched folder `Data/Financial_Slips` where you can drop PDF/CSV files, and the agent attempts to OCR/parse them (basic implementation). Refine tax logic for accurate 2026 BC brackets.

#### [System/Agents/cipher_agent.py]

- **Current**: Simple stub (verified).
- **Upgrade**: Implement actual file encryption/decryption methods for the `Data/Vault` directory using `cryptography` library (Fernet), ensuring 'Sovereign' security for your tax data.

### 2. Revenue Activation (The 'On' Switch)

#### [System/Agents/Active/ionet_manager.py]

- **Action**: Verify config and launch the worker subprocess.

#### [System/Agents/omnidirectional_revenue_scanner.py]

- **Action**: Execute the `launch_signup_pages` function for the top 3 'Quick Win' streams immediately.

## Verification Plan

### Automated Tests

- `tax_shield_agent.py`: Run and verify it outputs the *actual* hostname and GPU of this machine.
- `cipher_agent.py`: Create a dummy file, encrypt it, delete original, decrypt it, verify content matches.
- `ionet_manager.py`: Check if `io-worker` process is running via tasklist.

### Manual Verification

- User checks opened browser tabs for Revenue Signups.
- User verifies `Sentinels/*.done` files for "GREEN" status.
