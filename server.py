#!/usr/bin/env python3
"""
Simple HTTP server for TechParts mockups
Serves static HTML files from the mockups directory
"""

import http.server
import socketserver
import os
import sys
from pathlib import Path

# Configuration
PORT = 8000
DIRECTORY = "mockups"

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
    
    def end_headers(self):
        # Add CORS headers for ngrok
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        super().end_headers()
    
    def log_message(self, format, *args):
        # Cleaner logging
        print(f"[{self.address_string()}] {format % args}")

def main():
    # Verify mockups directory exists
    if not os.path.exists(DIRECTORY):
        print(f"Error: Directory '{DIRECTORY}' not found!")
        sys.exit(1)
    
    # Change to project root to serve from mockups subdirectory
    os.chdir(Path(__file__).parent)
    
    # Create server
    with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        print(f"\n{'='*60}")
        print(f"TechParts Mockups Server")
        print(f"{'='*60}")
        print(f"Server running at: http://localhost:{PORT}")
        print(f"Serving directory: {DIRECTORY}/")
        print(f"\nTo expose publicly with ngrok:")
        print(f"  ngrok http {PORT}")
        print(f"\n{'='*60}\n")
        print("Press Ctrl+C to stop the server\n")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\nServer stopped.")

if __name__ == "__main__":
    main()

