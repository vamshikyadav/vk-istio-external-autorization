from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import json

# Read the list of allowed users from an environment variable
def read_allowed_users():
    allowed_users_str = os.environ.get('ALLOWED_USERS', '')
    return allowed_users_str.split(',')

# Define a simple access control policy
allowed_users = read_allowed_users()
allowed_paths = ["/api/allowed"]
allowed_methods = ["GET", "POST"]

class AuthorizationHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Read the incoming request body
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        request = json.loads(body.decode('utf-8'))

        # Extract relevant information from the request
        path = request.get("path", "")
        method = request.get("method", "")
        user = request.get("user", "")

        # Check if the request is allowed based on the access control policy
        if path in allowed_paths and method in allowed_methods and user in allowed_users:
            self.send_response(200)
        else:
            self.send_response(403)
        
        self.end_headers()

def run(server_class=HTTPServer, handler_class=AuthorizationHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting authorization server on port {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
