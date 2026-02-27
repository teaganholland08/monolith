# Project Monolith v4.5 - Enhancement Implementation Plan

## Overview

Enhance Project Monolith with automated account signup workflows, modernize missing components against 2026 best practices, fix remaining TODOs, and build browser automation to bridge gap between $0 and first revenue.

## User Review Required

> [!WARNING]
> **Account Creation Automation**: This plan includes browser automation using Playwright to help guide account creation for platforms like Phantom wallet, io.net, and Grass. While this automates navigation and form filling, you will still need to provide verification (email confirmations, etc.) and review the automated actions. The automation is designed to ASSIST, not bypass security or ToS.

> [!IMPORTANT]
> **Revenue Reality**: The system is already well-built (72 agents, 254 sentinels, robust tracking). The missing piece is human account creation on platforms. Once accounts are created and config files updated, the revenue tracking/reinvestment systems will activate automatically.

## Proposed Changes

### 1. Browser Automation Layer

#### [NEW] [account_creation_assistant.py](file:///c:/Users/Teagan%20Holland/Desktop/Monolith_v4.5_Immortal/System/Agents/account_creation_assistant.py)

**Purpose**: Playwright-based assistant to guide user through account creation workflows

**Features**:

- Automated navigation to signup pages
- Form auto-fill (where permitted)
- Step-by-step visual guidance
- Wallet address/email capture
- Config file auto-update after completion

**Platforms Supported**:

- Phantom wallet creation
- io.net worker signup  
- Grass extension installation guide
- PayPal/crypto exchange signups

---

### 2. Revenue Scanner Enhancements

#### [MODIFY] [omnidirectional_revenue_scanner.py](file:///c:/Users/Teagan%20Holland/Desktop/Monolith_v4.5_Immortal/System/Agents/omnidirectional_revenue_scanner.py)

**Changes**:

- Add 2026 platforms discovered from research:
  - **Gradient** (browser-based AI compute - earn EXP tokens)
  - **Kaisar Network** (idle GPU via browser extension)
  - **Nosana** (AI inference marketplace)
  - **Toloka AI** (data labeling tasks)
- Update revenue projections based on 2026 market rates
- Add verification status checking for each platform

---

### 3. Core Agent Fixes

#### [MODIFY] [architect.py](file:///c:/Users/Teagan%20Holland/Desktop/Monolith_v4.5_Immortal/Brain/architect.py)

**Fix**: Line 38 - Implement core architect logic for system oversight

**Implementation**:

- Add gap scanning loop
- Add system health monitoring
- Add autonomous repair triggers
- Hook into Director Schedule

#### [MODIFY] [ionet_gpu_manager.py](file:///c:/Users/Teagan%20Holland/Desktop/Monolith_v4.5_Immortal/System/Agents/ionet_gpu_manager.py)

**Fix**: Line 174 - Add process liveness checking  

**Implementation**:

- Use `psutil` to verify io-worker process is running
- Auto-restart on failure
- Report status to sentinel

---

### 4. State Management Enhancement

#### [NEW] [state_manager.py](file:///c:/Users/Teagan%20Holland/Desktop/Monolith_v4.5_Immortal/System/Core/state_manager.py)

**Purpose**: Centralized state management inspired by 2026 LangGraph best practices

**Features**:

- Global mission state tracking
- Agent coordination state
- Revenue stream activation status
- Milestone progress tracking
- Persistent state storage (JSON/SQLite)

---

### 5. Config Management Tools

#### [NEW] [config_validator.py](file:///c:/Users/Teagan%20Holland/Desktop/Monolith_v4.5_Immortal/System/Tools/config_validator.py)

**Purpose**: Validate and repair config files

**Features**:

- Check all config files for placeholder values
- Identify missing required fields
- Provide actionable fixes
- Auto-backup before changes

#### [NEW] [credential_manager.py](file:///c:/Users/Teagan%20Holland/Desktop/Monolith_v4.5_Immortal/System/Tools/credential_manager.py)

