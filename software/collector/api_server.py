from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os
from datetime import datetime

DATA_DIR = "data/raw"


class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)

        data = json.loads(body)

        os.makedirs(DATA_DIR, exist_ok=True)
        filename = datetime.now().strftime("%Y-%m-%d") + ".log"

        with open(os.path.join(DATA_DIR, filename), "a") as f:
            f.write(json.dumps(data) + "\n")

        print("Received:", data)

        self.send_response(200)
        self.end_headers()


def run():
    server = HTTPServer(("0.0.0.0", 5000), Handler)
    print("Server running on port 5000...")
    server.serve_forever()


if __name__ == "__main__":
    run()