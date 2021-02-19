# -*- coding: utf-8 -*-
"""
Server Thread.

@auteur: Darkness4
"""

import logging
from http.server import HTTPServer

from csgo_gsi_arduino_lcd.data.arduino_mediator import ArduinoMediator
from csgo_gsi_arduino_lcd.data.csgo_request_handler import CsgoRequestHandler
from csgo_gsi_arduino_lcd.debug.payload_viewer_thread import (
    PayloadViewerThread,
)
from qtpy.QtCore import QThread
from serial import Serial


class ServerThread(QThread):
    """Server thread."""

    payload_viewer = PayloadViewerThread()
    arduino_mediator: ArduinoMediator
    server: HTTPServer
    ser_arduino: Serial

    def __init__(self, com_str: str):
        """Start thread and save the COM port."""
        QThread.__init__(self)
        self.com_str = com_str
        self.ser_arduino = Serial(self.com_str, 9600)
        logging.info("Arduino detected")

        # Launch mediator
        self.arduino_mediator = ArduinoMediator(self.ser_arduino)
        self.arduino_mediator.start()
        logging.info("Arduino Mediator started")

        handler = CsgoRequestHandler.create(
            self.arduino_mediator,
            self.payload_viewer,
        )
        self.server = HTTPServer(("localhost", 3000), handler)

    def run(self):
        """Start the server."""
        logging.info("CS:GO GSI Quick Start server starting")
        self.server.serve_forever()
        logging.info("CS:GO GSI Quick Start server stopped")
        self.ser_arduino.close()
        logging.info("Serial stopped")
