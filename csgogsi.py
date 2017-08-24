# -*- coding: utf-8 -*-
"""
CSGO's informations displayed on an Arduino featuring a bomb timer.

@auteur: tsuriga, Darkness4
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
from sys import exit, argv, platform
from time import time, sleep, asctime
from json import loads
from glob import glob
import getinfo
from serial import Serial, SerialException
from qtpy.QtWidgets import (QPushButton, QApplication, QComboBox,
                            QVBoxLayout, QHBoxLayout, QWidget)
from qtpy.QtCore import Slot, QThread, Qt
from qtpy.QtGui import QIcon


def progress(i):
    """ Progress bar, for arduino 5px large"""
    switcher = {i <= 0: b"\x07",
                i == 1: b"\x02",
                i == 2: b"\x03",
                i == 3: b"\x04",
                i == 4: b"\x05",
                i >= 5: b"\x06"}
    return switcher[True]


def bombtimer(ser_arduino):
    "40s bomb timer on arduino"
    offset = time()
    actualtime = 40-time() + offset
    while actualtime > 0:
        oldtime = int(actualtime)
        sleep(0.1)
        actualtime = 40 - time() + offset
        if oldtime != int(actualtime):  # Actualization
            ser_arduino.write(b'BOMB PLANTED')
            # Wait for second line
            sleep(0.1)
            ser_arduino.write(progress(int(actualtime)))  # 5s max
            ser_arduino.write(progress(int(actualtime-5)))  # 10s max
            ser_arduino.write(progress(int(actualtime-10)))  # 15s max
            ser_arduino.write(progress(int(actualtime-15)))  # 20s max
            ser_arduino.write(progress(int(actualtime-20)))  # 25s max
            ser_arduino.write(progress(int(actualtime-25)))
            ser_arduino.write(progress(int(actualtime-30)))
            ser_arduino.write(progress(int(actualtime-35)))
            ser_arduino.write(bytes(str(int(actualtime)).encode()))
    return


def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif platform.startswith('linux') or platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob('/dev/tty[A-Za-z]*')
    elif platform.startswith('darwin'):
        ports = glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            connect = Serial(port)
            connect.close()
            result.append(port)
        except (OSError, SerialException):
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
    ser_arduino = None

    def do_POST(self):
        """Receive CSGO's informations"""
        length = int(self.headers['Content-Length'])
        body = self.rfile.read(length).decode('utf-8')

        self.parse_payload(loads(body), self.ser_arduino)

        self.send_header('Content-type', 'text/html')
        self.send_response(200)
        self.end_headers()

    # Parsing and actions
    def parse_payload(self, payload, ser_arduino):
        """ Search payload and execute arduino's codes"""
        round_phase = getinfo.get_round_phase(payload)

        if round_phase is not None:
            bomb = getinfo.get_bomb(payload)
            if bomb == 'planted':
                if bomb != self.server.bomb:
                    self.server.bomb = bomb
                    bombtimer(ser_arduino)
            else:
                self.server.bomb = bomb

            state = getinfo.get_state(payload)
            if state != self.server.state:  # if the state has changed
                self.server.state = state  # Gather player's state
                # Progress bar HP AM
                health = int(state['health'])  # Health
                armor = int(state['armor'])  # Armor
                ser_arduino.write(b'H: ')  # Writing progress bar on Serial
                ser_arduino.write(progress(int(health/5)))
                ser_arduino.write(progress(int((health-25)/5)))
                ser_arduino.write(progress(int((health-50)/5)))
                ser_arduino.write(progress(int((health-75)/5)))
                ser_arduino.write(b' A: ')
                ser_arduino.write(progress(int(armor/5)))
                ser_arduino.write(progress(int((armor-25)/5)))
                ser_arduino.write(progress(int((armor-50)/5)))
                ser_arduino.write(progress(int((armor-75)/5)))
                # Wait for second line
                sleep(0.1)
                # Kill or Money
                if round_phase != 'freezetime':
                    # HS and Kill counter
                    headshots = int(state['round_killhs'])
                    kills = state['round_kills']-headshots
                    ser_arduino.write(b'K: ')
                    for _ in range(0, kills):  # counting
                        ser_arduino.write(b'\x00')  # Byte 0 char : kill no HS
                    for _ in range(0, headshots):  # counting
                        ser_arduino.write(b'\x01')  # Byte 1 char : HS
                else:  # Not kill streak
                    ser_arduino.write(bytes('M: {}'.format(state['money']).encode()))
        elif not self.server.waiting:
            self.server.waiting = True  # isWaiting
            ser_arduino.write(b'Waiting for')
            sleep(0.1)
            ser_arduino.write(b'matches')

    def log_message(self, format, *args):
        """
        Prevents requests from printing into the console
        """
        return


