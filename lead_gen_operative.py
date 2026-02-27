import urllib.request
import json
import time
import os
from pathlib import Path

class LeadGenerationAgent:
    def __init__(self):
        self.root = Path(__file__).parent.parent
        self.assets_dir = self.root / "Data" / "Leads"
        self.assets_dir.mkdir(parents=True, exist_ok=True)
        self.leads_file = self.assets_dir / "hot_leads.txt"
        
        # Subreddits where business owners ask for tech/automation help
        self.subreddits = ["Entrepreneur", "smallbusiness", "SaaS", "startups"]
        self.keywords = ["automate", "automation", "ai", "developer", "hire", "need help", "software", "bottleneck"]
        self.ollama_url = "http://127.0.0.1:11434/api/generate"
        self.model = "qwen2.5:0.5b" # Defaulting to the model the user pulled

    def fetch_reddit_posts(self, subreddit):
        url = f"https://www.reddit.com/r/{subreddit}/new/.json?limit=25"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) MonolithAgent/1.0'}
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode('utf-8'))
                return data['data']['children']
        except Exception as e:
            print(f"[!] Error fetching r/{subreddit}: {e}")
            return []

    def draft_pitch(self, title, description):
        prompt = (
            f"You are an expert AI automation consultant. A business owner posted this on Reddit:\n"
            f"Title: {title}\n"
            f"Description: {description}\n\n"
            f"Write a short, powerful, 3-sentence direct message to send them. "
            f"Pitch that you can solve their problem using custom AI agents or automation. "
            f"End with a low-friction call to action asking if they have 5 minutes to chat. "
            f"Do not include placeholders, make it sound human and professional."
        )
        
        data = {"model": self.model, "prompt": prompt, "stream": False}
        try:
            req = urllib.request.Request(self.ollama_url, data=json.dumps(data).encode('utf-8'), headers={'Content-Type': 'application/json'})
            with urllib.request.urlopen(req, timeout=30) as response:
                result = json.loads(response.read().decode('utf-8'))
                return result.get("response", "").strip()
        except:
            return "Hi there, I saw your post and I build custom AI automation systems that solve exactly this. Do you have 5 minutes to chat about how we can implement this for your business?"

    def scan_for_leads(self):
        print(f"\n[LEAD GEN] 🕵️‍♂️ Initiating Subreddit Scan for High-Ticket Consulting Leads...")
        print("-" * 60)
        
        found_leads = 0
        with open(self.leads_file, "a", encoding="utf-8") as f:
            for sub in self.subreddits:
                print(f"[*] Scanning r/{sub}...")
                posts = self.fetch_reddit_posts(sub)
                
                for post in posts:
                    post_data = post['data']
                    title = post_data.get('title', '')
                    selftext = post_data.get('selftext', '')
                    author = post_data.get('author', '')
                    permalink = post_data.get('permalink', '')
                    
                    # Combine title and text to check for keywords
                    full_text = (title + " " + selftext).lower()
                    
                    if any(kw in full_text for kw in self.keywords) and len(selftext) > 50:
                        print(f"    [+] HOT LEAD FOUND: u/{author} | Topic: {title[:40]}...")
                        
                        pitch = self.draft_pitch(title, selftext)
                        
                        report = (
                            f"LEAD: u/{author}\n"
                            f"URL: https://reddit.com{permalink}\n"
                            f"TOPIC: {title}\n"
                            f"PITCH TO SEND:\n{pitch}\n"
                            f"{'-'*40}\n"
                        )
                        f.write(report)
                        found_leads += 1
                        print(f"    [📝] AI Pitch drafted and saved.")
                        
                time.sleep(2) # Be polite to Reddit API
                
        print("-" * 60)
        print(f"[+] Scan Complete. {found_leads} high-ticket leads identified and pitched.")
        print(f"[+] Leads saved to: {self.leads_file}")
        
if __name__ == "__main__":
    agent = LeadGenerationAgent()
    agent.scan_for_leads()
