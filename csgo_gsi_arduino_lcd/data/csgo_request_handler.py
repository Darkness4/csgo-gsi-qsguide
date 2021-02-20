import json
import logging
import socketserver
from functools import partial
from http.server import BaseHTTPRequestHandler
from typing import Any, Dict, Optional, Tuple

from csgo_gsi_arduino_lcd.data.arduino_mediator import ArduinoMediator
from csgo_gsi_arduino_lcd.data.data_store import DataStore
from csgo_gsi_arduino_lcd.entities.state import State
from csgo_gsi_arduino_lcd.entities.status import Status


class CsgoRequestHandler(BaseHTTPRequestHandler):
    """CSGO's requests handler."""

    is_waiting: bool = False
    arduino: ArduinoMediator
    data_store: DataStore
    last_data: Optional[Dict[str, Any]] = None

    @classmethod
    def create(cls, arduino_mediator: ArduinoMediator, data_store: DataStore):
        return partial(cls, arduino_mediator, data_store)

    def __init__(
        self,
        arduino_mediator: ArduinoMediator,
        request: bytes,
        client_address: Tuple[str, int],
        server: socketserver.BaseServer,
    ):
        super(CsgoRequestHandler, self).__init__(
            request, client_address, server
        )
        self.arduino = arduino_mediator

    def do_POST(self):
        """Receive CSGO's informations."""
        length = int(self.headers["Content-Length"])
        body = self.rfile.read(length).decode("utf-8")

        data = json.loads(body)
        self.parse_payload(data)
        self.data_store.data = data

        self.send_header("Content-type", "text/html")
        self.send_response(200)
        self.end_headers()

    # Parsing and actions
    def parse_payload(
        self,
        payload: Dict[str, Any],
    ):
        """
        Search payload and execute arduino's codes.

        Parameters
        ----------
        payload : dict
            Payload containing all CSGO's informations.

        """
        try:
            round_phase = payload["round"]["phase"]

            if round_phase is not None:
                self.is_waiting = False
                state = State.from_dict(payload["player"]["state"])
                self.arduino.status = Status.from_bomb_dict(
                    payload["round"]["bomb"]
                )

                if state != self.arduino.state:  # if the state has changed
                    self.arduino.status = Status.NOT_FREEZETIME
                    # Progress bar HP AM
                    self.arduino.state = state

                    self.arduino.status = Status.from_round_phase_dict(
                        round_phase
                    )
            elif not self.is_waiting:
                self.is_waiting = True
                self.arduino.status = Status.NONE
        except (KeyError, TypeError):
            logging.exception("Parsing incorrect")
