# -*- coding: utf-8 -*-
"""
ArduinoMediator.

@auteur: Darkness4
"""
import logging
from threading import Thread
from time import sleep, time
from typing import Optional

from csgo_gsi_arduino_lcd.entities.state import State
from csgo_gsi_arduino_lcd.entities.status import Status
from serial import Serial


class ArduinoMediator(Thread):
    """Give order to the arduino."""

    state: Optional[State] = None
    __refresh = False  # Order to refresh informations
    __start = True  # Order to start/stop
    __status: Status = Status.NONE
    ser_arduino: Serial

    def __init__(self, ser_arduino: Serial):
        """Init save."""
        super(ArduinoMediator, self).__init__()
        self.ser_arduino = ser_arduino

    @property
    def status(self) -> Status:
        return self.__status

    @status.setter
    def status(self, status: Status):
        """Change Messenger behavior."""
        self.__status = status
        self.__refresh = True  # Informations need to be refreshed

    def run(self):
        """Thread start."""
        while self.__start:
            self.refresh() if self.__refresh else sleep(0.1)
        logging.info("Messenger is dead.")

    def refresh(self):
        self.__refresh = False
        # Has refreshed
        if self.__status in (
            Status.BOMB,
            Status.DEFUSED,
            Status.EXPLODED,
        ):  # Bomb
            self.draw_bomb_timer()
        elif self.__status == Status.NONE:
            self.draw_idling()
        else:  # Default status
            self.write_player_stats()

    def draw_bomb_timer(self):
        """40 sec bomb timer on arduino."""
        offset = time()
        actualtime: int = int(40 - time() + offset)
        while actualtime > 0 and self.__status == Status.BOMB:
            oldtime = actualtime
            sleep(0.1)
            actualtime = int(40 - time() + offset)
            if oldtime != actualtime:  # Actualization only integer change
                self.ser_arduino.write(b"BOMB PLANTED")
                # Wait for second line
                sleep(0.1)
                for i in range(0, 40, 5):
                    self.ser_arduino.write(
                        ArduinoMediator.progress(actualtime - i)
                    )
                self.ser_arduino.write(str(actualtime).encode())
                sleep(0.1)
        if self.__status == Status.DEFUSED:
            self.ser_arduino.write(b"BOMB DEFUSED")
            # Wait for second line
            sleep(0.1)
            self.ser_arduino.write(b" ")
            sleep(0.1)
        elif self.__status == Status.EXPLODED:
            self.ser_arduino.write(b"BOMB EXPLODED")
            # Wait for second line
            sleep(0.1)
            self.ser_arduino.write(b" ")
            sleep(0.1)

    def write_player_stats(self):
        """Player stats writer."""
        # Not too fast
        sleep(0.1)

        # Writing health and armor in Serial
        self.draw_health_and_armor()

        # Wait for second line
        sleep(0.1)

        # Kill or Money
        if self.__status == Status.NOT_FREEZETIME:
            self.draw_kills()
        elif self.__status == Status.FREEZETIME:
            self.draw_money()
        sleep(0.1)

    def draw_kills(self):
        """Show kills in one line."""
        # HS and Kill counter
        self.ser_arduino.write(b"K: ")
        for _ in range(
            self.state.round_kills - self.state.round_killhs
        ):  # counting
            self.ser_arduino.write(b"\x00")  # Byte 0 char : kill no HS
        for _ in range(self.state.round_killhs):  # counting
            self.ser_arduino.write(b"\x01")  # Byte 1 char : HS

    def draw_money(self):
        """Show money in one line."""
        self.ser_arduino.write(f"M: {self.state.money}".encode())

    def draw_health_and_armor(self):
        """Show health and armor in one line."""
        self.ser_arduino.write(b"H: ")
        self.ser_arduino.write(
            ArduinoMediator.progress(self.state.health // 5)
        )
        self.ser_arduino.write(
            ArduinoMediator.progress((self.state.health - 25) // 5)
        )
        self.ser_arduino.write(
            ArduinoMediator.progress((self.state.health - 50) // 5)
        )
        self.ser_arduino.write(
            ArduinoMediator.progress((self.state.health - 75) // 5)
        )
        self.ser_arduino.write(b" A: ")
        self.ser_arduino.write(ArduinoMediator.progress(self.state.armor // 5))
        self.ser_arduino.write(
            ArduinoMediator.progress((self.state.armor - 25) // 5)
        )
        self.ser_arduino.write(
            ArduinoMediator.progress((self.state.armor - 50) // 5)
        )
        self.ser_arduino.write(
            ArduinoMediator.progress((self.state.armor - 75) // 5)
        )

    def draw_idling(self):
        """Print text while idling."""
        self.ser_arduino.write(b"Waiting for")
        sleep(0.1)
        self.ser_arduino.write(b"matches")

    def shutdown(self):
        """Stop the mediator."""
        self.__start = False

    @staticmethod
    def progress(i: int) -> bytes:
        """
        Progress bar, for arduino 5px large.

        Parameters
        ----------
        i : int
            Select which character to send to Arduino.

        Returns
        -------
        bytes : Character send to Arduino.

        """
        if i <= 0:
            return b"\x07"
        elif 1 <= i <= 5:
            return bytes([i + 1])
        else:
            return b"\x06"
