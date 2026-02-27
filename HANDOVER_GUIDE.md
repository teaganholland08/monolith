# Project Monolith v4.5 Handoff Guide

**WELCOME TO PROJECT MONOLITH.**

This package contains the complete, "Immortal" version of the Monolith system. It is designed to be self-hosted, autonomous, and resilient.

## 📦 Package Contents

- **System/**: Core source code for all Agents, Sentinels, and Core logic.
- **Config/**: Configuration files (JSON).
- **Tools**: Batch scripts (`.bat`) and PowerShell scripts (`.ps1`) for easy management.
- **Documentation**: All `.md` files in the root and `Brain/` directory.

## 🚀 Quick Start

### Prerequisites

- **Python 3.10+**: Ensure Python is installed and added to PATH.
- **Git** (Optional, for version control).
- **Docker** (Optional, if you prefer containerized deployment).

### 1. Setup Environment

Open a terminal in the project root:

```bash
# Windows
./monolith_install.ps1

# OR Manual Setup
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Secrets
>
> **⚠️ IMPORTANT**: The `.env` file containing API keys and secrets has been included. **Protect this file.**

- Open `.env` and verify your keys (OpenAI, Brave, etc.).
- Ensure `vault_key.key` is present in the root (required for encryption).

### 3. Launch the System

You have several launch options:

- **Launch Dashboard & Core**:
  Double-click `LAUNCH_UI.bat`

- **Launch "Immortal" Loop (No UI)**:
  Double-click `DEPLOY_IMMORTAL.bat`

- **Emergency Stop**:
  Double-click `PANIC_BUTTON.bat`

## 📂 Key Architecture

- **Monolith Core**: `System/Core/monolith_core.py` - The central brain.
- **Omega Entry**: `monolith_omega.py` - The unified entry point.
- **Sentinels**: `System/Agents/` - Autonomous guardians for Finance, Legal, and Platform risk.

## 🆘 Troubleshooting

- **Missing Dependencies**: Run `pip install -r requirements.txt` again.
- **Permission Errors**: Run terminals/scripts as Administrator.
- **Logs**: Check the `Logs/` directory for detailed runtime information.

*Good luck. The system is ready.*