**Purpose**: Secure credential storage and retrieval

**Features**:

- Encrypted credential storage
- Wallet address management  
- API key rotation reminders
- Config file updates after account creation

---

### 6. Zero-Touch Revenue Activation

#### [NEW] [revenue_activation_orchestrator.py](file:///c:/Users/Teagan%20Holland/Desktop/Monolith_v4.5_Immortal/System/Agents/revenue_activation_orchestrator.py)

**Purpose**: Master coordinator for activating all revenue streams

**Workflow**:

1. Scan for missing accounts/credentials
2. Launch browser automation for each missing platform
3. Wait for user completion + verification
4. Update configs automaticallyassistant
5. Activate revenue tracking  
6. Report status to dashboard

---

## Verification Plan

### Automated Tests

1. **Config Validation Test**

   ```powershell
   cd "C:\Users\Teagan Holland\Desktop\Monolith_v4.5_Immortal"
   python -m pytest tests/test_config_validator.py -v
   ```

   - Verifies all config files can be parsed
   - Checks for missing fields
   - Tests backup/restore functionality

2. **State Manager Test**

   ```powershell
   python tests/test_state_manager.py
   ```

   - Verifies state persistence
   - Tests concurrent access
   - Validates state transitions

3. **Revenue Scanner Integration Test**  

   ```powershell
   python System/Agents/omnidirectional_revenue_scanner.py
   ```

   - Verify all new platforms are discovered
   - Check URL accessibility
   - Validate revenue projections

### Browser Automation Tests

1. **Account Creation Assistant (User-Guided)**

   ```powershell
   python System/Agents/account_creation_assistant.py --platform phantom --dryrun
   ```

   - Opens browser in dry-run mode
   - Navigates to Phantom wallet page
   - Shows form fill preview without submitting
   - User visually verifies automation is correct

2. **Full Activation Workflow Test**

   ```powershell  
   python System/Agents/revenue_activation_orchestrator.py --test-mode
   ```

   - Scans system for missing credentials
   - Lists required accounts
   - Launches browser guides (dry-run)
   - Reports what WOULD be activated

### Manual Verification

1. **User Completes One Platform Signup**
   - User runs: `python System/Agents/account_creation_assistant.py --platform phantom`
   - Browser opens, user creates wallet
   - Assistant captures Solana address
   - User confirms config was updated correctly in `System/Config/ionet_config.json`

2. **Revenue Tracking Verification**
   - After one platform is active (e.g., Grass extension running), wait 24 hours  
   - Run: `python System/Agents/revenue_tracker.py`
   - Verify `execution_log.jsonl` shows actual revenue events (not simulation)
   - Check sentinel file `System/Sentinels/revenue_tracker.done` for correct totals

3. **Reinvestment Logic Test**
   - Manually add test revenue entry to `Memory/revenue_orchestrator/earnings_log.json`:

     ```json
     [{"amount": 100, "source": "test", "timestamp": "2026-02-04T18:00:00"}]
     ```

   - Run: `python System/Agents/auto_reinvestor.py`
   - Verify output shows 80/15/5 split calculation
   - Check `reinvestment_log.json` was updated

---

## Success Criteria

- ✅ All 2 TODOs fixed and tested
- ✅ Browser automation opens correct pages and guides user
- ✅ Config validator detects placeholders and suggests fixes
- ✅ State manager persists data between runs
- ✅ Revenue scanner includes 4+ new 2026 platforms
- ✅ At least 1 manual account creation flow completed successfully
- ✅ Revenue tracking shows real (not simulated) data after platform activation
- ✅ Reinvestment triggers correctly at milestones

---

## Post-Implementation

Once user completes account signups using the browser automation:

1. System will automatically track real revenue
2. Reinvestment will trigger at thresholds ($50, $100, $500, $1000)
3. Dashboard will show real-time earnings
4. Scaling happens autonomously per existing logic
