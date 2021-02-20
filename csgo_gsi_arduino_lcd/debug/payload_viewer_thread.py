# -*- coding: utf-8 -*-
"""
Payload printer.

@auteur: Darkness4
"""

import json
import logging
from threading import Thread
from typing import Any, Dict, Optional


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
    payload: Optional[Dict[str, Any]] = None
    __pause = True

    def __init__(self):
        """Start thread."""
        super(PayloadViewerThread, self).__init__()

    def run(self):
        """Print payload."""
        while self.running:
            if not self.__pause:
                if self.refreshable:
                    logging.debug(json.dumps(self.payload, indent=2))
                    self.refreshable = False

    def shutdown(self):
        """Shutdown thread."""
        self.running = False

    def pause(self):
        self.__pause = True

    def resume(self):
        self.__pause = False

    def refresh(self):
        """Refresh."""
        self.refreshable = True
