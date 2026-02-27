import os
import re
import filecmp
from collections import defaultdict
import shutil

# This script groups all duplicate-named files (e.g., agent_1.py, agent_2.py)
# and compares their content to the base file (e.g., agent.py).
# If the numbered file is an exact duplicate, it is safely deleted. 
# If it has unique content, it is moved to a 'To_Merge' folder for review.

def run_dedup():
    print("Initializing Deduplication Protocol...")
    
    # Regex to match files ending in _[number].[ext]
    pattern = re.compile(r'^(.*)_(\d+)\.(py|md|json|txt|pyc)$')
    
    grouped_files = defaultdict(list)
    
    # Group the duplicate files by their base name
    for root, _, files in os.walk('.'):
        for f in files:
            if "To_Merge" in root or ".git" in root:
                continue
                
            match = pattern.match(f)
            if match:
                base_name = f"{match.group(1)}.{match.group(3)}"
                base_path = os.path.join(root, base_name)
                dup_path = os.path.join(root, f)
                grouped_files[base_path].append(dup_path)

    to_merge_dir = os.path.join(os.getcwd(), "To_Merge")
    os.makedirs(to_merge_dir, exist_ok=True)
    
    deleted = 0
    saved_for_merge = 0

    print(f"Found {len(grouped_files)} base file groups with duplicates.")

    for base_path, dups in grouped_files.items():
        if not os.path.exists(base_path):
            print(f"[WARNING] Base file missing for {base_path}. Keeping duplicates.")
            continue
            
        for dup in dups:
            # If the duplicate is an exact byte-for-byte copy of the base
            if filecmp.cmp(base_path, dup, shallow=False):
                try:
                    os.remove(dup)
                    deleted += 1
                except Exception as e:
                    print(f"Failed to delete {dup}: {e}")
            else:
                # The file is different from the base. Save it for merging.
                # E.g. To_Merge/agent_base_1.py
                try:
                    safe_name = dup.replace(".\\", "").replace("\\", "_")
                    dest = os.path.join(to_merge_dir, safe_name)
                    shutil.move(dup, dest)
                    saved_for_merge += 1
                except Exception as e:
                    print(f"Failed to move {dup}: {e}")
                    
    print("\n--- Deduplication Complete ---")
    print(f"Exact duplicates deleted: {deleted}")
    print(f"Files saved with unique differences to 'To_Merge': {saved_for_merge}")

if __name__ == "__main__":
    run_dedup()
