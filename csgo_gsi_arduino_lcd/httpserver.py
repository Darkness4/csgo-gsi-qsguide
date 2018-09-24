# -*- coding: utf-8 -*-
"""
HTTP server Thread.

@auteur: tsuriga, Darkness4
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
from json import loads
from time import asctime
from .messenger import Messenger


class MyServer(HTTPServer):
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
        super(MyServer, self).__init__(*args, **kwargs)
        self.round_phase = None
        self.bomb = None
        self.state = None
        self.is_waiting = False
        self.payloadviewer = None
        self.ser_arduino = ser_arduino
        self.messenger = Messenger(ser_arduino)
        self.messenger.start()
        print(asctime(), '-', "Messenger is online.")


class MyRequestHandler(BaseHTTPRequestHandler):
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
                    self.server.messenger.change_status("Bomb")
                elif bomb == 'defused':
                    self.server.messenger.change_status("Defused")
                elif bomb == 'exploded':
                    self.server.messenger.change_status("Exploded")
                else:
                    self.server.messenger.change_status("None")
            elif state != self.server.state:  # if the state has changed
                self.server.messenger.change_status("!Freezetime")
                self.server.state = state  # Gather player's state
                # Progress bar HP AM
                self.server.messenger.health = int(state['health'])
                self.server.messenger.armor = int(state['armor'])
                self.server.messenger.money = int(state['money'])
                self.server.messenger.set_kills(state['round_kills'],
                                                state['round_killhs'])
                if round_phase != 'freezetime':
                    self.server.messenger.change_status("!Freezetime")
                else:  # Not kill streak
                    self.server.messenger.change_status("Freezetime")
        elif not self.server.is_waiting:
            self.server.is_waiting = True  # is_waiting
            self.server.messenger.change_status("None")

        #  Start the payload viewer
        if self.server.payloadviewer is not None \
           and payload != self.server.payloadviewer.payload:
            self.server.payloadviewer.set_payload(payload)
            self.server.payloadviewer.refresh()

    def log_message(self, format, *args) -> None:
        """Prevent requests from printing into the console."""
        return
