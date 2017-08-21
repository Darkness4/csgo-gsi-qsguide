# -*- coding: utf-8 -*-
"""
CSGO's informations displayed on an Arduino featuring a bomb timer.

@auteur: tsuriga, Darkness4
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
import sys
import time
import json
import glob
import serial


def progress(i):
    """ Progress bar, for arduino 5px large"""
    switcher = {i <= 0: b"\x07",
                i == 1: b"\x02",
                i == 2: b"\x03",
                i == 3: b"\x04",
                i == 4: b"\x05",
                i >= 5: b"\x06"}
    return switcher[True]


def bombtimer():
    "40s bomb timer on arduino"
    offset = time.time()
    actualtime = 40-time.time() + offset
    while actualtime > 0:
        oldtime = int(actualtime)
        time.sleep(0.1)
        actualtime = 40 - time.time() + offset
        if oldtime != int(actualtime):  # Actualization
            S.write(b'BOMB PLANTED')
            # Wait for second line
            time.sleep(0.1)
            S.write(progress(int(actualtime)))  # 5s max
            S.write(progress(int(actualtime-5)))  # 10s max
            S.write(progress(int(actualtime-10)))  # 15s max
            S.write(progress(int(actualtime-15)))  # 20s max
            S.write(progress(int(actualtime-20)))  # 25s max
            S.write(progress(int(actualtime-25)))
            S.write(progress(int(actualtime-30)))
            S.write(progress(int(actualtime-35)))
            S.write(bytes(str(int(actualtime)).encode()))
    return


def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            connect = serial.Serial(port)
            connect.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result


class MyServer(HTTPServer):
    """Server storing CSGO's information"""
    def init_state(self):
        """
        You can store states over multiple requests in the server
        """
        self.round_phase = None
        self.bomb = None
        self.state = None
        self.waiting = False


class MyRequestHandler(BaseHTTPRequestHandler):
    """CSGO's requests handler"""
    def do_POST(self):
        """Receive CSGO's informations"""
        length = int(self.headers['Content-Length'])
        body = self.rfile.read(length).decode('utf-8')

        self.parse_payload(json.loads(body))

        self.send_header('Content-type', 'text/html')
        self.send_response(200)
        self.end_headers()

    # Get Information function
    def get_round_phase(self, payload):
        """Get round phase"""
        if 'round' in payload and 'phase' in payload['round']:
            return payload['round']['phase']

    def get_state(self, payload):
        """Get player status"""
        if 'player' in payload and 'state' in payload['player']:
            return {'health': payload['player']['state']['health'],
                    'armor': payload['player']['state']['armor'],
                    'round_kills': payload['player']['state']['round_kills'],
                    'round_killhs': payload['player']['state']['round_killhs'],
                    'money': payload['player']['state']['money']}

    def get_bomb(self, payload):
        """Get bomb status"""
        if 'round' in payload and 'bomb' in payload['round']:
            return payload['round']['bomb']

    # Parsing and actions
    def parse_payload(self, payload):
        """ Search payload and execute arduino's codes"""
        round_phase = self.get_round_phase(payload)

        if round_phase is not None:
            bomb = self.get_bomb(payload)
            if bomb == 'planted':
                if bomb != self.server.bomb:
                    self.server.bomb = bomb
                    bombtimer()
            else:
                self.server.bomb = bomb

            state = self.get_state(payload)
            if state != self.server.state:  # if the state has changed
                self.server.state = state  # Récup des stats du joueurs
                # Progress bar HP AM
                health = int(state['health'])  # Health
                armor = int(state['armor'])  # Armor
                S.write(b'H: ')  # Writing progress bar on Serial
                S.write(progress(int(health/5)))
                S.write(progress(int((health-25)/5)))
                S.write(progress(int((health-50)/5)))
                S.write(progress(int((health-75)/5)))
                S.write(b' A: ')
                S.write(progress(int(armor/5)))
                S.write(progress(int((armor-25)/5)))
                S.write(progress(int((armor-50)/5)))
                S.write(progress(int((armor-75)/5)))
                # Wait for second line
                time.sleep(0.1)
                # Kill or Money
                if round_phase != 'freezetime':
                    # HS and Kill counter
                    headshots = int(state['round_killhs'])
                    kills = state['round_kills']-headshots
                    S.write(b'K: ')
                    for _ in range(0, kills):  # counting
                        S.write(b'\x00')  # Byte 0 char : kill no HS
                    for _ in range(0, headshots):  # counting
                        S.write(b'\x01')  # Byte 1 char : HS
                else:  # Not kill streak
                    S.write(bytes('M: {}'.format(state['money']).encode()))
        elif not self.server.waiting:
            self.server.waiting = True  # isWaiting
            S.write(b'Waiting for')
            time.sleep(0.1)
            S.write(b'matches')

    def log_message(self, format, *args):
        """
        Prevents requests from printing into the console
        """
        return

# Arduino connection
print("Ports availables : {}".format(serial_ports()))
COM_STR = input("Please enter the corresponding COMX : ")  # De la forme COMX
print("Waiting for Arduino")
while True:
    try:
        S = serial.Serial(COM_STR, 9600)
        break
    except IndexError:
        pass
print(time.asctime(), '-', "Arduino detected")
time.sleep(2)    # wait for the Serial to initialize

# Server initialization
SERVER = MyServer(('localhost', 3000), MyRequestHandler)
SERVER.init_state()

print(time.asctime(), '-', 'CS:GO GSI Quick Start server starting')

try:
    SERVER.serve_forever()
except (KeyboardInterrupt, SystemExit):
    pass

SERVER.server_close()
print(time.asctime(), '-', 'CS:GO GSI Quick Start server stopped')
print(time.asctime(), '-', 'Serial stopped')
S.close()
