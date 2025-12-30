#!/bin/bash

# ===================================================
# STARTUP SCRIPT FOR LINUX/MAC
# Automatically installs dependencies and starts API
# ===================================================

echo ""
echo "==================================================="
echo "INTERNSHIP CREDIBILITY CHECKER - BACKEND"
echo "==================================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.12+ from https://www.python.org"
    exit 1
fi

echo "Python found!"
python3 --version
echo ""

# Run the Flask app with auto-install
echo "Starting backend server with auto-dependency installation..."
echo ""

cd "$(dirname "$0")"
python3 run.py

if [ $? -ne 0 ]; then
    echo ""
    echo "ERROR: Failed to start server"
    echo ""
    echo "Try manual installation:"
    echo "  pip3 install -r requirement1.txt"
    echo "  python3 app.py"
    exit 1
fi
