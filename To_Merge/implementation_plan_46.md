# Project Monolith Setup Plan

## Goal Description

Deploy "Project Monolith: Omega" by creating and executing a PowerShell installer script that sets up the required directory structure, writes python source files for the dashboard and engine, sets environment variables, and installs dependencies.

## User Review Required
>
> [!IMPORTANT]
> The installer script will modify User-level environment variables (`MONOLITH_HOME`, `MONOLITH_STATUS`) and install Python packages globally (or to the active environment). Ensure you are okay with these changes.

## Proposed Changes

### Workspace

#### [NEW] [install_monolith.ps1](file:///C:/Users/Teagan%20Holland/Desktop/Master%20Blueprint/install_monolith.ps1)

- Create a PowerShell script containing the exact setup logic provided by the user.

## Verification Plan

### Automated Verification

- **Execution**: Run the `install_monolith.ps1` script.
- **Checks**:
  - Verify directories exist: `C:\Monolith\System\UI`, etc.
  - Verify files exist: `C:\Monolith\System\UI\monolith_ui.py`, etc.
  - Verify Env Vars: `Get-Item env:\MONOLITH_HOME`
  - Verify Pip Install: Check if `crewai`, `streamlit`, etc. are installed.

### Manual Verification

- The script attempts to launch `streamlit run System\UI\monolith_ui.py`. I will allow this to run or verify manually if it blocks.
