import http.server 
import socketserver 
import os 
import subprocess 
import json 
import cgi 
 
PORT = 8000 
 
class JSPyHandler(http.server.SimpleHTTPRequestHandler): 
    def do_POST(self): 
        if self.path == '/save': 
            content_length = int(self.headers['Content-Length']) 
            post_data = self.rfile.read(content_length).decode('utf-8') 
            js_code = json.loads(post_data)['code'] 
 
            # Save the JavaScript code to a file 
            with open('samples/sample.js', 'w') as f: 
                f.write(js_code) 
 
            # Send response 
            self.send_response(200) 
            self.send_header('Content-type', 'application/json') 
            self.send_header('Access-Control-Allow-Origin', '*') 
            self.end_headers() 
            self.wfile.write(json.dumps({'success': True}).encode()) 
 
        elif self.path == '/convert': 
            # Try to use the improved Python converter first 
            try: 
                subprocess.run(['python', 'converters/js2py_improved.py', 'samples/sample.js', 'output/output.py'], check=True) 
            except subprocess.CalledProcessError: 
                # If improved converter fails, try the original Python converter 
                try: 
                    subprocess.run(['python', 'converters/js2py_converter.py', 'samples/sample.js', 'output/output.py'], check=True) 
                except subprocess.CalledProcessError: 
                    # If both Python converters fail, fall back to the C++ converter 
                    try: 
                        subprocess.run(['converters/final_js2py.exe', 'samples/sample.js', 'output/output.py'], check=True) 
                    except subprocess.CalledProcessError: 
                        # All converters failed 
                        self.send_response(500) 
                        self.send_header('Content-type', 'application/json') 
                        self.send_header('Access-Control-Allow-Origin', '*') 
                        self.end_headers() 
                        self.wfile.write(json.dumps({'success': False, 'error': 'All converters failed'}).encode()) 
                        return 
 
            # Send response 
            self.send_response(200) 
            self.send_header('Content-type', 'application/json') 
            self.send_header('Access-Control-Allow-Origin', '*') 
            self.end_headers() 
            self.wfile.write(json.dumps({'success': True}).encode()) 
 
    def do_GET(self): 
        if self.path == '/getOutput': 
            try: 
                with open('output/output.py', 'r') as f: 
                    py_code = f.read() 
 
                self.send_response(200) 
                self.send_header('Content-type', 'application/json') 
                self.send_header('Access-Control-Allow-Origin', '*') 
                self.end_headers() 
                self.wfile.write(json.dumps({'success': True, 'code': py_code}).encode()) 
            except FileNotFoundError: 
                self.send_response(404) 
                self.send_header('Content-type', 'application/json') 
                self.send_header('Access-Control-Allow-Origin', '*') 
                self.end_headers() 
                self.wfile.write(json.dumps({'success': False, 'error': 'Output file not found'}).encode()) 
        else: 
            super().do_GET() 
 
print(f"Starting server at http://localhost:{PORT}") 
print("Press Ctrl+C to stop the server") 
with socketserver.TCPServer(("", PORT), JSPyHandler) as httpd: 
    try: 
        httpd.serve_forever() 
    except KeyboardInterrupt: 
        print("Server stopped") 
