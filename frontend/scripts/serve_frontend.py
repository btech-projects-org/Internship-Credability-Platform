#!/usr/bin/env python3
"""
Simple HTTP server for frontend development
Purpose: Local static server
Forbidden: Any business logic
"""

import http.server
import socketserver
import os
import sys

PORT = 8000

# Change to frontend directory
frontend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
os.chdir(frontend_dir)

Handler = http.server.SimpleHTTPRequestHandler

try:
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Server running at http://localhost:{PORT}/")
        print(f"Serving from: {os.getcwd()}")
        print("Press Ctrl+C to stop")
        httpd.serve_forever()
except KeyboardInterrupt:
    print("\nServer stopped")
    sys.exit(0)
except OSError as e:
    if "Address already in use" in str(e):
        print(f"Port {PORT} is already in use")
    sys.exit(1)
