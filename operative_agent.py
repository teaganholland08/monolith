from bs4 import BeautifulSoup
import urllib.request
import os
import time

class OperativeAgent:
    def __init__(self):
        self.sandbox = "./data/operative/"
        os.makedirs(self.sandbox, exist_ok=True)

    def scrape_marketplace(self):
        print("[Operative] The Hunter is scraping marketplace data...")
        try:
            # Example marketplace URL lookup using native urllib
            url = "https://example.com"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            
            with urllib.request.urlopen(req) as response:
                html = response.read()
                soup = BeautifulSoup(html, 'html.parser')
                
                # Extract some marketplace data
                title = soup.title.string if soup.title else "No Title"
                print(f"[Operative] Mined target data: {title}")
                
                hunt_file = os.path.join(self.sandbox, "latest_hunt.txt")
                with open(hunt_file, "w", encoding="utf-8") as f:
                    f.write(title)
        except Exception as e:
            print(f"[Operative] Marketplace scraping failed: {e}")

    def run(self):
        while True:
            self.scrape_marketplace()
            time.sleep(600)  # Hunt every 10 minutes

if __name__ == "__main__":
    operative = OperativeAgent()
    operative.run()
