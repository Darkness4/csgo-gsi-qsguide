# -*- coding: utf-8 -*-
"""
Server Thread.

@auteur: Darkness4
"""

from time import asctime, sleep
from serial import Serial
from qtpy.QtCore import QThread
from .httpserver import MyServer, MyRequestHandler


class ServerThread(QThread):
    """Server's thread."""

    ser_arduino = None
    server = None

    def __init__(self, com_str):
        """Start thread and save the COM port."""
        QThread.__init__(self)
        self.com_str = com_str

    def run(self):
        """Start the server."""
        self.ser_arduino = Serial(self.com_str, 9600)
        sleep(2)  # Wait for arduino
        print(asctime(), '-', "Arduino detected")
        # Launch server
        self.server = MyServer(('localhost', 3000), MyRequestHandler)
        self.server.init_state(self.ser_arduino)  # Init var
        print(asctime(), '-', 'CS:GO GSI Quick Start server starting')
        self.server.serve_forever()  # Run
        self.server.server_close()  # Close server
        print(asctime(), '-', 'CS:GO GSI Quick Start server stopped')
        self.ser_arduino.close()  # Close COM port
        print(asctime(), '-', 'Serial stopped')
