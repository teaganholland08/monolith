# IMPL PLAN: DASHBOARD PHASE 2 - "THE OMEGA UPDATE"

## Goal

Expand `monolith_ui.py` to match the full scope of `PROJECT_MONOLITH_BLUEPRINT.md`. The User feels "a lot is missing" because the dashboard currently focuses only on *Hardware/Tactical* stats, missing the *Strategic* and *Knowledge* layers.

## User Review Required
>
> [!IMPORTANT]
> This update adds significant complexity to the UI, introducing a "Multi-Page" sidebar architecture to house the new modules.

## Proposed Changes

### 1. New Sidebar Navigation

Instead of just "Command Mode" (Mobile vs Desktop), we will add a **Mission Module** selector:

- **COMMAND**: The current Dashboard (Hardware/Tactical).
- **LIBRARY**: Access to `MONOLITH_OPERATOR_MANUAL.md` and `BLUEPRINT` (RAG/Read-Only view).
- **AGENTS**: Utilization of the `auto_monolith.py` agent states (Scout, Writer, Sentinel).
- **TERMINAL**: A "Hacker" style command line interface for manual overrides.

### 2. [NEW] LIBRARY MODULE

- **Function**: Reads and renders the Markdown files (Manual/Blueprint) directly in the UI.
- **Why**: The Commander needs to consult the manual without leaving the HUD.

### 3. [NEW] AGENTS MODULE

- **Function**: Visualizes the 3 Agents from the Blueprint:
  - **Scout**: "Hunting for $..." (Status)
  - **Writer**: "Drafting Viral Copy..." (Status)
  - **Sentinel**: "Scanning Legal..." (Status)
- **Controls**: "DEPLOY", "RECALL", "CHANGE MODE".

### 4. [NEW] SECURE TERMINAL

- **Function**: A text input field that simulates (or executes) shell commands.
- **Commands**: `ping`, `scan`, `deploy_drone`, `wipe_logs`.

## Component: `monolith_ui.py`

#### [MODIFY] `monolith_ui.py`

- Refactor `sidebar` to include `st.selectbox("MODULE", ["COMMAND", "AGENTS", "LIBRARY", "TERMINAL"])`.
- Implement conditional rendering for each Module.
- Add file reading logic for **LIBRARY**.
- Add mock-state logic for **AGENTS** (until fully hooked up).

## Verification Plan

### Manual Verification

- **Click Through**: Test navigation between Command, Agents, and Library.
- **Read Test**: Verify `MONOLITH_OPERATOR_MANUAL.md` renders correctly in Library.
- **Mobile Check**: Ensure new modules don't break the "Shield Mode" responsiveness.
