#!/usr/bin/env python3
"""
Validate all file paths in frontend
Purpose: Validate relative paths
Forbidden: Runtime dependencies
"""

import os
from pathlib import Path

def validate_paths():
    """Validate all paths in frontend structure"""
    frontend_root = Path(__file__).parent.parent
    errors = []
    
    print("Validating frontend paths...")
    print(f"Frontend root: {frontend_root}\n")
    
    # Check required directories
    required_dirs = [
        'pages',
        'css/base',
        'css/components',
        'css/animations',
        'js/core',
        'js/analysis',
        'js/config',
        'js/utils',
        'assets/video'
    ]
    
    for dir_path in required_dirs:
        full_path = frontend_root / dir_path
        if not full_path.exists():
            errors.append(f"Missing directory: {dir_path}")
        else:
            print(f"✓ {dir_path}")
    
    # Check required files
    required_files = [
        'css/main.css',
        'css/base/style.css',
        'css/base/layout.css',
        'css/components/components.css',
        'css/animations/animations.css',
        'js/core/validation.js',
        'js/core/storage.js',
        'js/core/navigation.js',
        'js/core/ui.js',
        'js/analysis/analysis.js',
        'js/analysis/resume.js',
        'js/analysis/result.js',
        'js/config/config.js',
        'js/utils/button-state.js',
        'pages/index.html',
        'pages/check.html',
        'pages/analysis.html',
        'pages/result.html'
    ]
    
    print("\nChecking files:")
    for file_path in required_files:
        full_path = frontend_root / file_path
        if not full_path.exists():
            errors.append(f"Missing file: {file_path}")
        else:
            print(f"✓ {file_path}")
    
    print("\n" + "="*50)
    if errors:
        print("VALIDATION FAILED")
        print("\nErrors found:")
        for error in errors:
            print(f"  ✗ {error}")
        return False
    else:
        print("VALIDATION PASSED")
        print("All required paths exist!")
        return True


if __name__ == '__main__':
    success = validate_paths()
    exit(0 if success else 1)
