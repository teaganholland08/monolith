# Health Dashboard Implementation Plan

Create a Python-based Health Dashboard in the `Monolith-Core` workspace to monitor local disk and memory usage.

## Proposed Changes

### Dashboard Component

#### [NEW] [dashboard.py](file:///C:/Users/Teagan%20Holland/.gemini/antigravity/scratch/Monolith-Core/dashboard.py)

A Streamlit application that:

- Uses `psutil` to fetch memory and disk statistics.
- Displays metrics in real-time or on refresh.
- Uses charts (e.g., bar charts or pie charts) to visualize usage.

#### [NEW] [requirements.txt](file:///C:/Users/Teagan%20Holland/.gemini/antigravity/scratch/Monolith-Core/requirements.txt)

Dependencies:

- `streamlit`
- `psutil`
- `pandas` (for data handling)

## Verification Plan

### Automated Tests

- Run `streamlit run dashboard.py` and verify the process starts.

### Manual Verification

- Use the browser agent to navigate to the Streamlit local URL (typically `http://localhost:8501`).
- Confirm that Disk Usage and Memory stats are displayed and match realistic system values.
