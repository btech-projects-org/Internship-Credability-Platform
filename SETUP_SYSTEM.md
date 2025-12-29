# STRICT DEPENDENCY VALIDATION SYSTEM

## Overview

This system provides **100% automated, fail-safe dependency validation** before the backend starts.

### The Guarantee

```
User runs ONE command/file
   ↓
Python is verified (or error)
   ↓
ALL dependencies installed sequentially (or error at first failure)
   ↓
Installation verified via import test
   ↓
Backend starts (only if ALL checks pass)
```

## Files Delivered

### 1. `dependency_validator.py` (Core)
**Purpose**: Strict, non-negotiable dependency validation

**Functionality**:
- ✅ Checks Python availability via CLI
- ✅ Locates requirements.txt
- ✅ Parses all dependencies
- ✅ **Installs SEQUENTIALLY** (one at a time, not batched)
- ✅ **FAILS IMMEDIATELY** on any error
- ✅ Verifies installation via import tests
- ✅ Explicit success/failure messages
- ✅ Blocks backend startup if ANY check fails

**Key Features**:
- No silent failures
- No skipping failed packages
- No assumptions about pre-installed libraries
- Clear error reporting with exact package name
- Non-zero exit codes on failure
- 5-minute timeout per package (prevents hangs)

### 2. `setup_and_run.py` (Orchestrator)
**Purpose**: Unified entry point that chains validation → backend

**Flow**:
1. Runs `dependency_validator.py`
2. Checks exit code (must be 0 for success)
3. If validation fails: exits with error
4. If validation succeeds: imports and starts `launcher.py`

**Result**: Single command to validate + start backend

### 3. `RUN.bat` (Windows Wrapper)
**Purpose**: User-friendly batch file (double-click to run)

**Function**:
- Checks Python is installed
- Runs `setup_and_run.py`
- Shows clear error messages
- Pauses before exit so user can see output

**Usage**:
```
Double-click RUN.bat
```

## Execution Flow

### For Users

**Option 1: Double-click**
```
RUN.bat → setup_and_run.py → dependency_validator.py → launcher.py
```

**Option 2: Command line**
```powershell
python setup_and_run.py
```

**Option 3: Direct (advanced)**
```powershell
python dependency_validator.py
python launcher.py
```

### What Happens

```
Step 1: dependency_validator.py runs
  ├─ [STEP 1] Check Python available
  │   └─ Verify: python --version
  │
  ├─ [STEP 2] Find requirements.txt
  │   └─ Search: ./backend/requirements.txt or ./requirements.txt
  │
  ├─ [STEP 3] Parse requirements
  │   └─ List all 45+ packages from requirements.txt
  │
  ├─ [STEP 4] Install sequentially
  │   ├─ [1/45] Installing: Flask==3.0.0
  │   │   └─ pip install Flask==3.0.0 (waits for completion)
  │   ├─ [2/45] Installing: flask-cors==4.0.0
  │   │   └─ pip install flask-cors==4.0.0 (waits for completion)
  │   ├─ ... (continue for all 45 packages)
  │   │
  │   └─ If ANY fails:
  │       ├─ Print exact package name
  │       ├─ Print error details
  │       └─ EXIT with code 1 (STOPS HERE - no backend)
  │
  ├─ [STEP 5] Verify installation
  │   └─ Test: import flask, import numpy, etc. (for all packages)
  │
  └─ SUCCESS: Print summary and exit(0)

Step 2: setup_and_run.py checks exit code
  ├─ If exit(1): Print error, stop
  └─ If exit(0): Continue to step 3

Step 3: launcher.py starts Flask backend
  ├─ Start server on localhost:5000
  └─ Open browser automatically
```

## Error Handling (STRICT)

### If Python is not found
```
[STEP 1] Checking Python availability...
  Using executable: C:\Python312\python.exe
  Version: 3.12.3

✗ FATAL ERROR: Python not found
Issue: Cannot execute: C:\Python312\python.exe
Solution: Install Python from python.org and ensure it's in your PATH

⚠️  BACKEND WILL NOT START
⚠️  FIX THE ISSUE ABOVE AND TRY AGAIN

Exit code: 1 (non-zero)
Backend does NOT start
```

