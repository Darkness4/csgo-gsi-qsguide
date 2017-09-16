# -*- coding: utf-8 -*-
"""
Payload printer.

@auteur: Darkness4
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
from json import loads, dumps


class MyRequestHandler(BaseHTTPRequestHandler):
    """CSGO's requests handler."""

    def do_POST(self):
        """Receive CSGO's informations."""
        length = int(self.headers['Content-Length'])
        body = self.rfile.read(length).decode('utf-8')

        self.parse_payload(loads(body))

        self.send_header('Content-type', 'text/html')
        self.send_response(200)
        self.end_headers()

    # Parsing and actions
    def parse_payload(self, payload):
        """Search payload."""
        if self.server.payload != payload:
            self.server.payload = payload
            print(dumps(payload, indent=4))

    def log_message(self, format, *args):
        """Prevents requests from printing into the console."""
        return


class MyServer(HTTPServer):
    """Server storing CSGO's information."""

    payload = None


server = MyServer(('localhost', 3000), MyRequestHandler)

try:
    server.serve_forever()
except (KeyboardInterrupt, SystemExit):
    pass

server.server_close()
