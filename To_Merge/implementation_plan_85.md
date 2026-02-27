# Reality-First Revenue Activation Plan - Project Monolith

**Goal**: Activate real-world revenue generation ("Real Money Now") starting from $0, bypassing the user's lack of bank account/ID by using self-custodied crypto wallets.

## User Review Required
>
> [!IMPORTANT]
> **Wallet Security**: This plan involves generating real cryptocurrency wallets. The **Private Keys** will be generated on your local machine and saved to `System/Config/secrets.env`. You MUST back these up offline (write them down) immediately after generation.

> [!WARNING]
> **Real-World Interaction**: This script will open browser windows and attempting to download mining/node software (io.net worker). You must approve these actions when they pop up.

## Proposed Changes

### 1. Financial Sovereignty Layer (The "No Bank" Fix)

**Component**: `System/Agents`

#### [NEW] `wallet_generator.py`

- **Purpose**: Generates a Solana Keypair (for io.net payouts) and a Bitcoin Address (for reserve).
- **Logic**:
  - Uses lightweight cryptographic libraries to generate keys locally.
  - Saves **Public Keys** to `System/Config/ionet_config.json`.
  - Saves **Private Keys** to `System/Config/secrets_do_not_share.json` (protected).
  - Prints the "Mnemonic" for the user to write down.

### 2. Revenue Agent Activation

**Component**: `System/Agents`

#### [MODIFY] `ionet_gpu_manager.py`

- **Change**: Add auto-detection of the generated wallet. If config is missing, it calls `wallet_generator`.
- **Change**: Add a specific `install_worker` function that downloads the signed io.net binary/script for Windows.

#### [MODIFY] `grass_node_manager.py`

- **Change**: Update defaults to "Enabled: True".
- **Change**: Add logic to check for the Chrome Extension process or warn if not installed.

### 3. System Orchestration

**Component**: `System/Core`

#### [NEW] `revenue_bootstrap.py`

- **Purpose**: The "Master Switch".
- **Steps**:
    1. Check for Wallets -> Generate if missing.
    2. Configure Agents -> Inject wallets/emails.
    3. Launch IO.Net Worker (or Docker container).
    4. Launch Grass Monitor.
    5. Start Treasurer to watch for incoming $.

## Verification Plan

### Automated Tests

- **Wallet Gen Test**: Run `python System/Agents/wallet_generator.py --test` to verify key format (without saving).
- **Config Injection**: Verify `ionet_config.json` contains a valid-looking Solana address.

### Manual Verification

- **Browser Check**: The system will open the io.net worker download page. User must confirm the download starts.
- **Process Check**: User runs `python System/Core/revenue_bootstrap.py` and confirms "Status: Active" for agents.
