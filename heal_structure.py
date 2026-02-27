import os
import ast
import shutil

def get_missing_imports(filepath):
    missing = set()
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            source = f.read()
            tree = ast.parse(source, filename=filepath)
            for node in ast.walk(tree):
                if isinstance(node, ast.ImportFrom):
                    if node.module and node.module.startswith("System."):
                        missing.add(node.module)
    except Exception as e:
        pass
    return missing

def heal_directory(root_dir):
    print("Initializing Structural Heal Protocol...")
    
    # 1. Collect all expected paths from AST of ALL files
    expected_modules = set()
    for dirpath, _, filenames in os.walk(root_dir):
        if "venv" in dirpath or "__pycache__" in dirpath or ".git" in dirpath:
            continue
        for file in filenames:
            if file.endswith(".py"):
                filepath = os.path.join(dirpath, file)
                expected_modules.update(get_missing_imports(filepath))
                
    # 2. For each expected module (e.g. System.Core.monolith_core)
    # find monolithic_core.py in the root and move it there.
    for module in expected_modules:
        parts = module.split('.')
        filename = parts[-1] + ".py"
        source_path = os.path.join(root_dir, filename)
        
        target_dir = os.path.join(root_dir, *parts[:-1])
        target_path = os.path.join(target_dir, filename)
        
        if os.path.exists(source_path) and not os.path.exists(target_path):
            print(f"Healing: Moving {filename} -> {target_path}")
            os.makedirs(target_dir, exist_ok=True)
            shutil.move(source_path, target_path)

if __name__ == "__main__":
    heal_directory(os.path.dirname(os.path.abspath(__file__)))
