#!/usr/bin/env python3
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler

PORT = 8000

if __name__ == '__main__':
    server = ThreadingHTTPServer(('0.0.0.0', PORT), SimpleHTTPRequestHandler)
    print(f'Open http://localhost:{PORT}/web/index.html')
    server.serve_forever()
