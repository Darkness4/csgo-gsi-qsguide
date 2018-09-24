# -*- coding: utf-8 -*-
"""
Payload printer.

@auteur: Darkness4
"""

from json import dumps
from threading import Thread


class PayloadViewerThread(Thread):
    """CSGO's requests handler."""

    start = True  # Order to start/stop
    refreshing = False
    __payload = None

    def __init__(self) -> None:
        """Start thread."""
        super(PayloadViewerThread, self).__init__()

    def run(self) -> None:
        """Print payload."""
        while self.start:
            if self.refreshing:
                print(dumps(self.payload, indent=4))
                self.refreshing = False

    def shutdown(self) -> None:
        """Shutdown thread."""
        self.start = False

    @property
    def payload(self) -> dict:
        """Get the color."""
        return self.__payload

    @payload.setter
    def payload(self, payload: dict) -> None:
        """Set the payload."""
        self.__payload = payload

    def refresh(self) -> None:
        """Refresh."""
        self.refreshing = True
