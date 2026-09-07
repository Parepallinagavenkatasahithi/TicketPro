import os
import zipfile

def package_project():
    zip_filename = "ticketpro.zip"
    if os.path.exists(zip_filename):
        os.remove(zip_filename)
        
    print(f"Creating {zip_filename}...")
    
    exclude_dirs = {'node_modules', 'dist', 'venv', '.venv', '__pycache__', '.pytest_cache'}
    exclude_files = {'ticketpro.db', 'test_ticketpro.db', zip_filename}
    
    file_count = 0
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk('.'):
            # Exclude unwanted directories
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            
            for file in files:
                if file in exclude_files or file.endswith('.pyc') or file.endswith('.pyo'):
                    continue
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, '.')
                zipf.write(file_path, arcname)
                file_count += 1
                
    size_mb = os.path.getsize(zip_filename) / (1024 * 1024)
    print(f"Successfully packaged {file_count} files into {zip_filename} ({size_mb:.2f} MB)")

if __name__ == "__main__":
    package_project()
