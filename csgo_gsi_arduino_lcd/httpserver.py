# -*- coding: utf-8 -*-
"""
HTTP server Thread.

@auteur: tsuriga, Darkness4
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
from json import loads
from time import asctime
from .getinfo import get_bomb, get_round_phase, get_state
from .messenger import Messenger


class MyServer(HTTPServer):
    """Server storing CSGO's information."""

    def init_state(self, ser_arduino):
        """You can store states over multiple requests in the server."""
        self.round_phase = None
        self.bomb = None
        self.state = None
        self.waiting = False
        self.payloadviewer = None
        self.ser_arduino = ser_arduino
        self.messenger = Messenger(ser_arduino)
        self.messenger.start()
        print(asctime(), '-', "Messenger is online.")


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
        """Search payload and execute arduino's codes."""
        round_phase = get_round_phase(payload)

        if round_phase is not None:
            self.server.waiting = False
            bomb = get_bomb(payload)
            state = get_state(payload)
            if bomb != self.server.bomb:
                if bomb == 'planted':
                    self.server.bomb = bomb
                    self.server.messenger.changestatus("Bomb")
                elif bomb == 'defused':
                    self.server.bomb = bomb
                    self.server.messenger.changestatus("Defused")
                elif bomb == 'exploded':
                    self.server.bomb = bomb
                    self.server.messenger.changestatus("Exploded")
            elif state != self.server.state:  # if the state has changed
                self.server.messenger.changestatus("!Freezetime")
                self.server.state = state  # Gather player's state
                # Progress bar HP AM
                self.server.messenger.health = int(state['health'])
                self.server.messenger.armor = int(state['armor'])
                self.server.messenger.money = int(state['money'])
                self.server.messenger.setkills(state['round_kills'],
                                               state['round_killhs'])
                if round_phase != 'freezetime':
                    self.server.messenger.changestatus("!Freezetime")
                else:  # Not kill streak
                    self.server.messenger.changestatus("Freezetime")
        elif not self.server.waiting:
            self.server.waiting = True  # isWaiting
            self.server.messenger.changestatus("None")

        #  Start the payload viewer
        if (self.server.payloadviewer is not None
           and payload != self.server.payloadviewer.payload):
            self.server.payloadviewer.setpayload(payload)
            self.server.payloadviewer.refresh()

    def log_message(self, format, *args):
        """Prevent requests from printing into the console."""
        return
