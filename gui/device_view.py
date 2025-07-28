"""Widget for displaying connected devices."""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QListWidget, QLabel


class DeviceView(QWidget):
    def __init__(self, callback) -> None:
        super().__init__()
        self.callback = callback
        self.setup_ui()

    def setup_ui(self) -> None:
        layout = QVBoxLayout()
        self.label = QLabel("Connected Devices")
        self.device_list = QListWidget()
        layout.addWidget(self.label)
        layout.addWidget(self.device_list)
        self.setLayout(layout)

    def update_devices(self, devices) -> None:
        """Populate the list with detected devices."""
        self.device_list.clear()
        if not devices:
            return
        for device, info in devices.items():
            self.device_list.addItem(f"{info['brand']} {info['model']} ({device}) - {info['mode']}")
        self.callback(devices)

    def get_selected_device(self) -> str:
        item = self.device_list.currentItem()
        if item:
            # Extract device ID from string "brand model (serial) - mode"
            return item.text().split("(")[1].split(")")[0]
        return None