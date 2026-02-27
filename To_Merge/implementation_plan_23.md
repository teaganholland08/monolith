# Monolith v6.0 "Sovereign" Implementation Plan

## Goal Description

Project Monolith currently uses "simulated" agents that output hardcoded placeholders. The goal is to upgrade these into **Active Agents** that:

1. **Creative Engine**: Actually *generates* the digital assets (images, text) using available tools.
2. **Revenue Scanner**: Actually *scans* the web for real-time trends instead of using static lists.
3. **Growth Engine**: Tracks a real local ledger (`ledger.csv`) instead of simulated JSON streams.

This moves the system from "Roleplay" to "Real Utility," directly aiding the user in generating revenue by providing finished goods (assets) and real market intelligence.

## User Review Required
>
> [!IMPORTANT]
> **Asset Generation**: The system will start generating *real* images and text files in `Monolith_v4.5_Immortal/Assets`. This requires disk space.
> **Web Search**: The system will perform active web searches to find trends.

## Proposed Changes

### System/Agents

#### [MODIFY] [omnidirectional_revenue_scanner.py](file:///c:/Users/Teagan%20Holland/Desktop/Monolith_v4.5_Immortal/System/Agents/omnidirectional_revenue_scanner.py)

- **Change**: Replace hardcoded `_scan_digital_products` lists with a dynamic function that uses `search_web` (via a wrapper or prompt instruction) to find *current* trends on Redbubble, Etsy, and Stock sites.
- **Output**: Returns a list of *currently trending* niches (e.g., "Retrowave Cat", "Minimalist Planner").

#### [MODIFY] [creative_engine.py](file:///c:/Users/Teagan%20Holland/Desktop/Monolith_v4.5_Immortal/System/Agents/Creators/creative_engine.py)

- **Change**: Add a `generate_real_assets()` method.
- **Logic**:
    1. Read trends from the Revenue Scanner.
    2. Use the `generate_image` tool (via instructions to the agent) to creating the actual .png files in `Assets/Images`.
    3. Generate text descriptions/tags in `Assets/Metadata`.

#### [MODIFY] [system_growth_engine.py](file:///c:/Users/Teagan%20Holland/Desktop/Monolith_v4.5_Immortal/System/Agents/system_growth_engine.py)

- **Change**: implementations of `get_total_capital` to read from a simple `Data/ledger.csv`.
- **Change**: `decide_next_move` to provide specific, dynamic advice based on the actual ledger balance.

### System/Data

#### [NEW] [ledger.csv](file:///c:/Users/Teagan%20Holland/Desktop/Monolith_v4.5_Immortal/Data/ledger.csv)

- **Content**: `Date,Type,Amount,Category,Description`
- **Purpose**: Single source of truth for revenue tracking.

### Root

#### [MODIFY] [INSTANT_REVENUE_ACTIVATION.bat](file:///c:/Users/Teagan%20Holland/Desktop/Monolith_v4.5_Immortal/INSTANT_REVENUE_ACTIVATION.bat)

- **Change**: Add step to verify `Assets` folder exists and populate it if empty.
- **Change**: Open the `Assets` folder for the user to immediately drag-and-drop to the opened browser tabs.

## Verification Plan

### Automated Tests

- **verify_assets.py**: A script to check if `Assets/Images` contains files after the Creative Engine runs.
- **verify_scanner.py**: A script to mock the web search and ensure the Scanner returns dynamic data structures.

### Manual Verification

1. Run `INSTANT_REVENUE_ACTIVATION.bat`.
2. **Verify**: Browser tabs open AND the `Assets` folder opens containing fresh, high-quality images ready for upload.
3. **Verify**: The `scanner.done` sentinel file contains *current* date/trends, not hardcoded ones.
