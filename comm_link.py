import urllib.request
import urllib.parse
import json
import time
import os
import sys

class CommLink:
    def __init__(self):
        self.sandbox = "./data/comm/"
        os.makedirs(self.sandbox, exist_ok=True)
        # Using environment vars or placeholders
        self.token = os.environ.get("TELEGRAM_BOT_TOKEN", "LOCAL_TEST_TOKEN")
        self.chat_id = os.environ.get("TELEGRAM_CHAT_ID", "LOCAL_CHAT_ID")
        self.api_url = f"https://api.telegram.org/bot{self.token}"
        self.last_update_id = 0

    def send_notification(self, message):
        print(f"[CommLink] Sending notification via POST: {message}")
        try:
            url = f"{self.api_url}/sendMessage"
            payload = {'chat_id': self.chat_id, 'text': message}
            data = urllib.parse.urlencode(payload).encode('utf-8')
            
            # Using urllib.request for posting without external libraries
            req = urllib.request.Request(url, data=data)
            with urllib.request.urlopen(req) as response:
                return response.read()
        except Exception as e:
            print(f"[CommLink] Failed to dispatch via Telegram API: {e}")

    def listen_for_commands(self):
        try:
            url = f"{self.api_url}/getUpdates?offset={self.last_update_id + 1}&timeout=30"
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode('utf-8'))
                for update in result.get('result', []):
                    self.last_update_id = update['update_id']
                    message_text = update.get('message', {}).get('text', '')
                    
                    if message_text == '/kill':
                        print("[CommLink] CRITICAL: Received /kill command. Terminating Local Swarm.")
                        self.send_notification("Swarm process termination confirmed.")
                        sys.exit(0)
        except Exception as e:
             # Typically times out or fails auth if using dummy tokens, ignore gracefully
            pass

    def run(self):
        print("[CommLink] Comm-Link Active. Polling Telegram API...")
        while True:
            self.listen_for_commands()
            time.sleep(5)

if __name__ == "__main__":
    comm = CommLink()
    comm.run()
