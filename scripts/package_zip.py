import os
import zipfile
import subprocess

def prepare_git_refs():
    head_sha = subprocess.check_output('git rev-parse HEAD', shell=True, text=True).strip()
    git_dir = '.git'
    os.makedirs(os.path.join(git_dir, 'refs', 'heads'), exist_ok=True)

    # Write loose refs for main and master with LF line ending
    with open(os.path.join(git_dir, 'refs', 'heads', 'main'), 'wb') as f:
        f.write((head_sha + '\n').encode('utf-8'))
        
    with open(os.path.join(git_dir, 'refs', 'heads', 'master'), 'wb') as f:
        f.write((head_sha + '\n').encode('utf-8'))

    with open(os.path.join(git_dir, 'HEAD'), 'wb') as f:
        f.write(b'ref: refs/heads/main\n')

def package_project():
    prepare_git_refs()
    zip_filename = "ticketpro.zip"
    if os.path.exists(zip_filename):
        try:
            os.remove(zip_filename)
        except Exception:
            pass
        
    print(f"Packaging {zip_filename} with Linux forward-slash entries & loose refs...")
    
    exclude_dirs = {'node_modules', 'dist', 'venv', '.venv', '__pycache__', '.pytest_cache', 'coverage', '.idea', '.vscode'}
    exclude_files = {'ticketpro.db', 'test_ticketpro.db', zip_filename, 'ticketpro_measure_output.zip'}
    
    file_count = 0
    with zipfile.ZipFile(zip_filename, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=6) as zipf:
        for root, dirs, files in os.walk('.'):
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            
            for file in files:
                if file in exclude_files or file.endswith('.pyc') or file.endswith('.pyo'):
                    continue
                file_path = os.path.join(root, file)
                
                # Crucial fix for Linux zip unpackers (Replit / TrainPlex):
                arcname = os.path.relpath(file_path, '.').replace('\\', '/')
                
                # For text files inside .git/, ensure Unix LF (\n) line endings
                if arcname.startswith('.git/') and (file in {'HEAD', 'config', 'packed-refs', 'COMMIT_EDITMSG'} or 'refs/' in arcname):
                    try:
                        with open(file_path, 'rb') as f_in:
                            content = f_in.read().replace(b'\r\n', b'\n')
                        zipf.writestr(arcname, content)
                        file_count += 1
                        continue
                    except Exception:
                        pass

                zipf.write(file_path, arcname)
                file_count += 1
                
    size_mb = os.path.getsize(zip_filename) / (1024 * 1024)
    print(f"Successfully packaged {file_count} files into {zip_filename} ({size_mb:.2f} MB)")

if __name__ == "__main__":
    package_project()
