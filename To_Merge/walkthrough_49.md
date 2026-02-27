# Monolith-Core Health Dashboard Walkthrough

I have successfully built and verified the **Health Dashboard** for monitoring local disk and memory usage.

## What's Included

1. **[dashboard.py](file:///c:/Users/Teagan Holland/.gemini/antigravity/playground/interstellar-radiation/Monolith-Core/dashboard.py)**: The core Streamlit application.
2. **[launcher.py](file:///c:/Users/Teagan Holland/.gemini/antigravity/playground/interstellar-radiation/Monolith-Core/launcher.py)**: A helper script to launch the server reliably in your environment.

## How to Run

Because `streamlit` command was tricky to execute due to PATH issues, use the launcher:

```powershell
python "Monolith-Core/launcher.py"
```

The dashboard will be available at `http://localhost:8501`.

## Verification Results

- **Automated Check**: Verified via `curl -I http://localhost:8501` to ensure the server response is **200 OK**.
- **Visuals**: The dashboard displays "Memory Usage" and "Disk Usage (C:)" including progress bars and GB metrics.

## Troubleshooting

I encountered environment issues where `streamlit` was installed but not on the system PATH.

- **Solution**: I created `launcher.py` to import `streamlit.web.cli` directly, bypassing the broken executable path. This ensures reliability.
