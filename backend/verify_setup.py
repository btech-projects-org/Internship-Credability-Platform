#!/usr/bin/env python3
"""
System Verification Script
Checks if all components are properly installed and configured
"""

import sys
import os
import json
from pathlib import Path

# Colors for output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_header(text):
    print(f"\n{BLUE}{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}{RESET}\n")

def print_success(text):
    print(f"{GREEN}✓ {text}{RESET}")

def print_error(text):
    print(f"{RED}✗ {text}{RESET}")

def print_warning(text):
    print(f"{YELLOW}⚠ {text}{RESET}")

def print_info(text):
    print(f"{BLUE}ℹ {text}{RESET}")

def check_python_version():
    """Check Python version"""
    print_header("Python Version Check")
    
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    
    if version.major >= 3 and version.minor >= 9:
        print_success(f"Python {version_str}")
        return True
    else:
        print_error(f"Python {version_str} (need 3.9+)")
        return False

def check_packages():
    """Check if required packages are installed"""
    print_header("Package Installation Check")
    
    required_packages = {
        'flask': 'Flask',
        'torch': 'PyTorch',
        'transformers': 'HuggingFace Transformers',
        'sklearn': 'Scikit-learn',
        'numpy': 'NumPy',
        'pandas': 'Pandas',
        'requests': 'Requests',
    }
    
    all_installed = True
    
    for module, name in required_packages.items():
        try:
            __import__(module)
            print_success(f"{name}")
        except ImportError:
            print_error(f"{name} (not installed)")
            all_installed = False
    
    return all_installed

def check_files_structure():
    """Check if required files exist"""
    print_header("Project Structure Check")
    
    required_files = {
        'app.py': 'Flask application',
        'run.py': 'Start script',
        'requirement1.txt': 'Requirements file',
        'services/credibility_engine.py': 'Credibility engine',
        'services/company_verifier.py': 'Company verifier',
        'services/dataset_validator.py': 'Dataset validator',
        'models/random_forest_inference.py': 'ML inference',
        'tests/test_datasets.py': 'Test datasets',
        'tests/run_pipeline_tests.py': 'Test runner',
    }
    
    all_exist = True
    
    for file_path, description in required_files.items():
        full_path = Path(file_path)
        if full_path.exists():
            print_success(f"{description} ({file_path})")
        else:
            print_error(f"{description} (NOT FOUND: {file_path})")
            all_exist = False
    
    return all_exist

def check_data_files():
    """Check if data files exist"""
    print_header("Data Files Check")
    
    data_files = {
        'data/legitimate_companies.json': 'Legitimate companies database',
        'data/scam_companies.json': 'Scam companies database',
        'data/scam_patterns.json': 'Scam patterns database',
    }
    
    all_exist = True
    
    for file_path, description in data_files.items():
        full_path = Path(file_path)
        if full_path.exists():
            try:
                with open(full_path) as f:
                    data = json.load(f)
                    count = len(data) if isinstance(data, list) else len(data.get('companies', []))
                    print_success(f"{description} ({count} entries)")
            except Exception as e:
                print_warning(f"{description} (corrupted: {str(e)})")
        else:
            print_error(f"{description} (NOT FOUND: {file_path})")
            all_exist = False
    
    return all_exist

def check_environment():
    """Check environment configuration"""
    print_header("Environment Configuration Check")
    
    env_file = Path('.env')
    env_example = Path('.env.example')
    
    if env_file.exists():
        print_success(".env file found")
        
        # Check if key APIs are configured
        with open('.env') as f:
            env_content = f.read()
            if 'GOOGLE_CSE_API_KEY' in env_content:
                if '=' in env_content and not env_content.split('GOOGLE_CSE_API_KEY=')[1].split('\n')[0].strip().startswith('#'):
                    print_success("Google CSE API configured")
                else:
                    print_warning("Google CSE API not configured")
            else:
                print_warning("Google CSE API key not in .env")
                
            if 'HUGGINGFACE_API_KEY' in env_content:
                print_info("HuggingFace API key found in .env")
    else:
        if env_example.exists():
            print_warning(".env file not found (template available: .env.example)")
            print_info("Copy .env.example to .env and add your API keys")
        else:
            print_error(".env.example template not found")
            return False
    
    return True

def check_models():
    """Check if ML models exist"""
    print_header("Machine Learning Models Check")
    
    models = {
        'models/saved/random_forest.pkl': 'Random Forest model',
        'models/saved/scaler.pkl': 'Feature scaler',
    }
    
    all_exist = True
    
    for model_path, description in models.items():
        full_path = Path(model_path)
        if full_path.exists():
            size_mb = full_path.stat().st_size / (1024 * 1024)
            print_success(f"{description} ({size_mb:.1f} MB)")
        else:
            print_warning(f"{description} (not found - will be generated on first use)")
    
    return True

def check_documentation():
    """Check if documentation exists"""
    print_header("Documentation Check")
    
    docs = {
        'QUICK_START.md': 'Quick start guide',
        'TESTING_INDEX.md': 'Testing documentation index',
        'PIPELINE_TESTING_GUIDE.md': 'Detailed testing guide',
        'PIPELINE_ARCHITECTURE.md': 'Architecture documentation',
        'TESTING_SUMMARY.md': 'Testing summary',
        'QUICK_TESTING_GUIDE.md': 'Quick testing guide',
    }
    
    all_exist = True
    
    for doc_file, description in docs.items():
        full_path = Path(doc_file)
        if full_path.exists():
            print_success(f"{description}")
        else:
            print_warning(f"{description} (NOT FOUND: {doc_file})")
    
    return True

def main():
    """Run all checks"""
    print(f"{BLUE}")
    print("╔" + "═"*58 + "╗")
    print("║" + " "*58 + "║")
    print("║  " + "INTERNSHIP CREDIBILITY PLATFORM - SYSTEM VERIFICATION" + "  ║")
    print("║" + " "*58 + "║")
    print("╚" + "═"*58 + "╝")
    print(RESET)
    
    results = []
    
    # Run all checks
    results.append(("Python Version", check_python_version()))
    results.append(("Required Packages", check_packages()))
    results.append(("Project Structure", check_files_structure()))
    results.append(("Data Files", check_data_files()))
    results.append(("Environment Config", check_environment()))
    results.append(("ML Models", check_models()))
    results.append(("Documentation", check_documentation()))
    
    # Summary
    print_header("Verification Summary")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for check_name, result in results:
        status = f"{GREEN}✓ PASS{RESET}" if result else f"{RED}✗ FAIL{RESET}"
        print(f"{check_name}: {status}")
    
    print(f"\n{BLUE}Total: {passed}/{total} checks passed{RESET}\n")
    
    if passed == total:
        print_success("All systems operational! Ready to run tests.")
        print_info("Next step: python tests/run_pipeline_tests.py")
        return 0
    elif passed >= total - 2:
        print_warning("System mostly ready. Some optional components missing.")
        print_info("The system will work but with limited functionality.")
        return 0
    else:
        print_error("System verification failed. Install missing components.")
        print_info("See error messages above for details.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
