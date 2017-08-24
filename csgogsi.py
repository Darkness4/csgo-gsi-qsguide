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
from PyQt5.QtWidgets import (QWidget, QPushButton, QApplication, QComboBox,
                             QVBoxLayout)
from PyQt5.QtCore import pyqtSlot, QThread


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
                self.server.state = state  # Gather player's state
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


class ServerThread(QThread):
    def __init__(self, COM_STR):
        QThread.__init__(self)
        self.COM_STR = COM_STR

    def run(self):
        global S
        self.S = serial.Serial(self.COM_STR, 9600)
        time.sleep(2)
        print(time.asctime(), '-', "Arduino detected")
        self.SERVER = MyServer(('localhost', 3000), MyRequestHandler)
        self.SERVER.init_state()
        print(time.asctime(), '-', 'CS:GO GSI Quick Start server starting')
        self.SERVER.serve_forever()
        self.SERVER.server_close()
        self.S.close()
        print(time.asctime(), '-', 'CS:GO GSI Quick Start server stopped')
        print(time.asctime(), '-', 'Serial stopped')


class Csgogsi(QWidget):
    def __init__(self, parent=None):
        super(Csgogsi, self).__init__(parent)
        # Widgets
        self.connectbtn = QPushButton('Connect')
        self.connectbtn.clicked.connect(self.connect)

        self.cb = QComboBox()
        self.cb.addItems(serial_ports())
        if serial_ports() == []:
            self.connectbtn.setDisabled(True)
        else:
            self.connectbtn.setDisabled(False)

        self.refreshbtn = QPushButton('Refresh')
        self.refreshbtn.resize(self.refreshbtn.sizeHint())
        self.refreshbtn.clicked.connect(self.refresh)

        # Window
        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addWidget(self.refreshbtn)
        vbox.addWidget(self.cb)
        vbox.addWidget(self.connectbtn)
        self.setLayout(vbox)
        self.setWindowTitle('CSGO GSI on LCD')
        self.setFixedSize(97, 100)
        self.show()

    @pyqtSlot()
    def refresh(self):
        self.cb.clear()
        self.cb.addItems(serial_ports())
        if serial_ports() == []:
            self.connectbtn.setDisabled(True)
        else:
            self.connectbtn.setDisabled(False)

    @pyqtSlot()
    def connect(self):
        self.cb.setDisabled(True)
        self.connectbtn.setDisabled(True)
        self.refreshbtn.setDisabled(True)
        self.server = ServerThread(str(self.cb.currentText()))
        self.server.start()
        self.connectbtn.clicked.disconnect()
        self.connectbtn.clicked.connect(self.stop)
        self.connectbtn.setDisabled(False)
        self.connectbtn.setText('Stop')

    @pyqtSlot()
    def stop(self):
        self.server.SERVER.shutdown()
        self.server.quit()
        self.connectbtn.clicked.disconnect()
        self.connectbtn.clicked.connect(self.connect)
        self.connectbtn.setText('Connect')
        self.cb.setDisabled(False)
        self.connectbtn.setDisabled(False)
        self.refreshbtn.setDisabled(False)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Csgogsi()
    sys.exit(app.exec_())
