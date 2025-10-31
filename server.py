#!/usr/bin/env python3
"""
Simple HTTP server for TechParts mockups
Serves static HTML files from the mockups directory
"""

import http.server
import socketserver
import os
import sys
import subprocess
import platform
import time
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

def kill_process_on_port(port):
    """Kill any process using the specified port"""
    try:
        if platform.system() == "Windows":
            # Windows: Find process using the port
            result = subprocess.run(
                ["netstat", "-ano"],
                capture_output=True,
                text=True,
                check=False
            )
            
            # Find line with LISTENING on our port
            for line in result.stdout.split('\n'):
                if f':{port}' in line and 'LISTENING' in line:
                    parts = line.split()
                    if len(parts) >= 5:
                        pid = parts[-1]
                        try:
                            # Kill the process
                            subprocess.run(
                                ["taskkill", "/PID", pid, "/F"],
                                capture_output=True,
                                check=False
                            )
                            print(f"Killed process {pid} using port {port}")
                            return True
                        except Exception:
                            pass
        else:
            # Unix/Linux/Mac: Find and kill process
            result = subprocess.run(
                ["lsof", "-ti", f":{port}"],
                capture_output=True,
                text=True,
                check=False
            )
            if result.stdout.strip():
                pids = result.stdout.strip().split('\n')
                for pid in pids:
                    try:
                        subprocess.run(["kill", "-9", pid], check=False)
                        print(f"Killed process {pid} using port {port}")
                    except Exception:
                        pass
                return True
    except Exception as e:
        print(f"Warning: Could not check/kill processes on port {port}: {e}")
    return False

def check_port_available(port):
    """Check if port is available by trying to bind to it"""
    test_socket = socketserver.socket.socket(socketserver.socket.AF_INET, socketserver.socket.SOCK_STREAM)
    test_socket.setsockopt(socketserver.socket.SOL_SOCKET, socketserver.socket.SO_REUSEADDR, 1)
    try:
        test_socket.bind(("", port))
        test_socket.close()
        return True
    except OSError:
        test_socket.close()
        return False

def main():
    # Verify mockups directory exists
    if not os.path.exists(DIRECTORY):
        print(f"Error: Directory '{DIRECTORY}' not found!")
        sys.exit(1)
    
    # Change to project root to serve from mockups subdirectory
    os.chdir(Path(__file__).parent)
    
    # Check if port is available, kill process if not
    if not check_port_available(PORT):
        print(f"Port {PORT} is in use. Attempting to free it...")
        if kill_process_on_port(PORT):
            # Give it a moment to free up
            time.sleep(0.5)
        else:
            print(f"Warning: Could not free port {PORT}. The server may still fail to start.")
    
    # Create server
    try:
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
    except OSError as e:
        print(f"\nError: Could not start server on port {PORT}")
        print(f"Details: {e}")
        print("\nTip: Another process may still be using the port.")
        print("You may need administrator privileges to kill it.")
        sys.exit(1)

if __name__ == "__main__":
    main()

