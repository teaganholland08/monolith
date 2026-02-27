# Implementation Plan - Project Monolith: Real Revenue Activation

# Goal Description

The current system contains "Mock" agents (specifically `revenue_tracker.py` and `monolith_prime.py` bootstrap logic) that simulate data with random numbers. The goal is to replace these with **Real Execution** logic. We will:

1. Replace `random` revenue generation with a real `Ledger` system.
2. Upgrade `Revenue Scanner` to perform *actual* availability checks where possible.
3. Create a `Web Gig Scanner` to find real-time opportunities.
4. Ensure `monolith_prime.py` recognizes all 69+ existing agents.

## User Review Required
>
> [!IMPORTANT]
> **No Simulation Policy**: All `random` generation will be removed. Revenue will show as **$0.00** until *actual* income is manually or automatically logged.
> **External Connections**: The new agents will attempt to connect to external sites (Outlier, Upwork, etc.) to check status.

## Proposed Changes

### System Core

#### [MODIFY] [monolith_prime.py](file:///c:/Users/Teagan%20Holland/Desktop/Monolith_v4.5_Immortal/monolith_prime.py)

- **Bootstrap Logic**: Remove the hardcoded "starter agents" string injection if the file already exists.
- **Agent Registry**: Modify `_init_agent_registry` to auto-discover all `.py` files in `System/Agents/` and register them if missing.

### Revenue System

#### [MODIFY] [revenue_tracker.py](file:///c:/Users/Teagan%20Holland/Desktop/Monolith_v4.5_Immortal/System/Agents/revenue_tracker.py)

- Remove `random.uniform`.
- Implement `LedgerReader` to sum up actual `REVENUE_INCOME` entries from `System/Logs/execution_log.jsonl`.
- Return $0.00 if no logs exist.

#### [MODIFY] [omnidirectional_revenue_scanner.py](file:///c:/Users/Teagan%20Holland/Desktop/Monolith_v4.5_Immortal/System/Agents/omnidirectional_revenue_scanner.py)

- Add `check_live_status()` method.
- Add `webbrowser.open()` calls to immediately launch signup pages for high-priority items (Outlier, etc.).

### New Agents

#### [NEW] [web_gig_scanner.py](file:///c:/Users/Teagan%20Holland/Desktop/Monolith_v4.5_Immortal/System/Agents/web_gig_scanner.py)

- **Purpose**: Find *real* current gigs.
- **Logic**: Use `requests` / `BeautifulSoup` (or `search_web` tool equivalent in Python if allowed, otherwise standard scraping) to fetch RSS feeds from RemoteOK, WeWorkRemotely.
- **Output**: `System/Sentinels/new_gigs.done` with list of URLs.

## Verification Plan

### Automated Tests

1. **Registry Sync**: Run `monolith_prime.py` and verify `sqlite3 System/Logs/ledger.db "SELECT count(*) FROM agent_registry"` returns > 50.
2. **Revenue Reality**: Run `revenue_tracker.py`. Verify output is `$0.00` (or actual sum), NOT a random number.
3. **Gig Scan**: Run `web_gig_scanner.py`. Verify it produces `System/Sentinels/new_gigs.done` with valid HTTP links (checking status 200).

### Manual Verification

- User will see "Real Revenue: $0.00" instead of fake numbers.
- User will be prompted to open real URLs for signup.
