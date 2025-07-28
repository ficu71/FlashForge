"""Main application window assembling the various views and wiring up actions."""

from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QFileDialog,
)
from gui.device_view import DeviceView
from gui.firmware_view import FirmwareView
from gui.log_view import LogView
from core.device_detector import DeviceDetector
from core.chipset_identifier import ChipsetIdentifier
from core.firmware_handler import FirmwareHandler
from core.exploit_engine import ExploitEngine
from core.frp_bypass import FRPBypass
from core.bootloader_unlock import BootloaderUnlock
from core.lock_remover import LockRemover
from core.patcher import Patcher
from utils.logger import Logger


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("FlashForge - Syndicate Tool")
        self.setGeometry(100, 100, 1200, 800)
        self.logger = Logger("MainWindow")
        # Instantiate core components
        self.device_detector = DeviceDetector()
        self.chipset_identifier = ChipsetIdentifier()
        self.firmware_handler = FirmwareHandler()
        self.exploit_engine = ExploitEngine()
        self.frp_bypass = FRPBypass()
        self.bootloader_unlock = BootloaderUnlock()
        self.lock_remover = LockRemover()
        self.patcher = Patcher()
        # Build UI
        self.setup_ui()

    def setup_ui(self) -> None:
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout()
        # Left panel: device and firmware selectors
        left_panel = QVBoxLayout()
        self.device_view = DeviceView(self.device_detected_callback)
        self.firmware_view = FirmwareView(self.firmware_selected_callback)
        left_panel.addWidget(self.device_view)
        left_panel.addWidget(self.firmware_view)
        # Right panel: logs and actions
        right_panel = QVBoxLayout()
        self.log_view = LogView()
        action_layout = self.create_action_buttons()
        right_panel.addWidget(self.log_view)
        right_panel.addLayout(action_layout)
        # Compose panels
        main_layout.addLayout(left_panel)
        main_layout.addLayout(right_panel)
        central_widget.setLayout(main_layout)

    def create_action_buttons(self) -> QVBoxLayout:
        layout = QVBoxLayout()
        buttons = [
            ("Scan Devices", self.scan_devices),
            ("Flash Firmware", self.flash_firmware),
            ("Bypass FRP", self.bypass_frp),
            ("Unlock Bootloader", self.unlock_bootloader),
            ("Remove Lock", self.remove_lock),
            ("Patch Magisk", self.patch_magisk),
            ("Flash TWRP", self.flash_twrp),
        ]
        for text, func in buttons:
            btn = QPushButton(text)
            btn.clicked.connect(func)
            layout.addWidget(btn)
        return layout

    # Action handlers
    def scan_devices(self) -> None:
        devices = self.device_detector.detect_device()
        if devices:
            self.device_view.update_devices(devices)
            self.logger.info("Device scan completed")

    def flash_firmware(self) -> None:
        device = self.device_view.get_selected_device()
        firmware_path = self.firmware_view.get_selected_firmware()
        if not device or not firmware_path:
            self.logger.error("No device or firmware selected")
            return
        chipset = self.chipset_identifier.identify_chipset(device)
        firmware = self.firmware_handler.load_firmware(firmware_path)
        try:
            self.firmware_handler.flash_firmware(device, firmware, chipset)
            self.logger.info("Firmware flash completed")
        except Exception as e:
            self.logger.error(f"Firmware flash failed: {e}")

    def bypass_frp(self) -> None:
        device = self.device_view.get_selected_device()
        if device and self.frp_bypass.bypass_frp(device):
            self.logger.info("FRP bypass successful")
        else:
            self.logger.error("FRP bypass failed")

    def unlock_bootloader(self) -> None:
        device = self.device_view.get_selected_device()
        if not device:
            self.logger.error("No device selected")
            return
        chipset = self.chipset_identifier.identify_chipset(device)
        if self.bootloader_unlock.unlock(device, chipset):
            self.logger.info("Bootloader unlocked")
        else:
            self.logger.error("Bootloader unlock failed")

    def remove_lock(self) -> None:
        device = self.device_view.get_selected_device()
        if device and self.lock_remover.remove_lock(device):
            self.logger.info("Screen lock removed")
        else:
            self.logger.error("Screen lock removal failed")

    def patch_magisk(self) -> None:
        device = self.device_view.get_selected_device()
        boot_img = self.firmware_view.get_selected_boot_img()
        if not device or not boot_img:
            self.logger.error("No device or boot image selected")
            return
        patched_img = self.patcher.patch_magisk(device, boot_img)
        if patched_img:
            self.logger.info("Magisk patched successfully")
        else:
            self.logger.error("Magisk patch failed")

    def flash_twrp(self) -> None:
        device = self.device_view.get_selected_device()
        twrp_img = self.firmware_view.get_selected_twrp_img()
        if not device or not twrp_img:
            self.logger.error("No device or TWRP image selected")
            return
        if self.patcher.flash_twrp(device, twrp_img):
            self.logger.info("TWRP flashed successfully")
        else:
            self.logger.error("TWRP flash failed")

    # Callbacks from views
    def device_detected_callback(self, devices):
        self.device_view.update_devices(devices)

    def firmware_selected_callback(self, firmware_path: str):
        self.firmware_view.set_firmware(firmware_path)