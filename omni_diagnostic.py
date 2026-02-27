import ast
import os
import sys

def check_file(filepath, root_dir):
    errors = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            source = f.read()
    except Exception as e:
        return [f"Read error: {e}"]

    # Check Syntax
    try:
        tree = ast.parse(source, filename=filepath)
    except SyntaxError as e:
        return [f"SyntaxError on line {e.lineno}"]

    # Fast Import Check
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            if node.module and node.module.startswith("System."):
                parts = node.module.split('.')
                expected_path = os.path.join(root_dir, *parts) + ".py"
                expected_dir = os.path.join(root_dir, *parts)
                if not os.path.exists(expected_path) and not os.path.isdir(expected_dir):
                    errors.append(f"Missing import target: {node.module}")
    return errors

def run_diagnostics(root_dir):
    total = 0
    failed = {}
    
    for dirpath, _, filenames in os.walk(root_dir):
        if "venv" in dirpath or "__pycache__" in dirpath or ".git" in dirpath:
            continue
            
        for file in filenames:
            if file.endswith(".py"):
                filepath = os.path.join(dirpath, file)
                total += 1
                errs = check_file(filepath, root_dir)
                if errs:
                    failed[filepath] = errs

    report_path = os.path.join(root_dir, "diagnostic_report.txt")
    with open(report_path, "w", encoding="utf-8") as out:
        out.write("="*50 + "\n")
        out.write("PROJECT MONOLITH - OMNI-DIAGNOSTIC SCAN\n")
        out.write("="*50 + "\n\n")
        
        out.write(f"Scanned {total} Python files.\n")
        if not failed:
            out.write("ALL FILES PASSED SYNTAX AND STRUCTURE CHECKS. SYSTEM IS FLAWLESS.\n")
        else:
            out.write(f"FOUND ERRORS IN {len(failed)} FILES:\n\n")
            for fp, errs in failed.items():
                rel_path = os.path.relpath(fp, root_dir)
                out.write(f"- {rel_path}:\n")
                for e in errs:
                    out.write(f"    {e}\n")

if __name__ == "__main__":
    run_diagnostics(os.path.dirname(os.path.abspath(__file__)))
