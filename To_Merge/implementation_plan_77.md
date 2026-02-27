# Monolith-Core Health Dashboard Implementation Plan

## Goal

Create a local "Health Dashboard" to monitor system resources (Disk & Memory) using Python and Streamlit. This acts as the first module of the "Monolith-Core" workspace.

## Proposed Changes

### Monolith-Core

#### [NEW] [dashboard.py](file:///c:/Users/Teagan Holland/.gemini/antigravity/playground/interstellar-radiation/Monolith-Core/dashboard.py)

- Import `streamlit` and `psutil`.
- Fetch memory usage (RAM) using `psutil.virtual_memory()`.
- Fetch disk usage using `psutil.disk_usage('/')`.
- Display metrics using `st.metric` and `st.progress` or charts.
- Add a "Refresh" button or auto-refresh mechanism if simple.

## Verification Plan

### Automated Verification (Browser Agent)

1. **Launch Server**: Run `streamlit run Monolith-Core/dashboard.py --server.headless true` in the background.
2. **Verify**: Use the browser agent to navigate to `http://localhost:8501`.
3. **Check**:
    - Page title contains "Health Dashboard".
    - "Memory Usage" and "Disk Usage" sections are visible.
    - Values are displayed (not empty).
