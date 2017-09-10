# -*- coding: utf-8 -*-
"""
User interface.

@auteur: Darkness4
"""
from os.path import dirname, abspath
from serial.tools import list_ports
from qtpy.QtWidgets import (QPushButton, QComboBox,
                            QVBoxLayout, QHBoxLayout, QWidget)
from qtpy.QtCore import Slot, Qt, QSize
from qtpy.QtGui import QIcon
from .server import ServerThread
__dir__ = dirname(abspath(__file__))


def serial_ports():
    """List serial port names."""
    return [port.device for port in list_ports.comports()]


class Csgogsi(QWidget):
    """App UI."""

    def __init__(self, parent=None):
        """Init UI."""
        super(Csgogsi, self).__init__(parent)
        # Widgets
        self.connectbtn = QPushButton('Connect')
        self.connectbtn.clicked.connect(self.connect)

        self.comcb = QComboBox()
        self.comcb.addItems(serial_ports())
        if serial_ports() == []:
            self.connectbtn.setDisabled(True)
        else:
            self.connectbtn.setDisabled(False)

        self.refreshbtn = QPushButton('Refresh')
        self.refreshbtn.resize(self.refreshbtn.sizeHint())
        self.refreshbtn.clicked.connect(self.refresh)

        # Window
        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        vbox.addStretch(1)
        hbox.addWidget(self.comcb)
        hbox.addWidget(self.refreshbtn)
        vbox.addLayout(hbox)
        vbox.addWidget(self.connectbtn)
        self.setLayout(vbox)
        app_icon = QIcon()
        app_icon.addFile(
            __dir__+"\\..\\resources\\csgo-16.ico", QSize(16, 16))
        app_icon.addFile(
            __dir__+"\\..\\resources\\csgo-20.ico", QSize(20, 20))
        app_icon.addFile(
            __dir__+"\\..\\resources\\csgo-24.ico", QSize(24, 24))
        app_icon.addFile(
            __dir__+"\\..\\resources\\csgo-32.ico", QSize(32, 32))
        app_icon.addFile(
            __dir__+"\\..\\resources\\csgo-48.ico", QSize(48, 48))
        app_icon.addFile(
            __dir__+"\\..\\resources\\csgo-64.ico", QSize(64, 64))
        app_icon.addFile(
            __dir__+"\\..\\resources\\csgo-128.ico", QSize(128, 128))
        app_icon.addFile(
            __dir__+"\\..\\resources\\csgo-256.ico", QSize(256, 256))
        app_icon.addFile(
            __dir__+"\\..\\resources\\csgo-512.ico", QSize(512, 512))
        self.setWindowIcon(app_icon)
        self.setWindowTitle('CSGO GSI on LCD')
        self.setFixedSize(200, 75)
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.show()

    @Slot()
    def refresh(self):
        """Refresh COM ports."""
        self.comcb.clear()
        self.comcb.addItems(serial_ports())
        if serial_ports() == []:
            self.connectbtn.setDisabled(True)
        else:
            self.connectbtn.setDisabled(False)

    @Slot()
    def connect(self):
        """Connect to the server."""
        self.comcb.setDisabled(True)
        self.connectbtn.setDisabled(True)
        self.refreshbtn.setDisabled(True)
        self.serverthread = ServerThread(str(self.comcb.currentText()))
        self.serverthread.start()
        self.connectbtn.clicked.disconnect()
        self.connectbtn.clicked.connect(self.stop)
        self.connectbtn.setDisabled(False)
        self.connectbtn.setText('Stop')

    @Slot()
    def stop(self):
        """Stop the server."""
        self.serverthread.server.shutdown()
        self.serverthread.wait()
        self.serverthread.quit()
        self.connectbtn.clicked.disconnect()
        self.connectbtn.clicked.connect(self.connect)
        self.connectbtn.setText('Connect')
        self.comcb.setDisabled(False)
        self.connectbtn.setDisabled(False)
        self.refreshbtn.setDisabled(False)
