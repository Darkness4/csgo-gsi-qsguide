from http.server import BaseHTTPRequestHandler
from json import loads
from typing import Optional

from csgo_gsi_arduino_lcd.data.arduino_mediator import ArduinoMediator
from csgo_gsi_arduino_lcd.debug.payload_viewer_thread import (
    PayloadViewerThread,
)
from csgo_gsi_arduino_lcd.entities.state import State
from csgo_gsi_arduino_lcd.entities.status import Status


class CsgoRequestHandler(BaseHTTPRequestHandler):
    """CSGO's requests handler."""

    is_waiting: bool = False
    payload_viewer: PayloadViewerThread
    arduino: ArduinoMediator

    def __init__(
        self,
        arduino_mediator: ArduinoMediator,
        payload_viewer: PayloadViewerThread,
        *args,
        **kwargs
    ):
        super(CsgoRequestHandler, self).__init__(*args, **kwargs)
        self.arduino = arduino_mediator
        self.payload_viewer = payload_viewer

    def do_POST(self):
        """Receive CSGO's informations."""
        length = int(self.headers["Content-Length"])
        body = self.rfile.read(length).decode("utf-8")

        self.parse_payload(loads(body))

        self.send_header("Content-type", "text/html")
        self.send_response(200)
        self.end_headers()

    # Parsing and actions
    def parse_payload(
        self,
        payload: dict,
    ):
        """
        Search payload and execute arduino's codes.

        Parameters
        ----------
        payload : dict
            Payload containing all CSGO's informations.

        """
        round_phase = payload["round"]["phase"]

        if round_phase is not None:
            self.is_waiting = False
            state: Optional[State] = None
            state = State.from_dict(payload["player"]["state"])
            self.arduino.status = Status.from_bomb_dict(
                payload["round"]["bomb"]
            )

            if state != self.arduino.state:  # if the state has changed
                self.arduino.status = Status.NOT_FREEZETIME
                # Progress bar HP AM
                self.arduino.state = state

                if round_phase != "freezetime":
                    self.arduino.status = Status.NOT_FREEZETIME
                else:  # Not kill streak
                    self.arduino.status = Status.FREEZETIME
        elif not self.is_waiting:
            self.is_waiting = True  # is_waiting
            self.arduino.status = Status.NONE

        #  Start the payload viewer
        if payload != self.payload_viewer.payload:
            self.payload_viewer.payload = payload
            self.payload_viewer.refresh()
