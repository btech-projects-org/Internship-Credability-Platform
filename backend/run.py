"""
STARTUP SCRIPT - Run this to start the API with auto-dependency installation
Usage: python run.py
"""

import subprocess
import sys
import os
from pathlib import Path

def main():
    """Run the Flask application with auto-install"""
    
    print("\n" + "="*70)
    print("INTERNSHIP CREDIBILITY CHECKER - BACKEND")
    print("="*70)
    
    backend_dir = Path(__file__).parent
    app_file = backend_dir / "app.py"
    
    if not app_file.exists():
        print(f"ERROR: {app_file} not found!")
        sys.exit(1)
    
    print(f"\nStarting backend server...")
    print(f"Location: {backend_dir}")
    print(f"App: {app_file.name}\n")
    
    try:
        # Run the Flask app
        result = subprocess.run(
            [sys.executable, str(app_file)],
            cwd=str(backend_dir)
        )
        sys.exit(result.returncode)
    except KeyboardInterrupt:
        print("\n\nServer stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
