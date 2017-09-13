# -*- coding: utf-8 -*-
"""
CSGO's informations displayed on an Arduino featuring a bomb timer.

@auteur: tsuriga, Darkness4
"""

from sys import argv
from qtpy.QtWidgets import QApplication

from .appui import Csgogsi


def main():
    """Launch."""
    app = None
    app = QApplication(argv)
    ex = Csgogsi()
    app.exec_()
