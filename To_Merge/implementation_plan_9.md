# Brave Wallet Integration Plan

## Goal

Integrate the user's Brave Wallet into Project Monolith. This will allow the system to recognize a real crypto storage location, track balances (via public explorers or manual input), and direct revenue streams to this wallet.

## User Review Required
>
> [!IMPORTANT]
> **Public Address Needed**: I will need your Brave Wallet's public address (e.g., Ethereum/Solana address) to configure the system. I will NOT ask for private keys.

> [!NOTE]
> **Manual vs API**: Initially, the system will use public block explorers (like Etherscan free tier) or manual user input to track balances, as direct browser wallet integration requires complex browser automation that might be brittle.

## Proposed Changes

### System/Config

#### [NEW] [brave_wallet.json](file:///c:/Users/Teagan%20Holland/Desktop/Monolith_v4.5_Immortal/System/Config/brave_wallet.json)

- New configuration file to store:
  - `wallet_type`: "Brave"
  - `networks`: ["ETH", "SOL", "BSC"]
  - `addresses`: { "ETH": "...", "SOL": "..." }

### System/Finance

#### [NEW] [brave_wallet_adapter.py](file:///c:/Users/Teagan%20Holland/Desktop/Monolith_v4.5_Immortal/System/Finance/brave_wallet_adapter.py)

- `BraveWalletAdapter` class:
  - `load_config()`: Reads `brave_wallet.json`.
  - `get_balance(asset)`: Returns balance (initially mock/manual, extensible to API).
  - `get_deposit_address(network)`: Returns the address for revenue agents.

#### [MODIFY] [trade_protocol.py](file:///c:/Users/Teagan%20Holland/Desktop/Monolith_v4.5_Immortal/System/Finance/trade_protocol.py)

- Import `BraveWalletAdapter`.
- Update `execute_paper_trade` (or add `execute_real_trade`) to reference the wallet adapter.

## Verification Plan

### Automated Tests

- Create a test script `System/Finance/test_wallet_integration.py`:
  - Initialize `BraveWalletAdapter`.
  - Check if config loads (it should fail gracefully or ask for input if empty).
  - Print the "Deposit Address" for ETH.

### Manual Verification

1. Run the test script.
2. Verify it correctly identifies the "Brave Wallet" as the active treasury.
