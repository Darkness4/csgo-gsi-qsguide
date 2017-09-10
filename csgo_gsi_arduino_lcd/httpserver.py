# -*- coding: utf-8 -*-
"""
HTTP server Thread.

@auteur: tsuriga, Darkness4
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
from json import loads
from .getinfo import get_bomb, get_round_phase, get_state
from .progress import bombtimer, playerstats, sleep


class MyServer(HTTPServer):
    """Server storing CSGO's information."""

    def init_state(self):
        """You can store states over multiple requests in the server."""
        self.round_phase = None
        self.bomb = None
        self.state = None
        self.waiting = False


class MyRequestHandler(BaseHTTPRequestHandler):
    """CSGO's requests handler."""

    ser_arduino = None

    def do_POST(self):
        """Receive CSGO's informations."""
        length = int(self.headers['Content-Length'])
        body = self.rfile.read(length).decode('utf-8')

        self.parse_payload(loads(body), self.ser_arduino)

        self.send_header('Content-type', 'text/html')
        self.send_response(200)
        self.end_headers()

    # Parsing and actions
    def parse_payload(self, payload, ser_arduino):
        """Search payload and execute arduino's codes."""
        round_phase = get_round_phase(payload)

        if round_phase is not None:
            bomb = get_bomb(payload)
            if bomb == 'planted':
                if bomb != self.server.bomb:
                    self.server.bomb = bomb
                    bombtimer(ser_arduino)
            else:
                self.server.bomb = bomb

            state = get_state(payload)
            if state != self.server.state:  # if the state has changed
                self.server.state = state  # Gather player's state
                # Progress bar HP AM
                health = int(state['health'])  # Health
                armor = int(state['armor'])  # Armor
                playerstats(ser_arduino, health, armor)
                # Wait for second line
                sleep(0.1)
                # Kill or Money
                if round_phase != 'freezetime':
                    # HS and Kill counter
                    headshots = int(state['round_killhs'])
                    kills = state['round_kills'] - headshots
                    ser_arduino.write(b'K: ')
                    for _ in range(0, kills):  # counting
                        ser_arduino.write(b'\x00')  # Byte 0 char : kill no HS
                    for _ in range(0, headshots):  # counting
                        ser_arduino.write(b'\x01')  # Byte 1 char : HS
                else:  # Not kill streak
                    ser_arduino.write(
                        bytes('M: {}'.format(state['money']).encode()))
        elif not self.server.waiting:
            self.server.waiting = True  # isWaiting
            ser_arduino.write(b'Waiting for')
            sleep(0.1)
            ser_arduino.write(b'matches')

    def log_message(self, format, *args):
        """Prevents requests from printing into the console."""
        return
