# -*- coding: utf-8 -*-
"""
User interface.

@auteur: Darkness4
"""
import os
import sys

from csgo_gsi_arduino_lcd.data.server_thread import ServerThread
from qtpy.QtCore import QSize, Qt, Slot
from qtpy.QtGui import QIcon
from qtpy.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
from serial.tools import list_ports


def get_exec_path():
    try:
        sFile = os.path.abspath(sys.modules["__main__"].__file__)
    except Exception:
        sFile = sys.executable
    return os.path.dirname(sFile)


class CsgoWindow(QWidget):
    """App UI."""

    def __init__(self):
        """Init UI."""
        super(CsgoWindow, self).__init__()
        # Check ports
        list_ports_device = sorted(
            map(lambda x: str(x.name), list_ports.comports())
        )

        # Widgets
        self.server_thread = None
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

        self.payload_viewer_btn = QPushButton("View payload")
        self.payload_viewer_btn.setDisabled(True)

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

        # Icon
        app_icon = QIcon()
        for i in (16, 20, 24, 32, 48, 64, 128, 256, 512):
            app_icon.addFile(
                os.path.join(get_exec_path(), f"assets/csgo-{i}.ico"),
                QSize(i, i),
            )

        # Window
        self.setWindowIcon(app_icon)
        self.setWindowTitle("CSGO GSI on LCD")
        self.setWindowFlags(Qt.WindowCloseButtonHint)

        self.show()
        self.setFixedSize(self.size())

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
    def connect(self):
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

        # Enable payload_viewer
        self.payload_viewer_btn.clicked.connect(self.resume_payload_viewer)
        self.payload_viewer_btn.setDisabled(False)

    @Slot()
    def stop_server(self):
        """Stop the server."""
        # Disable buttons
        self.payload_viewer_btn.setDisabled(True)

        # Kill the messenger and server
        self.server_thread.arduino_mediator.shutdown()
        self.server_thread.payload_viewer.shutdown()
        self.server_thread.server.shutdown()
        self.server_thread = None

        # Change button function
        self.connect_btn.clicked.disconnect()
        self.connect_btn.clicked.connect(self.connect)
        self.connect_btn.setText("Connect")
        self.payload_viewer_btn.clicked.disconnect()
        self.payload_viewer_btn.clicked.connect(self.resume_payload_viewer)
        self.payload_viewer_btn.setText("View payload")

        # Enable buttons
        self.comcb.setDisabled(False)
        self.connect_btn.setDisabled(False)
        self.refresh_btn.setDisabled(False)

    @Slot()
    def resume_payload_viewer(self):
        """Start Payload Viewer."""
        # Start payload vierwer
        self.server_thread.payload_viewer.resume()

        # Change button function
        self.payload_viewer_btn.clicked.disconnect()
        self.payload_viewer_btn.clicked.connect(self.pause_payload_viewer)
        self.payload_viewer_btn.setText("Hide payload")

    @Slot()
    def pause_payload_viewer(self):
        """Stop Payload Viewer."""
        # Stop payload viewer
        if self.server_thread.payload_viewer is not None:
            self.server_thread.payload_viewer.pause()

        # Change button function
        self.payload_viewer_btn.clicked.disconnect()
        self.payload_viewer_btn.clicked.connect(self.resume_payload_viewer)
        self.payload_viewer_btn.setText("View payload")

    def close_all(self, *args, **kwargs):
        """Close everything before closing app."""
        super(CsgoWindow, self).closeEvent(*args, **kwargs)
        if self.server_thread is not None:
            self.server_thread.arduino_mediator.shutdown()
            self.server_thread.payload_viewer.shutdown()
            self.server_thread.server.shutdown()
            self.server_thread = None
