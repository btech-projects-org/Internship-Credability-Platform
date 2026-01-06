"""
Auto-Install Dependencies on Startup
This module checks and installs missing packages automatically
"""

import subprocess
import sys
import os
from pathlib import Path

def install_dependencies():
    """Check and install missing dependencies from requirement1.txt"""
    
    # Get the backend directory
    backend_dir = Path(__file__).parent
    requirements_file = backend_dir / "requirement1.txt"
    
    if not requirements_file.exists():
        print(f"ERROR: {requirements_file} not found!")
        return False
    
    print("\n" + "="*70)
    print("CHECKING & INSTALLING DEPENDENCIES")
    print("="*70)
    
    try:
        # Install packages from requirements file
        print(f"\nInstalling packages from {requirements_file.name}...")
        print("This may take a few minutes on first run...\n")
        
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", str(requirements_file)],
            capture_output=False,
            text=True
        )
        
        if result.returncode == 0:
            print("\n" + "="*70)
            print("SUCCESS: All dependencies installed!")
            print("="*70 + "\n")
            return True
        else:
            print("\nERROR: Failed to install dependencies")
            return False
            
    except Exception as e:
        print(f"\nERROR: {e}")
        return False

def check_imports():
    """Verify critical imports are available"""
    required_modules = [
        'flask',
        'flask_cors',
        'transformers',
        'sklearn',
        'requests',
    ]
    
    print("Verifying critical imports...")
    missing = []
    
    for module in required_modules:
        try:
            __import__(module)
            print(f"  ✓ {module}")
        except ImportError:
            print(f"  ✗ {module}")
            missing.append(module)
    
    if missing:
        print(f"\nWARNING: {len(missing)} packages still missing")
        return False
    
    print("\n✓ All critical imports available!")
    return True

if __name__ == "__main__":
    success = install_dependencies()
    if success:
        check_imports()
