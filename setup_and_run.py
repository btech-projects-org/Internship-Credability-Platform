#!/usr/bin/env python3
# ========================
# SETUP AND RUN ENTRY POINT
# ========================
# Single command to validate dependencies and start backend.
# User runs this once. Everything else is automated.

import sys
import os
import subprocess
from pathlib import Path

def main():
    """Main entry point. Run dependency validation before Flask."""
    
    print()
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 68 + "║")
    print("║" + "  INTERNSHIP CREDIBILITY CHECK - AUTOMATED SETUP".center(68) + "║")
    print("║" + " " * 68 + "║")
    print("╚" + "=" * 68 + "╝")
    print()
    
    # Get project root
    project_root = Path(__file__).parent
    validator_path = project_root / "dependency_validator.py"
    
    if not validator_path.exists():
        print("✗ ERROR: dependency_validator.py not found")
        print(f"  Expected at: {validator_path}")
        sys.exit(1)
    
    # Step 1: Run dependency validator
    print("Step 1/2: Running dependency validator...")
    print()
    
    try:
        result = subprocess.run(
            [sys.executable, str(validator_path)],
            cwd=str(project_root)
        )
        
        # Check if validation passed (exit code 0)
        if result.returncode != 0:
            print()
            print("╔" + "=" * 68 + "╗")
            print("║" + " " * 68 + "║")
            print("║" + "  SETUP FAILED - BACKEND WILL NOT START".center(68) + "║")
            print("║" + " " * 68 + "║")
            print("╚" + "=" * 68 + "╝")
            print()
            sys.exit(1)
        
    except Exception as e:
        print(f"✗ Validator execution failed: {e}")
        sys.exit(1)
    
    # Step 2: Start backend
    print("Step 2/2: Starting Flask backend...")
    print()
    
    # Import and run launcher
    sys.path.insert(0, str(project_root))
    
    try:
        # Import launcher
        from launcher import main as launcher_main
        launcher_main()
        
    except KeyboardInterrupt:
        print()
        print()
        print("╔" + "=" * 68 + "╗")
        print("║" + " " * 68 + "║")
        print("║" + "  SERVER STOPPED".center(68) + "║")
        print("║" + " " * 68 + "║")
        print("╚" + "=" * 68 + "╝")
        print()
        sys.exit(0)
    except Exception as e:
        print(f"✗ Backend startup failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
