#!/usr/bin/env python
# Solution contributed by Filip Kasic

from http.server import BaseHTTPRequestHandler, HTTPServer
import time

class CustomHttpServer(BaseHTTPRequestHandler):
    def do_GET(self):
        """
        Handling of GET requests
        :return:
        """
        if self.path == '/example':
            with open('example.html', 'rb') as file:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(file.read())
                file.close()
                return
        else:
            self.send_error(404, 'Not found')


if __name__ == "__main__":
    ws = HTTPServer(("127.0.0.1", 8080), CustomHttpServer)
    print(f"Started server on port 8080")

    try:
        ws.serve_forever()
    except KeyboardInterrupt:
        pass

    ws.server_close()

