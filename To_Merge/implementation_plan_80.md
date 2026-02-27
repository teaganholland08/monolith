# IMPLEMENATION PLAN: Node Alpha & IP Engines

## Goal

Implement missing "Node Alpha" and the granular "IP Arbitrage" engines defined in the blueprint but missing from the file system.

## New Agents

### 1. `System/Agents/node_alpha_high_ticket.py`

**Purpose**: "Node Alpha" - The High-Ticket Client Sniper.
**Function**: Scans social platforms (Twitter/LinkedIn/Reddit) for high-intent keywords ("looking for AI developer", "need automation expert").
**Why Alpha?**: High value, immediate revenue, "First" in the funnel (Direct intent).

### 2. `System/Agents/patent_hunter.py`

**Purpose**: Scans for expired patents with commercial viability.
**Source**: `IP_ARBITRAGE_ENGINE.md` spec.

### 3. `System/Agents/viral_loop.py`

**Purpose**: Social media engagement engine interaction.
**Source**: `IP_ARBITRAGE_ENGINE.md` spec.

### 4. `System/Agents/ghostwriter.py`

**Purpose**: KDP Automation (Book generation).
**Source**: `IP_ARBITRAGE_ENGINE.md` spec.

## Fix Verification

- Create `FIX_REVENUE.bat` to help user install `nuclei` and other external tools.
- Update `monolith_prime.py` (if needed, but it auto-scans).

## User Review

- None required (User said "No questions, just execution").
