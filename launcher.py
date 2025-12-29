#!/usr/bin/env python3
# ========================
# CREDIBILITY CHECK LAUNCHER
# Single-file PyInstaller entry point
# ========================

import sys
import os
import webbrowser
import time
from pathlib import Path

# Ensure backend is in path
sys.path.insert(0, str(Path(__file__).parent / 'backend'))

# Set environment variables
os.environ['FLASK_ENV'] = 'production'
os.environ['PYTHONUNBUFFERED'] = '1'

def main():
    """Launch the Flask app and open frontend in browser"""
    print("=" * 60)
    print("  INTERNSHIP CREDIBILITY CHECK - LOCAL DEPLOYMENT")
    print("=" * 60)
    print()
    
    # Import Flask app
    try:
        from app import app
        print("✓ Flask app loaded successfully")
    except Exception as e:
        print(f"✗ Failed to load Flask app: {e}")
        sys.exit(1)
    
    # Log startup
    print("✓ Starting backend server on http://localhost:5000")
    print("✓ Frontend will open automatically...")
    print()
    print("Press Ctrl+C to stop the server.")
    print("-" * 60)
    print()
    
    # Start Flask in main thread (blocking)
    # Open browser after a brief delay
    import threading
    
    def open_browser():
        time.sleep(2)  # Wait for server to start
        try:
            frontend_path = Path(__file__).parent / 'frontend' / 'pages' / 'index.html'
            if frontend_path.exists():
                webbrowser.open(f'file:///{frontend_path}')
                print(f"\n✓ Frontend opened: {frontend_path}")
            else:
                print(f"\n⚠ Frontend file not found: {frontend_path}")
                print(f"  Manually open: http://localhost:5000 or {frontend_path}")
        except Exception as e:
            print(f"\n⚠ Auto-open failed: {e}")
            print(f"  Manually open: http://localhost:5000 or {frontend_path}")
    
    browser_thread = threading.Thread(target=open_browser, daemon=True)
    browser_thread.start()
    
    try:
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=False,
            use_reloader=False,
            threaded=True
        )
    except KeyboardInterrupt:
        print("\n" + "=" * 60)
        print("Server stopped by user.")
        print("=" * 60)
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ Server error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
