# -*- coding: utf-8 -*-
"""
User interface.

@auteur: Darkness4
"""
from serial.tools import list_ports
from qtpy.QtWidgets import (QPushButton, QComboBox,
                            QVBoxLayout, QHBoxLayout, QWidget)
from qtpy.QtCore import Slot, Qt
from qtpy.QtGui import QIcon
from .server import ServerThread


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
        self.setWindowIcon(QIcon('csgo-icon-42854-16x16.ico'))
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