### If requirements.txt is missing
```
[STEP 2] Locating requirements.txt...

✗ FATAL ERROR: requirements.txt not found
Issue: Searched multiple locations...
Solution: Ensure requirements.txt exists in project root or backend/

⚠️  BACKEND WILL NOT START

Exit code: 1 (non-zero)
Backend does NOT start
```

### If ANY dependency installation fails
```
[STEP 4] Installing dependencies (sequential)...

  [1/45] Installing: Flask                           (Flask==3.0.0)
         ✓ OK
  [2/45] Installing: flask-cors                     (flask-cors==4.0.0)
         ✓ OK
  [3/45] Installing: numpy                         (numpy==1.26.2)
         ✓ OK
  [4/45] Installing: SOME_PACKAGE_THAT_FAILS      (some-package==1.0.0)
         ✗ FAILED

  ══════════════════════════════════════════════════════════════
  ✗ INSTALLATION FAILURE: SOME_PACKAGE_THAT_FAILS
  ══════════════════════════════════════════════════════════════

  Package Spec: some-package==1.0.0
  Exit Code: 1

  STDOUT:
    ERROR: Could not find a version that satisfies the requirement ...

  STDERR:
    No matching distribution found for some-package==1.0.0

  ══════════════════════════════════════════════════════════════

✗ FATAL ERROR: Installation of 'SOME_PACKAGE_THAT_FAILS' failed
Issue: pip install some-package==1.0.0 returned exit code 1
Solution: Fix the issue and try again

⚠️  BACKEND WILL NOT START

Exit code: 1 (non-zero)
Backend does NOT stop at failures - stops IMMEDIATELY at first failure
```

### If import verification fails
```
[STEP 5] Verifying installation...

  ✓ Flask                           (import: flask)
  ✓ flask-cors                      (import: flask_cors)
  ✗ some-package                    (import failed: some_package)

  Verified: 44/45 packages

  Import failures:
    - some-package (import some_package): No module named 'some_package'

✗ FATAL ERROR: Installation verification failed
Issue: 1 packages failed import verification
Solution: Packages were installed but cannot be imported

Exit code: 1 (non-zero)
Backend does NOT start
```

## Success Message

If everything passes:
```
══════════════════════════════════════════════════════════════

  ✓ ALL CHECKS PASSED

  Python Version: 3.12.3
  Python Executable: C:\Python312\python.exe
  Packages Installed: 45

  ✓ Backend is ready to start

══════════════════════════════════════════════════════════════
```

Then launcher.py starts automatically, and backend begins.

## Functional Requirements Met

✅ **Python Availability Check**
- Verifies Python is installed and accessible via CLI
- Terminates immediately if not found
- Backend DOES NOT start

✅ **Automated Dependency Installation**
- Reads all 45+ packages from requirements.txt
- Installs SEQUENTIALLY (one at a time, not batched)
- Each package installation waits for completion before next

✅ **Failure Handling (STRICT)**
- Stops execution IMMEDIATELY on first failure
- Prints exact package name that failed
- Exits with non-zero status code (exit 1)
- Backend execution is BLOCKED

✅ **Backend Execution Control**
- Backend starts ONLY after:
  - Python is confirmed available
  - ALL dependencies are installed successfully
  - ALL imports are verified
- NO partial execution allowed

✅ **Unknown System Compatibility**
- Assumes unknown OS (works on Windows, Linux, macOS)
- Assumes NO pre-installed libraries
- Assumes NO pre-built ML/DL packages
- Fails safely and explicitly if conditions not met

✅ **Execution Rules**
- User runs ONE file/command only (RUN.bat or python setup_and_run.py)
- No manual pip install steps required
- No manual environment configuration needed
- Backend doesn't start unless 100% valid state

## Guaranteed Behavior

### Case 1: Python NOT installed
```
Action: Run RUN.bat or python setup_and_run.py
Result: Clear error → Backend does NOT start
```

### Case 2: Python installed, dependencies missing
```
Action: Run RUN.bat
Result: Validator installs all sequentially → Backend starts
```

### Case 3: Python installed, dependency X fails
```
Action: Run RUN.bat
Result: Stops at package X → Clear error → Backend does NOT start
```

