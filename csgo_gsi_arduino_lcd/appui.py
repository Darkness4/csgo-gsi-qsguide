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
from .tableviewer import PayloadViewerThread

__dir__ = dirname(abspath(__file__))


def serial_ports():
    """List serial port names."""
    return [port.device for port in list_ports.comports()]


class Csgogsi(QWidget):
    """App UI."""

    def __init__(self):
        """Init UI."""
        super(Csgogsi, self).__init__()
        # Widgets
        self.serverthread = None
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

        self.payloadviewerbtn = QPushButton('View payload')
        self.payloadviewerbtn.setDisabled(True)

        # Container
        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        vbox.addStretch(1)
        hbox.addWidget(self.comcb)
        hbox.addWidget(self.refreshbtn)
        vbox.addLayout(hbox)
        vbox.addWidget(self.payloadviewerbtn)
        vbox.addWidget(self.connectbtn)
        self.setLayout(vbox)
        # Icon
        app_icon = QIcon()
        app_icon.addFile(
            __dir__ + "\\data\\csgo-16.ico", QSize(16, 16))
        app_icon.addFile(
            __dir__ + "\\data\\csgo-20.ico", QSize(20, 20))
        app_icon.addFile(
            __dir__ + "\\data\\csgo-24.ico", QSize(24, 24))
        app_icon.addFile(
            __dir__ + "\\data\\csgo-32.ico", QSize(32, 32))
        app_icon.addFile(
            __dir__ + "\\data\\csgo-48.ico", QSize(48, 48))
        app_icon.addFile(
            __dir__ + "\\data\\csgo-64.ico", QSize(64, 64))
        app_icon.addFile(
            __dir__ + "\\data\\csgo-128.ico", QSize(128, 128))
        app_icon.addFile(
            __dir__ + "\\data\\csgo-256.ico", QSize(256, 256))
        app_icon.addFile(
            __dir__ + "\\data\\csgo-512.ico", QSize(512, 512))
        # Window
        self.setWindowIcon(app_icon)
        self.setWindowTitle('CSGO GSI on LCD')
        self.setWindowFlags(Qt.WindowCloseButtonHint)

        self.show()
        self.setFixedSize(self.size())

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
        # Disable buttons
        self.comcb.setDisabled(True)
        self.connectbtn.setDisabled(True)
        self.refreshbtn.setDisabled(True)
        # Server start
        if self.serverthread is None:
            self.serverthread = ServerThread(str(self.comcb.currentText()))
        self.serverthread.start()
        # Change connect button's function to "stop"
        self.connectbtn.clicked.disconnect()
        self.connectbtn.clicked.connect(self.stop)
        self.connectbtn.setDisabled(False)
        self.connectbtn.setText('Stop')
        # Enable payloadviewer
        self.payloadviewerbtn.clicked.connect(self.startpayloadviewer)
        self.payloadviewerbtn.setDisabled(False)

    @Slot()
    def stop(self):
        """Stop the server."""
        # Disable buttons
        self.payloadviewerbtn.setDisabled(True)
        # Kill the messenger and server
        self.serverthread.server.messenger.shutdown()
        if (self.serverthread.server.payloadviewer is not None
           and self.serverthread.server.payloadviewer.is_alive()):
            self.serverthread.server.payloadviewer.shutdown()
            self.serverthread.server.payloadviewer = None
        self.serverthread.server.shutdown()
        self.serverthread = None
        # Change button function
        self.connectbtn.clicked.disconnect()
        self.connectbtn.clicked.connect(self.connect)
        self.connectbtn.setText('Connect')
        self.payloadviewerbtn.clicked.disconnect()
        self.payloadviewerbtn.clicked.connect(self.startpayloadviewer)
        self.payloadviewerbtn.setText('View payload')
        # Enable buttons
        self.comcb.setDisabled(False)
        self.connectbtn.setDisabled(False)
        self.refreshbtn.setDisabled(False)

    @Slot()
    def startpayloadviewer(self):
        """Stop the server."""
        # Start payload vierwer
        self.serverthread.server.payloadviewer = PayloadViewerThread()
        self.serverthread.server.payloadviewer.start()

        # Change button function
        self.payloadviewerbtn.clicked.disconnect()
        self.payloadviewerbtn.clicked.connect(self.stoppayloadviewer)
        self.payloadviewerbtn.setText('Hide payload')

    @Slot()
    def stoppayloadviewer(self):
        """Stop the server."""
        # Stop payload viewer
        self.serverthread.server.payloadviewer.shutdown()
        self.serverthread.server.payloadviewer = None

        # Change button function
        self.payloadviewerbtn.clicked.disconnect()
        self.payloadviewerbtn.clicked.connect(self.startpayloadviewer)
        self.payloadviewerbtn.setText('View payload')

    def closeEvent(self, *args, **kwargs):
        """Close everything before closing app."""
        super(Csgogsi, self).closeEvent(*args, **kwargs)
        if (self.serverthread is not None
           and self.serverthread.server.messenger.is_alive()):
            self.serverthread.server.messenger.shutdown()
        if self.serverthread is not None and self.serverthread.isRunning():
            self.serverthread.server.shutdown()
