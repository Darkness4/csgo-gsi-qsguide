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


class Csgogsi(QWidget):
    """
    App UI.

    Attributes
    ----------
    comcb : QComboBox
        Combo Box responsible for listing devices.
    connect_btn : QPushButton
        Button responsible for connection.
    payload_viewer_btn : QPushButton
        Button responsible to view the payload.
    refresh_btn :QPushButton
        Button responsible to refresh Serial.
    server_thread : ServerThread
        Server.

    Methods
    -------
    close_all(*args, **kwargs)
        Close everything before closing app.
    connect()
        Connect to COM.
    refresh()
        Refresh list.
    start_payload_viewer()
        Start Payload Viewer.
    stop_server()
        Stop the Server.
    stop_payload_viewer()
        Stop Payload Viewer.

    """

    def __init__(self) -> None:
        """Init UI."""
        super(Csgogsi, self).__init__()
        # Widgets
        self.server_thread = None
        self.connect_btn = QPushButton('Connect')
        self.connect_btn.clicked.connect(self.connect)

        self.comcb = QComboBox()
        list_ports_device = [port.device for port in list_ports.comports()]
        self.comcb.addItems(list_ports_device)
        if list_ports_device == []:
            self.connect_btn.setDisabled(True)
        else:
            self.connect_btn.setDisabled(False)

        self.refresh_btn = QPushButton('Refresh')
        self.refresh_btn.resize(self.refresh_btn.sizeHint())
        self.refresh_btn.clicked.connect(self.refresh)

        self.payload_viewer_btn = QPushButton('View payload')
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
    def refresh(self) -> None:
        """Refresh COM ports."""
        self.comcb.clear()
        list_ports_device = [port.device for port in list_ports.comports()]
        self.comcb.addItems(list_ports_device)
        if list_ports_device == []:
            self.connect_btn.setDisabled(True)
        else:
            self.connect_btn.setDisabled(False)

    @Slot()
    def connect(self) -> None:
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
        self.connect_btn.setText('Stop')
        # Enable payload_viewer
        self.payload_viewer_btn.clicked.connect(self.start_payload_viewer)
        self.payload_viewer_btn.setDisabled(False)

    @Slot()
    def stop_server(self) -> None:
        """Stop the server."""
        # Disable buttons
        self.payload_viewer_btn.setDisabled(True)
        # Kill the messenger and server
        self.server_thread.server.messenger.shutdown()
        if self.server_thread.server.payload_viewer is not None \
           and self.server_thread.server.payload_viewer.is_alive():
            self.server_thread.server.payload_viewer.shutdown()
            self.server_thread.server.payload_viewer = None
        self.server_thread.server.shutdown()
        self.server_thread = None
        # Change button function
        self.connect_btn.clicked.disconnect()
        self.connect_btn.clicked.connect(self.connect)
        self.connect_btn.setText('Connect')
        self.payload_viewer_btn.clicked.disconnect()
        self.payload_viewer_btn.clicked.connect(self.start_payload_viewer)
        self.payload_viewer_btn.setText('View payload')
        # Enable buttons
        self.comcb.setDisabled(False)
        self.connect_btn.setDisabled(False)
        self.refresh_btn.setDisabled(False)

    @Slot()
    def start_payload_viewer(self) -> None:
        """Start Payload Viewer."""
        # Start payload vierwer
        self.server_thread.server.payload_viewer = PayloadViewerThread()
        self.server_thread.server.payload_viewer.start()

        # Change button function
        self.payload_viewer_btn.clicked.disconnect()
        self.payload_viewer_btn.clicked.connect(self.stop_payload_viewer)
        self.payload_viewer_btn.setText('Hide payload')

    @Slot()
    def stop_payload_viewer(self) -> None:
        """Stop Payload Viewer."""
        # Stop payload viewer
        self.server_thread.server.payload_viewer.shutdown()
        self.server_thread.server.payload_viewer = None

        # Change button function
        self.payload_viewer_btn.clicked.disconnect()
        self.payload_viewer_btn.clicked.connect(self.start_payload_viewer)
        self.payload_viewer_btn.setText('View payload')

    def close_all(self, *args, **kwargs) -> None:
        """Close everything before closing app."""
        super(Csgogsi, self).closeEvent(*args, **kwargs)
        if self.server_thread is not None \
           and self.server_thread.server.messenger.is_alive():
            self.server_thread.server.messenger.shutdown()
        if self.server_thread is not None and self.server_thread.isRunning():
            self.server_thread.server.shutdown()
