"""Widget for selecting firmware images from disk."""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLineEdit, QFileDialog


class FirmwareView(QWidget):
    def __init__(self, callback) -> None:
        super().__init__()
        self.callback = callback
        self.setup_ui()

    def setup_ui(self) -> None:
        layout = QVBoxLayout()
        self.firmware_path = QLineEdit()
        browse_btn = QPushButton("Browse Firmware")
        browse_btn.clicked.connect(self.browse_firmware)
        layout.addWidget(self.firmware_path)
        layout.addWidget(browse_btn)
        self.setLayout(layout)

    def browse_firmware(self) -> None:
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Firmware",
            "",
            "Firmware Files (*.tar.md5 *.zip *.img *.scatter)",
        )
        if file_path:
            self.firmware_path.setText(file_path)
            self.callback(file_path)

    def get_selected_firmware(self) -> str:
        return self.firmware_path.text()

    def get_selected_boot_img(self) -> str:
        path = self.firmware_path.text()
        return path if path.endswith(".img") else None

    def get_selected_twrp_img(self) -> str:
        # For now both boot and twrp images use the same selector
        path = self.firmware_path.text()
        return path if path.endswith(".img") else None

    def set_firmware(self, firmware: str) -> None:
        self.firmware_path.setText(firmware)