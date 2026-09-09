import os
import sys
import subprocess

def count_lines_and_files(directory, extensions):
    total_loc = 0
    total_files = 0
    
    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if d not in ('node_modules', '__pycache__', '.git', 'dist', 'venv', 'coverage', '.pytest_cache')]
        for file in files:
            ext = os.path.splitext(file)[1]
            if ext in extensions:
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'rb') as f:
                        lines = f.read().count(b'\n') + 1
                        total_loc += lines
                        total_files += 1
                except Exception:
                    pass
    return total_loc, total_files

def audit_project():
    print("=" * 60)
    print("TICKETPRO — AUTOMATED PROJECT AUDIT REPORT")
    print("=" * 60)
    sys.stdout.flush()
    
    # 1. Measure Production LOC & Files
    prod_extensions = ['.py', '.ts', '.tsx', '.js', '.jsx']
    backend_loc, backend_files = count_lines_and_files('backend', prod_extensions)
    frontend_loc, frontend_files = count_lines_and_files('frontend/src', prod_extensions)
    
    total_prod_loc = backend_loc + frontend_loc
    total_prod_files = backend_files + frontend_files
    
    # 2. Measure Test Files
    test_loc, test_files = count_lines_and_files('tests', ['.py', '.ts', '.tsx'])
    
    # 3. Check Git commits
    try:
        commit_output = subprocess.check_output(['git', 'rev-list', '--count', 'HEAD'], stderr=subprocess.DEVNULL).decode().strip()
        commit_count = int(commit_output)
    except Exception:
        commit_count = 0
        
    # 4. Check Secrets & License
    has_env = os.path.exists('.env')
    has_license = os.path.exists('LICENSE')
    has_docker = os.path.exists('docker-compose.yml')
    has_ci = os.path.exists('.github/workflows/ci.yml')
    has_readme = os.path.exists('README.md')
    
    print(f"Production LOC:        {total_prod_loc} (Backend: {backend_loc}, Frontend: {frontend_loc})")
    print(f"Production Files:      {total_prod_files}")
    print(f"Test Specification Files: {test_files}")
    print(f"Git Commits Count:     {commit_count}")
    print(f"Committed .env File:   {'FAIL (Found .env)' if has_env else 'PASS (None committed)'}")
    print(f"Open-Source LICENSE:   {'FAIL (Found LICENSE)' if has_license else 'PASS (No LICENSE as required)'}")
    print(f"Docker Setup:          {'PASS' if has_docker else 'FAIL'}")
    print(f"CI/CD Workflow:        {'PASS' if has_ci else 'FAIL'}")
    print(f"README Present:        {'PASS' if has_readme else 'FAIL'}")
    print("=" * 60)
    sys.stdout.flush()
    
    return {
        "prod_loc": total_prod_loc,
        "prod_files": total_prod_files,
        "test_files": test_files,
        "commit_count": commit_count,
        "has_env": has_env,
        "has_license": has_license
    }

if __name__ == "__main__":
    audit_project()
