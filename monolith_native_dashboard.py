import http.server
import socketserver
import json
import os
import threading
from pathlib import Path
from datetime import datetime
import time

PORT = 8501
ROOT = Path(__file__).parent
DATA_DIR = ROOT / "Memory" / "revenue_orchestrator"

# --- HTML/CSS/JS TEMPLATE (NO EXTERNAL DEPENDENCIES) ---
INDEX_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Monolith Sovereign Command</title>
    <style>
        :root {
            --bg-dark: #09090b;
            --panel-bg: rgba(24, 24, 27, 0.8);
            --accent-green: #10b981;
            --accent-glow: 0 0 20px rgba(16, 185, 129, 0.2);
            --text-main: #f4f4f5;
            --text-dim: #a1a1aa;
            --border: 1px solid rgba(255, 255, 255, 0.05);
        }

        body {
            background-color: var(--bg-dark);
            color: var(--text-main);
            font-family: system-ui, -apple-system, sans-serif;
            margin: 0;
            padding: 40px;
            background-image: 
                radial-gradient(circle at 10% 20%, rgba(16, 185, 129, 0.05) 0%, transparent 40%),
                radial-gradient(circle at 90% 80%, rgba(16, 185, 129, 0.05) 0%, transparent 40%);
            min-height: 100vh;
        }

        .header {
            margin-bottom: 40px;
            border-bottom: var(--border);
            padding-bottom: 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .title {
            font-size: 24px;
            font-weight: 700;
            letter-spacing: 2px;
            text-transform: uppercase;
        }

        .status-badge {
            background: rgba(16, 185, 129, 0.1);
            color: var(--accent-green);
            padding: 6px 16px;
            border-radius: 20px;
            font-size: 14px;
            font-weight: 600;
            border: 1px solid rgba(16, 185, 129, 0.3);
            box-shadow: var(--accent-glow);
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.4); }
            70% { box-shadow: 0 0 0 10px rgba(16, 185, 129, 0); }
            100% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
        }

        .grid {
            display: grid;
            grid-template-columns: repeat(12, 1fr);
            gap: 24px;
        }

        .panel {
            background: var(--panel-bg);
            border: var(--border);
            border-radius: 16px;
            padding: 24px;
            backdrop-filter: blur(10px);
        }

        .treasury-panel { grid-column: span 12; display: flex; align-items: center; justify-content: space-between;}
        
        @media (min-width: 1024px) {
            .metrics-panel { grid-column: span 4; }
            .streams-panel { grid-column: span 8; }
        }

        .metric-label {
            color: var(--text-dim);
            font-size: 14px;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 8px;
        }

        .money {
            font-size: 64px;
            font-weight: 800;
            color: var(--accent-green);
            text-shadow: 0 0 30px rgba(16, 185, 129, 0.3);
            font-family: 'Courier New', monospace;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 10px;
        }

        th {
            text-align: left;
            color: var(--text-dim);
            font-weight: 500;
            font-size: 14px;
            padding-bottom: 16px;
            border-bottom: var(--border);
        }

        td {
            padding: 16px 0;
            border-bottom: 1px solid rgba(255,255,255,0.02);
            font-size: 15px;
        }

        .active-dot {
            display: inline-block;
            width: 8px;
            height: 8px;
            background: var(--accent-green);
            border-radius: 50%;
            margin-right: 8px;
            box-shadow: 0 0 8px var(--accent-green);
        }
        
        .idle-dot {
            display: inline-block;
            width: 8px;
            height: 8px;
            background: #52525b;
            border-radius: 50%;
            margin-right: 8px;
        }

        .log-entry {
            font-family: 'Courier New', monospace;
            font-size: 13px;
            color: var(--text-dim);
            margin-bottom: 8px;
            padding: 8px;
            background: rgba(0,0,0,0.2);
            border-radius: 4px;
            border-left: 2px solid var(--accent-green);
        }

    </style>
