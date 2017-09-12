# -*- coding: utf-8 -*-
"""
CSGO's informations displayed on an Arduino featuring a bomb timer.

@auteur: tsuriga, Darkness4
"""

__title__ = "csgo-gsi-arduino-lcd"
__version__ = "1.4.0"
__project_url__ = 'https://github.com/Darkness4/csgo-gsi-arduino-lcd'
__credits__ = ["tsuriga", "Darkness4"]

print(__title__+" "+__version__)
from sys import argv
from qtpy.QtWidgets import QApplication

from csgo_gsi_arduino_lcd.appUI import Csgogsi
from csgo_gsi_arduino_lcd.main import main
