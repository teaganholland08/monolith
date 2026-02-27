"""
NUCLEI INSTALLER - Project Monolith
Automatically downloads and installs the latest Nuclei binary for Windows.
"""
import os
import shutil
import zipfile
import requests
import sys
from pathlib import Path

def install_nuclei():
    print("☢️  INITIATING NUCLEI INSTALLATION...")
    
    url = "https://github.com/projectdiscovery/nuclei/releases/download/v3.2.0/nuclei_3.2.0_windows_amd64.zip"
    dest_zip = "nuclei.zip"
    
    # 1. Download
    print(f"⬇️  Downloading from {url}...")
    try:
        resp = requests.get(url, stream=True)
        resp.raise_for_status()
        with open(dest_zip, 'wb') as f:
            for chunk in resp.iter_content(chunk_size=8192):
                f.write(chunk)
        print("✅ Download Complete.")
    except Exception as e:
        print(f"❌ Download Failed: {e}")
        return

    # 2. Extract
    print("📦 Extracting...")
    try:
        with zipfile.ZipFile(dest_zip, 'r') as zip_ref:
            zip_ref.extractall(".")
        print("✅ Extraction Complete.")
    except Exception as e:
        print(f"❌ Extraction Failed: {e}")
        return

    # 3. Cleanup & Verify
    if os.path.exists(dest_zip):
        os.remove(dest_zip)
        
    if os.path.exists("nuclei.exe"):
        print("✅ nuclei.exe verified present.")
        
        # Add to local user path if possible, or just keep it here
        # We will move it to System/Tools if possible, or keep in root for now as per `FIX_REVENUE_BLOCKERS.bat` check
        target_dir = Path("System/Tools/Nuclei")
        target_dir.mkdir(parents=True, exist_ok=True)
        
        shutil.move("nuclei.exe", target_dir / "nuclei.exe")
        print(f"📍 Moved to {target_dir}")
        
        # Add to PATH (Temporary for session, Permanent needs registry)
        os.environ["PATH"] += os.pathsep + str(target_dir.resolve())
        print(f"👉 Added {target_dir} to current PATH.")
        
        # Verify
        os.system(f"{target_dir / 'nuclei.exe'} -version")
        
    else:
        print("❌ Error: nuclei.exe not found after extraction.")

if __name__ == "__main__":
    install_nuclei()
