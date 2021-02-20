import json
from typing import Any, Dict, Optional

from qtpy.QtCore import Qt
from qtpy.QtGui import QIcon
from qtpy.QtWidgets import QDialog, QFormLayout, QLabel, QScrollArea


class PayloadDialog(QDialog):
    label: QLabel

    def __init__(self, app_icon: QIcon):
        super().__init__(
            None, Qt.WindowSystemMenuHint | Qt.WindowCloseButtonHint
        )
        self.setWindowIcon(app_icon)
        self.setWindowTitle("Last Payload")

        self.label = QLabel("")
        self.label.setTextInteractionFlags(Qt.TextSelectableByMouse)

        scrollArea = QScrollArea()
        scrollArea.setWidgetResizable(True)

        scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scrollArea.setWidget(self.label)
        scrollArea.setWidgetResizable(True)

        layout = QFormLayout()
        layout.addWidget(scrollArea)
        self.setLayout(layout)

    def update_text(self, data: Optional[Dict[str, Any]]):
        self.label.setText(
            json.dumps(data, indent=2, sort_keys=True)
            if data is not None
            else ""
        )
