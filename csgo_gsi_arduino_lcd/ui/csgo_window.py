# -*- coding: utf-8 -*-
"""
User interface.

@auteur: Darkness4
"""
import os
import sys
from typing import Optional

from csgo_gsi_arduino_lcd.data.server_thread import ServerThread
from csgo_gsi_arduino_lcd.ui.payload_dialog import PayloadDialog
from qtpy.QtCore import QSize, Qt, Slot
from qtpy.QtGui import QCloseEvent, QIcon
from qtpy.QtWidgets import (QComboBox, QHBoxLayout, QPushButton, QVBoxLayout,
                            QWidget)
from serial.tools import list_ports


def resource_path(relative_path: str):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


class CsgoWindow(QWidget):
    """App UI."""

    server_thread: Optional[ServerThread] = None
    connect_btn: QPushButton
    refresh_btn: QPushButton
    payload_viewer_btn: QPushButton
    comcb: QComboBox
    payload_dialog: PayloadDialog

    def __init__(self):
        """Init UI."""
        super(CsgoWindow, self).__init__()
        # Icon
        app_icon = QIcon()
        for i in (16, 20, 24, 32, 48, 64, 128, 256, 512):
            app_icon.addFile(
                resource_path(f"assets/csgo-{i}.ico"),
                QSize(i, i),
            )

        # Window
        self.setWindowIcon(app_icon)
        self.setWindowTitle("CSGO GSI on LCD")
        self.setWindowFlags(Qt.WindowCloseButtonHint)

        # Check ports
        list_ports_device = sorted(
            map(lambda x: str(x.name), list_ports.comports())
        )

        # Widgets
        self.connect_btn = QPushButton("Connect")

        self.comcb = QComboBox()
        self.comcb.addItems(list_ports_device)
        if not list_ports_device:
            self.connect_btn.setDisabled(True)
        else:
            self.connect_btn.setDisabled(False)

        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.resize(self.refresh_btn.sizeHint())
        self.refresh_btn.clicked.connect(self.refresh)

        # Payload Viewer
        self.payload_viewer_btn = QPushButton("View payload")
        self.payload_viewer_btn.clicked.connect(self.show_last_data)
        self.payload_dialog = PayloadDialog(app_icon)

        # Container
        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        vbox.addStretch(1)
        hbox.addWidget(self.comcb)
        hbox.addWidget(self.refresh_btn)
        vbox.addLayout(hbox)
        vbox.addWidget(self.payload_viewer_btn)
        vbox.addWidget(self.connect_btn)
        self.setLayout(vbox)

        self.show()
        self.setFixedSize(self.size())

    @Slot()
    def show_last_data(self):
        data = None
        if self.server_thread is not None:
            data = self.server_thread.data_store.data
        self.payload_dialog.update_text(data)
        self.payload_dialog.show()

    @Slot()
    def refresh(self):
        """Refresh COM ports."""
        self.comcb.clear()
        list_ports_device = sorted(
            map(lambda x: str(x.name), list_ports.comports())
        )
        self.comcb.addItems(list_ports_device)
        if not list_ports_device:
            self.connect_btn.setDisabled(True)
        else:
            self.connect_btn.setDisabled(False)

    @Slot()
    def start_server(self):
        """Connect to the server."""
        # Disable buttons
        self.comcb.setDisabled(True)
        self.connect_btn.setDisabled(True)
        self.refresh_btn.setDisabled(True)

        # Server start
        if self.server_thread is None:
            self.server_thread = ServerThread(str(self.comcb.currentText()))
        self.server_thread.start()

        # Change connect button's function to "stop"
        self.connect_btn.clicked.disconnect()
        self.connect_btn.clicked.connect(self.stop_server)
        self.connect_btn.setDisabled(False)
        self.connect_btn.setText("Stop")

    @Slot()
    def stop_server(self):
        """Stop the server."""
        # Kill the messenger and server
        if self.server_thread is not None:
            self.server_thread.arduino_mediator.shutdown()
            self.server_thread.server.shutdown()
            self.server_thread = None

        # Change button function
        self.connect_btn.clicked.disconnect()
        self.connect_btn.clicked.connect(self.start_server)
        self.connect_btn.setText("Connect")

        # Enable buttons
        self.comcb.setDisabled(False)
        self.connect_btn.setDisabled(False)
        self.refresh_btn.setDisabled(False)

    def close_all(self, event: QCloseEvent):
        """Close everything before closing app."""
        super(CsgoWindow, self).closeEvent(event)
        if self.server_thread is not None:
            self.server_thread.arduino_mediator.shutdown()
            self.server_thread.server.shutdown()
            self.server_thread = None
