import http.server
import socketserver
import os
import sys

PORT = 8000
DIRECTORY = "dashboard"

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

def main():
    if not os.path.exists(DIRECTORY):
        print(f"Error: Directory '{DIRECTORY}' not found.")
        sys.exit(1)
        
    # Ensure db.json exists or create a sample one
    if not os.path.exists("db.json"):
        with open("db.json", "w") as f:
            f.write("[]")
            
    os.chdir(".") # Stay in root so it can access ../db.json from dashboard/
    
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Dashboard serving at http://localhost:{PORT}/dashboard/")
        print("Press Ctrl+C to stop.")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nStopping server.")

if __name__ == "__main__":
    main()
