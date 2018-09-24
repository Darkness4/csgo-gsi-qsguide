# -*- coding: utf-8 -*-
"""
Payload printer.

@auteur: Darkness4
"""

from json import dumps
from threading import Thread


class PayloadViewerThread(Thread):
    """CSGO's requests handler."""

    __start = True  # Order to start/stop
    __refresh = False
    payload = None

    def __init__(self):
        """Start thread."""
        super(PayloadViewerThread, self).__init__()

    def run(self):
        """Print payload."""
        while self.__start:
            if self.__refresh:
                print(dumps(self.payload, indent=4))
                self.__refresh = False

    def shutdown(self):
        """Shutdown thread."""
        self.__start = False

    def set_payload(self, payload):
        """Update payload."""
        self.payload = payload

    def refresh(self):
        """Refresh."""
        self.__refresh = True
