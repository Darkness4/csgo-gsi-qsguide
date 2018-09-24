# -*- coding: utf-8 -*-
"""
HTTP server Thread.

@auteur: tsuriga, Darkness4
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
from json import loads
from time import asctime
from .messenger import Messenger


class HTTPCSGOServer(HTTPServer):
    """Server storing CSGO's information."""
    def __init__(self, ser_arduino, *args, **kwargs) -> None:
        """
        You can store states over multiple requests in the server.

        Parameters
        ----------
        ser_arduino : Serial
            Arduino in Serial.

        """
        # HTTPServer.__init__(self, *args, **kwargs)
        super(HTTPCSGOServer, self).__init__(*args, **kwargs)
        self.round_phase = None
        self.bomb = None
        self.state = None
        self.is_waiting = False
        self.payload_viewer = None
        self.ser_arduino = ser_arduino
        self.messenger = Messenger(ser_arduino)
        self.messenger.start()
        print(asctime(), '-', "Messenger is online.")


class CSGORequestHandler(BaseHTTPRequestHandler):
    """
    CSGO's requests handler.

    Methods
    -------
    do_POST()
        Receive CSGO's informations.
    parse_payload(payload: dict)
        Search payload and execute arduino's codes.
    log_message(self, format, *args)
        Prevent requests from printing into the console.

    """

    def do_POST(self):
        """Receive CSGO's informations."""
        length = int(self.headers['Content-Length'])
        body = self.rfile.read(length).decode('utf-8')

        self.parse_payload(loads(body))

        self.send_header('Content-type', 'text/html')
        self.send_response(200)
        self.end_headers()

    # Parsing and actions
    def parse_payload(self, payload: dict) -> None:
        """
        Search payload and execute arduino's codes.

        Parameters
        ----------
        payload : dict
            Payload containing all CSGO's informations.

        """
        round_phase = None
        if 'round' in payload and 'phase' in payload['round']:
            round_phase = payload['round']['phase']

        if round_phase is not None:
            self.server.is_waiting = False
            bomb = None
            state = None

            if 'round' in payload and 'bomb' in payload['round']:
                bomb = payload['round']['bomb']

            if 'player' in payload and 'state' in payload['player']:
                state = {'health': payload['player']['state']['health'],
                         'armor': payload['player']['state']['armor'],
                         'round_kills': payload['player']['state']['round_kills'],
                         'round_killhs': payload['player']['state']['round_killhs'],
                         'money': payload['player']['state']['money']}

            if bomb != self.server.bomb:
                self.server.bomb = bomb
                if bomb == 'planted':
                    self.server.messenger.status = "Bomb"
                elif bomb == 'defused':
                    self.server.messenger.status = "Defused"
                elif bomb == 'exploded':
                    self.server.messenger.status = "Exploded"
                else:
                    self.server.messenger.status = "None"
            elif state != self.server.state:  # if the state has changed
                self.server.messenger.status = "!Freezetime"
                self.server.state = state  # Gather player's state
                # Progress bar HP AM
                self.server.messenger.health = int(state['health'])
                self.server.messenger.armor = int(state['armor'])
                self.server.messenger.money = int(state['money'])
                self.server.messenger.kills = (state['round_kills'],
                                               state['round_killhs'])
                if round_phase != 'freezetime':
                    self.server.messenger.status = "!Freezetime"
                else:  # Not kill streak
                    self.server.messenger.status = "Freezetime"
        elif not self.server.is_waiting:
            self.server.is_waiting = True  # is_waiting
            self.server.messenger.status = "None"

        #  Start the payload viewer
        if self.server.payload_viewer is not None \
           and payload != self.server.payload_viewer.payload:
            self.server.payload_viewer.payload = payload
            self.server.payload_viewer.refresh()

    def log_message(self, format, *args) -> None:
        """Prevent requests from printing into the console."""
        return
