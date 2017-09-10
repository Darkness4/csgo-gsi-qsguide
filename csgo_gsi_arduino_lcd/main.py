# -*- coding: utf-8 -*-
"""
CSGO's informations displayed on an Arduino featuring a bomb timer.

@auteur: tsuriga, Darkness4
"""

from sys import argv
from qtpy.QtWidgets import QApplication

import csgo_gsi_arduino_lcd


def main():
    APP = None
    APP = QApplication(argv)
    EX = csgo_gsi_arduino_lcd.Csgogsi()
    APP.exec_()
