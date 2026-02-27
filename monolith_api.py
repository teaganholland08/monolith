"""
MONOLITH API - The Nervous System v5.0
FastAPI Backend for the Decoupled Dashboard.
"""
import glob
import json
import logging
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI(title="Project Monolith Alpha-Zero")

# Fix CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Paths
ROOT = Path(__file__).parent
SENTINELS_DIR = ROOT / "System" / "Sentinels"
LOGS_DIR = ROOT / "Logs"

@app.get("/status")
def get_system_status():
    """Aggregates all Sentinel done-files."""
    status = {"global": "ONLINE", "agents": {}}
    
    files = glob.glob(str(SENTINELS_DIR / "*.done"))
    for fpath in files:
        try:
            with open(fpath, 'r') as f:
                data = json.load(f)
                status["agents"][data.get("agent", Path(fpath).stem)] = data
        except:
            pass
    return status

@app.get("/revenue")
def get_revenue_streams():
    """Mock aggregate of revenue (until DB is live)."""
    # In production, query SQLite or Ledger
    return {
        "total_revenue_usd": 0.00,
        "streams": [
            {"source": "Content Agency", "val": 0.00, "status": "Active"},
            {"source": "Cloud Arbitrage", "val": 0.00, "status": "Scanning"},
            {"source": "Bounty Swarm", "val": 0.00, "status": "Hunting"}
        ]
    }

@app.get("/logs")
def get_recent_logs():
    """Returns tail of operations log."""
    log_file = LOGS_DIR / "agent_telemetry.json"
    if log_file.exists():
        try:
            with open(log_file, 'r') as f:
                return json.load(f)[-50:]
        except:
            return []
    return []

@app.get("/")
def serve_dashboard():
    return FileResponse(ROOT / "UI" / "dashboard_modern.html")

# Serve UI static files if needed
app.mount("/ui", StaticFiles(directory=ROOT / "UI"), name="ui")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