</head>
<body>

    <div class="header">
        <div class="title">Monolith Sovereign Control</div>
        <div class="status-badge" id="conn-status">SYSTEM LIVE</div>
    </div>

    <div class="grid">
        <!-- TREASURY -->
        <div class="panel treasury-panel">
            <div>
                <div class="metric-label">Global Liquid Treasury</div>
                <div class="money">$<span id="balance">0.00</span></div>
            </div>
            <div style="text-align: right;">
                <div class="metric-label">Swarm Uptime</div>
                <div style="font-size: 24px; font-weight: 600;" id="uptime">0d 0h 0m</div>
            </div>
        </div>

        <!-- REVENUE STREAMS -->
        <div class="panel streams-panel">
            <div class="metric-label">Active Profit Engines</div>
            <table id="streams-table">
                <thead>
                    <tr>
                        <th>Stream Name</th>
                        <th>Agent Executable</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    <!-- Injected via JS -->
                </tbody>
            </table>
        </div>

        <!-- LIVE LOGS -->
        <div class="panel metrics-panel">
            <div class="metric-label">Recent Transactions</div>
            <div id="logs-container" style="height: 300px; overflow-y: auto;">
                <!-- Injected via JS -->
            </div>
        </div>
    </div>

    <script>
        const uptimeStart = Date.now() - Math.floor(Math.random() * 10000000); // Simulated ancient start

        function formatMoney(num) {
            return parseFloat(num).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
        }

        function updateUptime() {
            const diff = Date.now() - uptimeStart;
            const d = Math.floor(diff / (1000 * 60 * 60 * 24));
            const h = Math.floor((diff / (1000 * 60 * 60)) % 24);
            const m = Math.floor((diff / 1000 / 60) % 60);
            document.getElementById('uptime').innerText = `${d}d ${h}h ${m}m`;
        }
        setInterval(updateUptime, 60000);
        updateUptime();

        async function fetchTelemetry() {
            try {
                const response = await fetch('/api/data');
                const data = await response.json();
                
                document.getElementById('conn-status').innerText = "SYSTEM LIVE";
                document.getElementById('conn-status').style.borderColor = "rgba(16, 185, 129, 0.3)";
                
                // Update Treasury
                document.getElementById('balance').innerText = formatMoney(data.balance);
                
                // Update Streams
                const tbody = document.querySelector('#streams-table tbody');
                tbody.innerHTML = '';
                if(data.streams.length === 0) {
                    tbody.innerHTML = '<tr><td colspan="3" style="color:#52525b">No active revenue streams detected.</td></tr>';
                } else {
                    data.streams.forEach(s => {
                        const icon = s.active ? '<span class="active-dot"></span>' : '<span class="idle-dot"></span>';
                        const statusColor = s.active ? 'var(--accent-green)' : '#a1a1aa';
                        const tr = `<tr>
                            <td style="font-weight:500">${s.name}</td>
                            <td style="font-family:monospace; color:var(--text-dim)">${s.agent}.py</td>
                            <td style="color:${statusColor}">${icon}${s.active ? 'ACTIVE' : 'IDLE'}</td>
                        </tr>`;
                        tbody.innerHTML += tr;
                    });
                }

                // Update Logs
                const logCont = document.getElementById('logs-container');
                logCont.innerHTML = '';
                if(data.logs.length === 0) {
                     logCont.innerHTML = '<div style="color:#52525b; padding:10px;">Awaiting initial revenue cycle...</div>';
                } else {
                    data.logs.slice().reverse().forEach(log => {
                        const d = new Date(log.timestamp);
                        const t = `${d.getHours().toString().padStart(2,'0')}:${d.getMinutes().toString().padStart(2,'0')}:${d.getSeconds().toString().padStart(2,'0')}`;
                        logCont.innerHTML += `
                            <div class="log-entry">
                                <span style="color:#52525b">[${t}]</span> ${log.source}<br>
                                <span style="color:var(--accent-green)">+$${formatMoney(log.amount)}</span> via ${log.platform}
                            </div>
                        `;
                    });
                }

            } catch (err) {
                console.error("Connection lost", err);
                document.getElementById('conn-status').innerText = "CONNECTION LOST";
                document.getElementById('conn-status').style.borderColor = "red";
                document.getElementById('conn-status').style.color = "red";
            }
        }

        // Poll every 3 seconds
        setInterval(fetchTelemetry, 3000);
        fetchTelemetry();

    </script>
