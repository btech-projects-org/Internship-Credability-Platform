#!/usr/bin/env python3
# ========================
# STRICT DEPENDENCY VALIDATOR & INSTALLER
# ========================
# Ensures Python exists, installs ALL dependencies sequentially,
# and BLOCKS execution if ANY dependency fails.
# No silent failures. No partial installs. No assumptions.

import sys
import subprocess
import os
from pathlib import Path

class DependencyValidator:
    """Validates Python availability and installs all dependencies sequentially."""
    
    def __init__(self):
        self.failed_packages = []
        self.installed_packages = []
        self.python_executable = None
        self.requirements_file = None
        
    def check_python_availability(self):
        """
        MANDATORY: Verify Python is installed and accessible.
        Fails immediately if not found.
        """
        print("=" * 70)
        print("  DEPENDENCY VALIDATOR - STARTUP CHECK")
        print("=" * 70)
        print()
        
        print("[STEP 1] Checking Python availability...")
        print(f"  Using executable: {sys.executable}")
        print(f"  Version: {sys.version.split()[0]}")
        
        # Verify Python is accessible via CLI
        try:
            result = subprocess.run(
                [sys.executable, "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode != 0:
                self.fatal_error(
                    "Python check failed",
                    f"Executable {sys.executable} returned non-zero exit code",
                    "Install Python 3.12+ from python.org and ensure it's in PATH"
                )
            
            print(f"  ✓ Python is available and accessible")
            self.python_executable = sys.executable
            print()
            return True
            
        except FileNotFoundError:
            self.fatal_error(
                "Python not found",
                f"Cannot execute: {sys.executable}",
                "Install Python from python.org and ensure it's in your PATH"
            )
        except subprocess.TimeoutExpired:
            self.fatal_error(
                "Python check timeout",
                "Python executable did not respond within 5 seconds",
                "Verify Python installation and system resources"
            )
        except Exception as e:
            self.fatal_error(
                "Python availability check failed",
                str(e),
                "System may have permission or configuration issues"
            )
    
    def locate_requirements_file(self):
        """Find requirements.txt in backend/ directory."""
        print("[STEP 2] Locating requirements.txt...")
        
        possible_paths = [
            Path(__file__).parent / "backend" / "requirements.txt",
            Path(__file__).parent / "requirements.txt",
            Path.cwd() / "backend" / "requirements.txt",
            Path.cwd() / "requirements.txt",
        ]
        
        for req_path in possible_paths:
            if req_path.exists():
                print(f"  Found: {req_path}")
                self.requirements_file = req_path
                print()
                return True
        
        self.fatal_error(
            "requirements.txt not found",
            f"Searched: {', '.join(str(p) for p in possible_paths)}",
            "Ensure requirements.txt exists in project root or backend/"
        )
    
    def parse_requirements(self):
        """
        Parse requirements.txt file.
        Returns: List of package specs (with versions).
        """
        print("[STEP 3] Parsing requirements.txt...")
        
        packages = []
        line_number = 0
        
        if self.requirements_file is None:
            self.fatal_error(
                "requirements_file not set",
                "Internal error: locate_requirements_file must be called first",
                "Contact support"
            )
        
        try:
            with open(str(self.requirements_file), 'r') as f:
                for line in f:
                    line_number += 1
                    line = line.strip()
                    
                    # Skip empty lines and comments
                    if not line or line.startswith('#'):
                        continue
                    
                    packages.append(line)
            
            print(f"  Found {len(packages)} packages to install")
            for i, pkg in enumerate(packages, 1):
                # Parse package name (before ==, >=, <=, etc.)
                pkg_name = pkg.split('==')[0].split('>=')[0].split('<=')[0].split('>')[0].split('<')[0].split('!=')[0].strip()
                print(f"    {i}. {pkg_name:<30} ({pkg})")
            
            print()
            return packages
            
        except FileNotFoundError:
            self.fatal_error(
                "requirements.txt disappeared",
                f"File was found but is now inaccessible: {self.requirements_file}",
                "Check file permissions and system status"
            )
        except Exception as e:
            self.fatal_error(
                "Failed to parse requirements.txt",
                str(e),
                "File may be corrupted or unreadable"
            )
    
    def install_dependencies_sequential(self, packages):
        """
        Install each dependency ONE AT A TIME.
        FAIL IMMEDIATELY on any error.
        NO SKIPPING. NO BATCHING.
        """
        print("[STEP 4] Installing dependencies (sequential)...")
        print()
        
        total = len(packages)
        
        for index, package_spec in enumerate(packages, 1):
            pkg_name = package_spec.split('==')[0].split('>=')[0].split('<=')[0].split('>')[0].split('<')[0].split('!=')[0].strip()
            
            print(f"  [{index}/{total}] Installing: {pkg_name:<30} ({package_spec})")
            
            # SEQUENTIAL installation - one at a time
            try:
                if self.python_executable is None:
                    self.fatal_error(
                        "python_executable not set",
                        "Internal error: check_python_availability must be called first",
                        "Contact support"
                    )
                
                result = subprocess.run(
                    [self.python_executable, "-m", "pip", "install", package_spec],
                    capture_output=True,
                    text=True,
                    timeout=300  # 5 minute timeout per package
                )
                
                if result.returncode != 0:
                    # FAIL IMMEDIATELY - do not continue
                    print(f"         ✗ FAILED")
                    print()
                    self.failed_packages.append(pkg_name)
                    self.print_install_failure(pkg_name, package_spec, result)
                    # NO RECOVERY - STOP HERE
                    self.fatal_error(
                        f"Installation of '{pkg_name}' failed",
                        f"pip install {package_spec} returned exit code {result.returncode}",
                        "Fix the issue and try again"
                    )
                else:
                    print(f"         ✓ OK")
                    self.installed_packages.append(pkg_name)
                    
            except subprocess.TimeoutExpired:
                print(f"         ✗ TIMEOUT (>5 min)")
                print()
                self.failed_packages.append(pkg_name)
                self.fatal_error(
                    f"Installation of '{pkg_name}' timed out",
                    f"Package took longer than 5 minutes to install",
                    "Check internet connection or try again later"
                )
            except Exception as e:
                print(f"         ✗ ERROR: {str(e)}")
                print()
                self.failed_packages.append(pkg_name)
                self.fatal_error(
                    f"Installation of '{pkg_name}' encountered system error",
                    str(e),
                    "Check system resources and permissions"
                )
        
        print()
        return len(self.failed_packages) == 0
    
    def print_install_failure(self, pkg_name, spec, result):
        """Print detailed failure information."""
        print()
        print("  " + "=" * 66)
        print(f"  INSTALLATION FAILURE: {pkg_name}")
        print("  " + "=" * 66)
        print()
        print(f"  Package Spec: {spec}")
        print(f"  Exit Code: {result.returncode}")
        print()
        
        if result.stdout:
            print("  STDOUT:")
            for line in result.stdout.split('\n')[-20:]:  # Last 20 lines
                if line.strip():
                    print(f"    {line}")
        
        if result.stderr:
            print()
            print("  STDERR:")
            for line in result.stderr.split('\n')[-20:]:  # Last 20 lines
                if line.strip():
                    print(f"    {line}")
        
        print()
        print("  " + "=" * 66)
        print()
    
    def verify_installation(self, packages):
        """Verify all packages were installed by attempting import."""
        print("[STEP 5] Verifying installation...")
        print()
        
        # Extract just package names for import verification
        import_names = {
            'flask': 'flask',
            'flask-cors': 'flask_cors',
            'python-dotenv': 'dotenv',
            'numpy': 'numpy',
            'pandas': 'pandas',
            'scikit-learn': 'sklearn',
            'transformers': 'transformers',
            'torch': 'torch',
            'nltk': 'nltk',
            'spacy': 'spacy',
            'textblob': 'textblob',
            'requests': 'requests',
            'beautifulsoup4': 'bs4',
            'lxml': 'lxml',
            'url-normalize': 'url_normalize',
            'tldextract': 'tldextract',
            'whois': 'whois',
            'gunicorn': 'gunicorn',
            'pyinstaller': 'PyInstaller',
            'pytest': 'pytest',
            'pytest-flask': 'pytest_flask',
        }
        
        verified = 0
        failed_imports = []
        
        for package_spec in packages:
            pkg_name = package_spec.split('==')[0].split('>=')[0].split('<=')[0].split('>')[0].split('<')[0].split('!=')[0].strip()
            import_name = import_names.get(pkg_name.lower(), pkg_name.lower().replace('-', '_'))
            
            if not import_name:
                import_name = pkg_name.lower().replace('-', '_')
            
            try:
                __import__(import_name)
                print(f"  ✓ {pkg_name:<30} (import: {import_name})")
                verified += 1
            except ImportError as e:
                print(f"  ✗ {pkg_name:<30} (import failed: {import_name})")
                failed_imports.append((pkg_name, import_name, str(e)))
        
        print()
        print(f"  Verified: {verified}/{len(packages)} packages")
        
        if failed_imports:
            print()
            print("  Import failures:")
            for pkg, imp, err in failed_imports:
                print(f"    - {pkg} (import {imp}): {err}")
            print()
            self.fatal_error(
                "Installation verification failed",
                f"{len(failed_imports)} packages failed import verification",
                "Packages were installed but cannot be imported"
            )
        
        print()
        return True
    
    def fatal_error(self, title, message, solution):
        """
        Print fatal error and exit with non-zero status.
        BLOCKS backend execution.
        """
        print()
        print("  " + "=" * 66)
        print(f"  ✗ FATAL ERROR: {title}")
        print("  " + "=" * 66)
        print()
        print(f"  Issue: {message}")
        print()
        print(f"  Solution: {solution}")
        print()
        print("  " + "=" * 66)
        print()
        print("  ⚠️  BACKEND WILL NOT START")
        print("  ⚠️  FIX THE ISSUE ABOVE AND TRY AGAIN")
        print()
        print("=" * 70)
        
        sys.exit(1)  # NON-ZERO EXIT - BLOCKS EXECUTION
    
    def success_message(self):
        """Print success message before backend startup."""
        print("=" * 70)
        print()
        print("  ✓ ALL CHECKS PASSED")
        print()
        print(f"  Python Version: {sys.version.split()[0]}")
        print(f"  Python Executable: {self.python_executable}")
        print(f"  Packages Installed: {len(self.installed_packages)}")
        print()
        print("  ✓ Backend is ready to start")
        print()
        print("=" * 70)
        print()
    
    def validate_and_install(self):
        """
        Main entry point. Performs ALL validation steps.
        Returns True if ready to start backend, False otherwise (actually exits on error).
        """
        try:
            # STEP 1: Python check
            self.check_python_availability()
            
            # STEP 2: Find requirements.txt
            self.locate_requirements_file()
            
            # STEP 3: Parse requirements
            packages = self.parse_requirements()
            
            # STEP 4: Install sequentially
            install_success = self.install_dependencies_sequential(packages)
            
            if not install_success:
                self.fatal_error(
                    "Dependency installation incomplete",
                    f"One or more packages failed to install",
                    "Review errors above and try again"
                )
            
            # STEP 5: Verify installation
            self.verify_installation(packages)
            
            # SUCCESS: All checks passed
            self.success_message()
            return True
            
        except KeyboardInterrupt:
            print()
            print()
            print("=" * 70)
            print("  USER INTERRUPT")
            print("=" * 70)
            print()
            sys.exit(1)
        except Exception as e:
            print()
            print()
            self.fatal_error(
                "Unexpected error during validation",
                str(e),
                "Check system status and try again"
            )


def main():
    """Entry point for dependency validation."""
    validator = DependencyValidator()
    success = validator.validate_and_install()
    
    if not success:
        sys.exit(1)
    
    # If we reach here, all dependencies are installed and verified
    sys.exit(0)


if __name__ == '__main__':
    main()
