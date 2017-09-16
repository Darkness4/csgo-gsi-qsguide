# -*- coding: utf-8 -*-
"""
Payload printer.

@auteur: Darkness4
"""

from json import dumps
from threading import Thread


class PayloadViewerThread(Thread):
    """CSGO's requests handler."""

    __start__ = True  # Order to start/stop
    __refresh__ = False
    payload = None

    def __init__(self):
        """Start thread."""
        super(PayloadViewerThread, self).__init__()

    def run(self):
        """Print payload."""
        while self.__start__:
            if self.__refresh__:
                print(dumps(self.payload, indent=4))
                self.__refresh__ = False

    def shutdown(self):
        """Shutdown thread."""
        self.__start__ = False

    def setpayload(self, payload):
        """Update payload."""
        self.payload = payload

    def refresh(self):
        """Refresh."""
        self.__refresh__ = True