### Case 4: All dependencies installed, but some missing from system
```
Action: Run RUN.bat
Result: Validator installs missing → Backend starts
```

### Case 5: All dependencies OK, old/incompatible versions
```
Action: Run RUN.bat
Result: Validator enforces exact versions from requirements.txt → Backend starts with correct versions
```

## Usage Instructions

### For Users (First Time)

**Windows:**
```
1. Open project folder
2. Double-click RUN.bat
3. Wait for setup (2-10 minutes first time)
4. Browser opens automatically
5. App is ready to use
```

**Command line:**
```
python setup_and_run.py
```

### For Developers

**Local development (test code changes):**
```bash
python dependency_validator.py    # One-time: validate + install
cd backend
python app.py                      # Start Flask directly
```

**Build for distribution:**
```bash
build.bat    # Creates dist/CredibilityCheck.exe (as before)
```

## Implementation Notes

### Sequential Installation (Why?)
- **Why not batch?** Batch installation can have cascading failures where one bad package masks another
- **Sequential approach** shows exactly which package fails
- **Clear accountability** - user knows which dependency has the problem
- **Better diagnostics** - error messages are specific to one package

### 5-Minute Timeout
- Some packages (PyTorch, TensorFlow) take a long time to download/compile
- 5 minutes is generous for most systems
- Prevents hanging indefinitely if download stalls

### Import Verification
- Confirms packages installed and are importable
- Catches cases where pip says "OK" but package is broken
- Final sanity check before backend starts

### Exit Codes
- `exit(0)` - Success, all checks passed, backend can start
- `exit(1)` - Failure, issue found, backend BLOCKED

## Failure Constraints (Reality Check)

This system **CANNOT guarantee** execution if:

❌ **Python is not installed**
- Solution: User must install Python 3.12+ from python.org
- System will fail clearly and explicitly

❌ **Internet access is unavailable**
- Solution: pip needs internet to download packages
- System will fail at first package and report the issue

❌ **OS-level permissions block installations**
- Solution: User may need to run as Administrator or use `--user` flag
- System will fail and show permission error

❌ **System disk space exhausted**
- Solution: Free up disk space (45+ packages need ~2-3 GB)
- System will fail when pip reports disk full

These constraints are **ACKNOWLEDGED, NOT HIDDEN**. Error messages will explicitly state the root cause.

## Architecture Diagram

```
RUN.bat (user double-clicks)
   ↓
Python check (RUN.bat)
   ↓
setup_and_run.py (Python script)
   ↓
dependency_validator.py (core validation)
   │
   ├─ Check Python available
   ├─ Find requirements.txt
   ├─ Parse 45+ packages
   ├─ Install sequentially (pkg1, pkg2, ..., pkg45)
   │  └─ STOP on first failure
   ├─ Verify installation (import test)
   │  └─ STOP if imports fail
   │
   └─ Return exit code
      ├─ 0 = Success, continue
      └─ 1 = Failure, STOP

setup_and_run.py (checks exit code)
   ├─ If 1: Print error, exit
   └─ If 0: Continue

launcher.py (Flask backend)
   ├─ Start server on localhost:5000
   └─ Open browser automatically

Browser
   └─ User can access web interface
```

## Testing the System

### Test Case 1: Normal startup
```
python setup_and_run.py
Expected: All validation passes → Backend starts → Browser opens
```

### Test Case 2: Missing dependency (simulate)
```
Edit requirements.txt, add: bad-package-name==1.0.0
python setup_and_run.py
Expected: Installer fails at bad-package-name → Clear error → Backend blocked
```

### Test Case 3: Python validation only
```
python dependency_validator.py
Expected: Runs validation, installs deps, prints success, exits(0)
```

## Summary

This system provides:

✅ **Zero ambiguity** - Clear success/failure messages
✅ **Zero assumptions** - Validates everything explicitly
✅ **Zero partial execution** - All-or-nothing approach
✅ **Zero manual steps** - Fully automated
✅ **Zero silent failures** - Every error is reported
✅ **Guaranteed safety** - Backend doesn't start if ANY check fails

**User experience**: Download → Double-click RUN.bat → Done

**Developer experience**: Edit code → Run RUN.bat → Immediate feedback on setup status
