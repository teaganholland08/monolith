import http.server
import socketserver
import json
import random
import os

PORT = 8000

class TelemetryHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Add CORS headers if needed
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

    def do_GET(self):
        if self.path == '/telemetry':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            
            # Read real telemetry
            telemetry_file = "./agent_telemetry.json"
            active_agents = 0
            revenue = 0.0
            
            lines = []
            if os.path.exists(telemetry_file):
                try:
                    with open(telemetry_file, 'r') as f:
                        lines = f.readlines()
                        if lines:
                            latest = json.loads(lines[-1].strip())
                            active_agents = len(set([json.loads(line).get('agent') for line in lines[-50:] if line.strip()]))
                            revenue = latest.get('earnings', 0.0)
                except Exception:
                    pass

            data = {
                "system_status": "ONLINE" if active_agents > 0 else "IDLE",
                "active_agents": active_agents,
                "revenue_generated": revenue,
                "current_wattage": round(random.uniform(800.0, 1350.0), 2),
                "tasks_completed": len(lines) if os.path.exists(telemetry_file) else 0
            }
            body = json.dumps(data).encode('utf-8')
            self.send_header('Content-Length', len(body))
            self.end_headers()
            try:
                self.wfile.write(body)
            except ConnectionAbortedError:
                pass
            
        elif self.path == '/kill_switch':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            
            print("KILL SWITCH ENGAGED VIA DASHBOARD.")
            with open("KILL_SIGNAL", "w") as f:
                f.write("SHUTDOWN")
                
            body = json.dumps({"status": "Swarm Terminated"}).encode('utf-8')
            self.send_header('Content-Length', len(body))
            self.end_headers()
            try:
                self.wfile.write(body)
            except ConnectionAbortedError:
                pass
            
        elif self.path == '/bank_status':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            
            # Read real balance from telemetry
            telemetry_file = "./agent_telemetry.json"
            balance = 0.0
            
            if os.path.exists(telemetry_file):
                try:
                    with open(telemetry_file, 'r') as f:
                        lines = f.readlines()
                        if lines:
                            latest = json.loads(lines[-1].strip())
                            balance = latest.get('earnings', 0.0)
                except Exception:
                    pass

            body = f"<html><body><h1>Bank Portal</h1><p>Balance: ${balance}</p></body></html>".encode('utf-8')
            self.send_header('Content-Length', len(body))
            self.end_headers()
            try:
                self.wfile.write(body)
            except ConnectionAbortedError:
                pass # The API client correctly disconnected before we could flush the socket
            
        elif self.path == '/opportunities':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            
            # Simulated API Response
            data = {"status": "success", "data": "profitable_operation_data", "roi": random.uniform(1.1, 3.5)}
            body = json.dumps(data).encode('utf-8')
            self.send_header('Content-Length', len(body))
            self.end_headers()
            try:
                self.wfile.write(body)
            except ConnectionAbortedError:
                pass
            
        else:
            # Serve files (like index.html)
            super().do_GET()

def start_server():
    print(f"Starship Command Deck booting -> http://localhost:{PORT}")
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), TelemetryHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("Shutting down Dashboard.")

if __name__ == "__main__":
    start_server()