class ServerThread(QThread):
    """Server's thread"""
    def __init__(self, com_str):
        QThread.__init__(self)
        self.com_str = com_str

    def run(self):
        """Start the server"""
        self.ser_arduino = Serial(self.com_str, 9600)
        sleep(2)
        print(asctime(), '-', "Arduino detected")
        MyRequestHandler.ser_arduino = self.ser_arduino
        self.server = MyServer(('localhost', 3000), MyRequestHandler)
        self.server.init_state()
        print(asctime(), '-', 'CS:GO GSI Quick Start server starting')
        self.server.serve_forever()
        self.server.server_close()
        self.ser_arduino.close()
        print(asctime(), '-', 'CS:GO GSI Quick Start server stopped')
        print(asctime(), '-', 'Serial stopped')


class Csgogsi(QWidget):
    """App UI"""
    def __init__(self, parent=None):
        super(Csgogsi, self).__init__(parent)
        # Widgets
        self.connectbtn = QPushButton('Connect')
        self.connectbtn.clicked.connect(self.connect)

        self.comcb = QComboBox()
        self.comcb.addItems(serial_ports())
        if serial_ports() == []:
            self.connectbtn.setDisabled(True)
        else:
            self.connectbtn.setDisabled(False)

        self.refreshbtn = QPushButton('Refresh')
        self.refreshbtn.resize(self.refreshbtn.sizeHint())
        self.refreshbtn.clicked.connect(self.refresh)

        # Window
        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        vbox.addStretch(1)
        hbox.addWidget(self.comcb)
        hbox.addWidget(self.refreshbtn)
        vbox.addLayout(hbox)
        vbox.addWidget(self.connectbtn)
        self.setLayout(vbox)
        self.setWindowIcon(QIcon('csgo-icon-42854-16x16.ico'))
        self.setWindowTitle('CSGO GSI on LCD')
        self.setFixedSize(200, 75)
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.show()

    @Slot()
    def refresh(self):
        """Refresh COM ports"""
        self.comcb.clear()
        self.comcb.addItems(serial_ports())
        if serial_ports() == []:
            self.connectbtn.setDisabled(True)
        else:
            self.connectbtn.setDisabled(False)

    @Slot()
    def connect(self):
        """Connect to the server"""
        self.comcb.setDisabled(True)
        self.connectbtn.setDisabled(True)
        self.refreshbtn.setDisabled(True)
        self.serverthread = ServerThread(str(self.comcb.currentText()))
        self.serverthread.start()
        self.connectbtn.clicked.disconnect()
        self.connectbtn.clicked.connect(self.stop)
        self.connectbtn.setDisabled(False)
        self.connectbtn.setText('Stop')

    @Slot()
    def stop(self):
        """Stop the server"""
        self.serverthread.server.shutdown()
        self.serverthread.wait()
        self.serverthread.quit()
        self.connectbtn.clicked.disconnect()
        self.connectbtn.clicked.connect(self.connect)
        self.connectbtn.setText('Connect')
        self.comcb.setDisabled(False)
        self.connectbtn.setDisabled(False)
        self.refreshbtn.setDisabled(False)


if __name__ == '__main__':
    APP = QApplication(argv)
    EX = Csgogsi()
    exit(APP.exec_())
