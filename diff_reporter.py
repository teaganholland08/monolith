import os
import difflib

# We only care about reviewing the .py logic files for "best" code.
# The .md and .json files are just logs/telemetry duplicates.

target_bases = [
    "agent_factory.py", 
    "dashboard_server.py", 
    "hydra.py", 
    "launcher.py", 
    "monolith_core.py", 
    "monolith_ui.py", 
    "sentinel_agent.py",
    "dashboard.py"
]

to_merge_dir = "To_Merge"
files = [f for f in os.listdir(to_merge_dir) if f.endswith(".py")]

with open("diff_report.txt", "w", encoding="utf-8") as out:
    for f in files:
        base_name = None
        for b in target_bases:
            # f might be agent_factory_1.py, dashboard_server_3.py etc.
            name_no_ext = b.replace(".py", "")
            if f.startswith(name_no_ext + "_"):
                base_name = b
                break
                
        if not base_name or not os.path.exists(base_name):
            out.write(f"\n--- Could not find base for {f} ---\n")
            continue
            
        out.write(f"\n{'='*50}\nDIFF: {base_name} VS {f}\n{'='*50}\n")
        
        with open(base_name, "r", encoding="utf-8") as bfile, open(os.path.join(to_merge_dir, f), "r", encoding="utf-8") as mfile:
            blines = bfile.readlines()
            mlines = mfile.readlines()
            
            diff = difflib.unified_diff(blines, mlines, fromfile=base_name, tofile=f, n=1)
            for line in diff:
                out.write(line)
        
print("Wrote diffs to diff_report.txt")
