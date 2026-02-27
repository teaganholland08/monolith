import os
import zipfile
import datetime
import sys

def zip_project(output_filename):
    """Zips the ENTIRE current directory, NO EXCEPTIONS (except the zip itself)."""
    
    # Only exclude the output file and potentially the script itself to be clean
    EXCLUDE_FILES = {
        output_filename, 'packager.py', '.DS_Store'
    }
    # NO DIRECTORY EXCLUSIONS - USER WANTS EVERYTHING
    
    print(f"Starting COMPLETIONIST backup to {output_filename}...")
    print("Including .git, .venv, node_modules, and all data.")
    
    file_count = 0
    total_size = 0
    
    with zipfile.ZipFile(output_filename, 'w', zipfile.ZIP_DEFLATED, allowZip64=True) as zipf:
        for root, dirs, files in os.walk('.'):
            # Skip the output file if it exists in the tree
            if output_filename in files:
                files.remove(output_filename)
                
            for file in files:
                if file in EXCLUDE_FILES:
                    continue
                    
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, '.')
                
                try:
                    # Get size for stats
                    fsize = os.path.getsize(file_path)
                    total_size += fsize
                    
                    zipf.write(file_path, arcname)
                    file_count += 1
                    
                    # Progress update every 1000 files
                    if file_count % 1000 == 0:
                        size_mb = total_size / (1024 * 1024)
                        print(f"  Processed {file_count} files... ({size_mb:.1f} MB)", end='\r')
                        
                except PermissionError:
                    print(f"\n  [WARN] Permission denied (skipped): {file}")
                except OSError as e:
                    print(f"\n  [WARN] OS Error (skipped): {file} - {e}")
                except Exception as e:
                    print(f"\n  [ERR] Failed to pack {file}: {e}")

    print(f"\nCOMPLETIONIST Package Ready: {output_filename}")
    print(f"Total Files: {file_count}")
    print(f"Total Size: {os.path.getsize(output_filename) / (1024*1024):.2f} MB")

if __name__ == "__main__":
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_zip = f"Monolith_v4.5_Immortal_COMPLETE_{timestamp}.zip"
    zip_project(output_zip)
