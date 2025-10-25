import http.server
import socketserver
import json
import os
import urllib.request

PORT = 8000
API_KEY = "YOUR_OPENAI_API_KEY"

class ChatHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/chat':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            user_message = data.get('message', '')

            # Send request to OpenAI API
            payload = {
                "model": "gpt-4o-mini",  # or gpt-4/gpt-5 if available
                "messages": [{"role": "user", "content": user_message}]
            }

            req = urllib.request.Request(
                "https://api.openai.com/v1/chat/completions",
                data=json.dumps(payload).encode('utf-8'),
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {API_KEY}"
                }
            )

            with urllib.request.urlopen(req) as response:
                res_data = json.loads(response.read().decode('utf-8'))
                reply = res_data["choices"][0]["message"]["content"]

            # Return reply to frontend
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"reply": reply}).encode('utf-8'))
        else:
            super().do_GET()

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    print(f"Server running at http://localhost:{PORT}")
    with socketserver.TCPServer(("", PORT), ChatHandler) as httpd:
        httpd.serve_forever()
