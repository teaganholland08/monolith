import os
import shutil
from datetime import datetime

# Fingerprints for Project Monolith
search_terms = ['monolith', 'autonomous ai', 'openai', 'api_key', 'llm', 'chatbot', 'gemini'] 
extensions = ['.py', '.js', '.ts', '.cpp', '.hpp', '.c', '.h', '.cs', '.java', '.txt', '.md', '.json']

desktop = os.path.join(os.path.expanduser("~"), "Desktop")
master_folder = os.path.join(desktop, "MONOLITH_COMMAND_CENTER")

if not os.path.exists(master_folder):
    os.makedirs(master_folder)

print(f"[{datetime.now()}] Command Center: Starting System-Wide Sweep...")

for root, dirs, files in os.walk(os.path.expanduser("~")):
    if any(skip in root for skip in ['AppData', 'node_modules', '.git', 'venv', 'MONOLITH_COMMAND_CENTER']):
        continue
        
    for file in files:
        if any(file.lower().endswith(ext) for ext in extensions):
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    if any(term.lower() in f.read().lower() for term in search_terms):
                        # Close and move
                        new_path = os.path.join(master_folder, file)
                        counter = 1
                        while os.path.exists(new_path):
                            name, ext = os.path.splitext(file)
                            new_path = os.path.join(master_folder, f"{name}_{counter}{ext}")
                            counter += 1
                        shutil.move(file_path, new_path)
                        print(f"Captured: {file}")
            except:
                pass

print(f"[{datetime.now()}] Sweep Complete. All project files secured in COMMAND_CENTER.")