# -*- coding: utf-8 -*-
"""
Server Thread.

@auteur: Darkness4
"""

from time import asctime, sleep

from qtpy.QtCore import QThread
from serial import Serial

from .httpserver import CSGORequestHandler, HTTPCSGOServer


class ServerThread(QThread):
    """
    Server's thread.

    Attributes
    ----------
    com_str : str
        COM Port in str.
    ser_arduino : Serial
        Status of Messenger.
    server : Server
        Status of the refresher.

    Methods
    -------
    run()
        Start the Thread and run Server.

    """

    ser_arduino = None
    server = None

    def __init__(self, com_str) -> None:
        """Start thread and save the COM port."""
        QThread.__init__(self)
        self.com_str = com_str

    def run(self) -> None:
        """Start the server."""
        self.ser_arduino = Serial(self.com_str, 9600)
        sleep(2)  # Wait for arduino
        print(asctime(), '-', "Arduino detected")
        # Launch server
        self.server = HTTPCSGOServer(self.ser_arduino,
                                     ('localhost', 3000),
                                     CSGORequestHandler)
        print(asctime(), '-', 'CS:GO GSI Quick Start server starting')
        self.server.serve_forever()  # Run
        self.server.server_close()  # Close server
        print(asctime(), '-', 'CS:GO GSI Quick Start server stopped')
        self.ser_arduino.close()  # Close COM port
        print(asctime(), '-', 'Serial stopped')
