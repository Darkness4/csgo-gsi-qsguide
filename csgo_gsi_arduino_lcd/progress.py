# -*- coding: utf-8 -*-
"""
Processing functions.

@auteur: Darkness4
"""
from time import time, sleep


def progress(i):
    """Progress bar, for arduino 5px large."""
    switcher = {i <= 0: b"\x07",
                i == 1: b"\x02",
                i == 2: b"\x03",
                i == 3: b"\x04",
                i == 4: b"\x05",
                i >= 5: b"\x06"}
    return switcher[True]


def bombtimer(ser_arduino):
    """40s bomb timer on arduino."""
    offset = time()
    actualtime = 40 - time() + offset
    while actualtime > 0:
        oldtime = int(actualtime)
        sleep(0.1)
        actualtime = 40 - time() + offset
        if oldtime != int(actualtime):  # Actualization
            ser_arduino.write(b'BOMB PLANTED')
            # Wait for second line
            sleep(0.1)
            ser_arduino.write(progress(int(actualtime)))  # 5s max
            ser_arduino.write(progress(int(actualtime - 5)))  # 10s max
            ser_arduino.write(progress(int(actualtime - 10)))  # 15s max
            ser_arduino.write(progress(int(actualtime - 15)))  # 20s max
            ser_arduino.write(progress(int(actualtime - 20)))  # 25s max
            ser_arduino.write(progress(int(actualtime - 25)))
            ser_arduino.write(progress(int(actualtime - 30)))
            ser_arduino.write(progress(int(actualtime - 35)))
            ser_arduino.write(bytes(str(int(actualtime)).encode()))
    return


def playerstats(ser_arduino, health, armor):
    """Player's stats writer."""
    ser_arduino.write(b'H: ')  # Writing progress bar on Serial
    ser_arduino.write(progress(int(health / 5)))
    ser_arduino.write(progress(int((health - 25) / 5)))
    ser_arduino.write(progress(int((health - 50) / 5)))
    ser_arduino.write(progress(int((health - 75) / 5)))
    ser_arduino.write(b' A: ')
    ser_arduino.write(progress(int(armor / 5)))
    ser_arduino.write(progress(int((armor - 25) / 5)))
    ser_arduino.write(progress(int((armor - 50) / 5)))
    ser_arduino.write(progress(int((armor - 75) / 5)))