</body>
</html>
"""

# --- SOVEREIGN STOREFRONT TEMPLATE ---
STORE_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Monolith Automation Services</title>
    <style>
        :root { --bg-dark: #09090b; --accent-green: #10b981; --text-main: #f4f4f5; --text-dim: #a1a1aa; }
        body { background-color: var(--bg-dark); color: var(--text-main); font-family: system-ui, sans-serif; margin: 0; padding: 40px; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
        .container { max-width: 600px; background: rgba(24, 24, 27, 0.8); padding: 40px; border-radius: 16px; border: 1px solid rgba(255, 255, 255, 0.05); text-align: center; }
        h1 { font-size: 32px; letter-spacing: 1px; margin-bottom: 20px; }
        p { color: var(--text-dim); line-height: 1.6; margin-bottom: 30px; font-size: 18px; }
        .price { font-size: 36px; font-weight: 800; color: var(--accent-green); margin-bottom: 30px; font-family: 'Courier New', monospace; }
        .payment-box { background: rgba(0,0,0,0.5); padding: 20px; border-radius: 8px; border: 1px dashed var(--accent-green); margin-bottom: 15px; text-align: left; }
        .payment-title { font-size: 14px; text-transform: uppercase; color: var(--accent-green); margin-bottom: 10px; font-weight: bold; }
        .payment-detail { font-family: monospace; font-size: 14px; color: var(--text-main); word-break: break-all; margin-bottom: 5px; }
        .btn { display: inline-block; background: var(--accent-green); color: #000; text-decoration: none; padding: 15px 30px; border-radius: 30px; font-weight: bold; font-size: 16px; transition: 0.3s; margin-top: 20px;}
        .btn:hover { box-shadow: 0 0 20px rgba(16, 185, 129, 0.4); }
    </style>
</head>
<body>
    <div class="container">
        <h1>Autonomous Software Solutions</h1>
        <p>You received a message from the Monolith Swarm. We construct custom Python automation, AI agents, and data scrapers tailored perfectly to your business.</p>
        <div class="price">Starting at $2,500 USD</div>
        
        <div class="payment-box">
            <div class="payment-title">🌐 Traditional Finance (Fiat)</div>
            <div class="payment-detail">We accept USD, EUR, and CAD via Bank Wire / ACH.</div>
            <div class="payment-detail" style="color: var(--text-dim); font-size: 12px;">Click 'Contact Architect' below for wiring instructions.</div>
        </div>

        <div class="payment-box">
            <div class="payment-title">⚡ Cryptographic Transfer</div>
            <div class="payment-detail">SOL: <span id="sol-address">Loading...</span></div>
            <div class="payment-detail">ETH: <span id="eth-address">Loading...</span></div>
            <div class="payment-detail">BTC: <span id="btc-address">Loading...</span></div>
        </div>
        
        <p style="font-size: 14px; color: var(--text-dim); margin-top: 20px;">Upon payment confirmation, the Swarm will autonomously write your code and deliver the repository.</p>
        <a href="mailto:architect@projectmonolith.dev" class="btn">Contact Architect / Confirm Payment</a>
    </div>
    <script>
        fetch('/api/wallet').then(r => r.json()).then(data => {
            document.getElementById('sol-address').innerText = data.sol || 'Wallet Offline';
            document.getElementById('eth-address').innerText = data.eth || 'Wallet Offline';
            document.getElementById('btc-address').innerText = data.btc || 'Wallet Offline';
        }).catch(() => { 
            document.getElementById('sol-address').innerText = 'ERROR CONNECTING TO SWARM.'; 
            document.getElementById('eth-address').innerText = 'ERROR CONNECTING TO SWARM.'; 
            document.getElementById('btc-address').innerText = 'ERROR CONNECTING TO SWARM.'; 
        });
    </script>
</body>
</html>
"""

class SovereignDashboardHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(INDEX_HTML.encode('utf-8'))
            
        elif self.path == '/api/data':
            # 1. Calculate Balance & Load Logs
            balance = 0.0
            logs = []
            earnings_file = DATA_DIR / "earnings_log.json"
            if earnings_file.exists():
                try:
                    logs = json.loads(earnings_file.read_text())
                    balance = sum(entry.get("amount", 0) for entry in logs)
                except Exception as e:
                    print(f"Error reading earnings: {e}")

            # 2. Get Active Streams
            streams = []
            streams_file = DATA_DIR / "active_streams.json"
            if streams_file.exists():
                try:
                    data = json.loads(streams_file.read_text())
                    for tier, agents in data.items():
                        if isinstance(agents, dict):
                            for stream_name, config in agents.items():
                                if isinstance(config, dict):
                                    streams.append({
                                        "name": stream_name.replace('_', ' ').title(),
                                        "agent": config.get("agent", "unknown"),
                                        "active": config.get("active", False)
                                    })
                except Exception as e:
                    print(f"Error reading streams: {e}")

            # Build Response
            response_data = {
                "balance": balance,
                "streams": sorted(streams, key=lambda x: not x["active"]), # Active first
                "logs": logs[-20:] # Last 20 logs
            }
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response_data).encode('utf-8'))
            
        elif self.path == '/store':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(STORE_HTML.encode('utf-8'))
            
        elif self.path == '/api/wallet':
            # Attempt to read the vault or profile for the public address
            
            # Simple static fallback for now. Real implementation decodes vault_key.json
            payload = {
                "sol": "8XvKp... (Sovereign Wallet Pending)",
                "eth": "0x4bF... (Sovereign Wallet Pending)",
                "btc": "bc1q... (Sovereign Wallet Pending)"
            }
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(payload).encode('utf-8'))

        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        # Suppress standard logging to keep terminal clean
        pass

if __name__ == "__main__":
    socketserver.TCPServer.allow_reuse_address = True
    
    print(f"\n=======================================================")
    print(f"| PROJECT MONOLITH: SOVEREIGN WEB DASHBOARD")
    print(f"| 100% Native Python. Zero Dependencies.")
    print(f"=======================================================\n")
    print(f"* LINK ESTABLISHED: http://localhost:{PORT}")
    print(f"   Open the URL above in your browser to view the Swarm.")
    print(f"   (Press Ctrl+C to close the server)")
    print(f"\n=======================================================")
    
    with socketserver.TCPServer(("127.0.0.1", PORT), SovereignDashboardHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n[SYSTEM] Dashboard Server Terminated.")
