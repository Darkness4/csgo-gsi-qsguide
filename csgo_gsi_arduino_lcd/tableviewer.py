# -*- coding: utf-8 -*-
"""
Payload printer.

@auteur: Darkness4
"""

from json import dumps
from threading import Thread


class PayloadViewerThread(Thread):
    """
    Payload Viewer.

    Attributes
    ----------
    __payload : dict
        Payload from CSGO.
    refreshable : bool
        Can be refreshed.
    running : bool
        Order to run.


    Methods
    -------
    run()
        Start the Thread and run Payload Viewer.
    shutdown()
        Shutdown the Payload Viewer.
    refresh()
        Order to refresh the Payload.
    """

    running = True  # Order to start/stop
    refreshable = False
    __payload = None

    def __init__(self) -> None:
        """Start thread."""
        super(PayloadViewerThread, self).__init__()

    def run(self) -> None:
        """Print payload."""
        while self.running:
            if self.refreshable:
                print(dumps(self.payload, indent=4))
                self.refreshable = False

    def shutdown(self) -> None:
        """Shutdown thread."""
        self.running = False

    @property
    def payload(self) -> dict:
        """Get the payload."""
        return self.__payload

    @payload.setter
    def payload(self, payload: dict) -> None:
        """Set the payload."""
        self.__payload = payload

    def refresh(self) -> None:
        """Refresh."""
        self.refreshable = True
