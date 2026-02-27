import os
import base64

def package_everything_to_text(output_filename):
    """
    Reads EVERY file in the directory.
    - Text files are written as-is.
    - Binary files are Base64 encoded.
    - Includes .git, .venv, etc.
    """
    
    # Files to exclude (only the output file itself)
    EXCLUDE_FILES = {
        output_filename, 'packager.py', 'text_packager.py', '.DS_Store'
    }

    print(f"Creating COMPLETE Text Backup: {output_filename}...")
    print("WARNING: This file will be extremely large.")
    
    file_count = 0
    total_size = 0
    
    with open(output_filename, 'w', encoding='utf-8') as outfile:
        # Write Header
        outfile.write(f"# PROJECT MONOLITH COMPLETE DUMP\n")
        outfile.write(f"# CONTAINS EVERY LAST THING\n")
        outfile.write(f"# FORMAT: Text is plain, Binary is Base64 encoded with prefix 'BASE64:'\n")
        outfile.write(f"# ==========================================\n\n")

        for root, dirs, files in os.walk('.'):
            # No directory exclusions - USER WANTS EVERYTHING
            if output_filename in files:
                files.remove(output_filename)

            for file in files:
                if file in EXCLUDE_FILES:
                    continue
                
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, '.')
                
                try:
                    # Try reading as text first
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            is_binary = False
                    except UnicodeDecodeError:
                        # Fallback to binary/base64
                        with open(file_path, 'rb') as f:
                            content = base64.b64encode(f.read()).decode('ascii')
                            is_binary = True
                    
                    # Write Entry
                    outfile.write(f"\n# ==========================================\n")
                    outfile.write(f"# FILE: {rel_path}\n")
                    outfile.write(f"# TYPE: {'BINARY/BASE64' if is_binary else 'TEXT'}\n")
                    outfile.write(f"# ==========================================\n")
                    
                    if is_binary:
                        outfile.write("BASE64:\n")
                        outfile.write(content)
                    else:
                        outfile.write(content)
                    
                    outfile.write(f"\n# END FILE: {rel_path}\n")
                    
                    file_count += 1
                    
                    # Progress
                    if file_count % 1000 == 0:
                        print(f"  Processed {file_count} files...", end='\r')
                        
                except Exception as e:
                    print(f"\n  [ERR] Failed to pack {rel_path}: {e}")

    print(f"\nComplete Text Backup Ready: {output_filename}")
    print(f"Total Files: {file_count}")
    print(f"Size: {os.path.getsize(output_filename) / (1024*1024):.2f} MB")

if __name__ == "__main__":
    package_everything_to_text("MONOLITH_EVERYTHING_BACKUP.txt")
