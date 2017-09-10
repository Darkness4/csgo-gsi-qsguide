# -*- coding: utf-8 -*-
"""
Server Thread.

@auteur: Darkness4
"""

from time import asctime, sleep
from serial import Serial
from .httpserver import MyServer, MyRequestHandler
from qtpy.QtCore import QThread


class ServerThread(QThread):
    """Server's thread."""

    def __init__(self, com_str):
        """Start thread and save the COM port."""
        QThread.__init__(self)
        self.com_str = com_str

    def run(self):
        """Start the server."""
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
