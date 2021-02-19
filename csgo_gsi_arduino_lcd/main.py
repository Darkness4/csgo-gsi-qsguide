# -*- coding: utf-8 -*-
"""
CSGO's informations displayed on an Arduino featuring a bomb timer.

@auteur: tsuriga, Darkness4
"""

import sys

from qtpy.QtWidgets import QApplication

from csgo_gsi_arduino_lcd.ui.csgo_window import CsgoWindow


def main():
    global w
    app = QApplication(sys.argv)
    w = CsgoWindow()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
