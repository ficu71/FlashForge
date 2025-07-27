import subprocess
from utils.adb_fastboot import ADBFastboot
from utils.logger import Logger


class DeviceDetector:
    """Detect connected devices via ADB or Fastboot and collect basic info."""

    def __init__(self) -> None:
        self.logger = Logger("DeviceDetector")
        self.adb = ADBFastboot()

    def detect_device(self):
        """Return a mapping of device identifiers to brand/model/mode information."""
        devices = self.adb.get_devices()
        if not devices:
            self.logger.error("No devices detected")
            return None

        device_info = {}
        for device in devices:
            props = self.adb.get_properties(device)
            device_info[device] = {
                "brand": props.get("ro.product.brand", "Unknown"),
                "model": props.get("ro.product.model", "Unknown"),
                "mode": self.detect_mode(device),
            }
        return device_info

    def detect_mode(self, device: str) -> str:
        """Attempt to determine if a device is in ADB, Fastboot or Download mode."""
        try:
            output = subprocess.check_output(["fastboot", "devices"]).decode()
            if device in output:
                return "fastboot"
            output = subprocess.check_output(["adb", "devices"]).decode()
            if device in output:
                return "adb"
            return "download"
        except Exception as e:  # pragma: no cover - external binary
            self.logger.error(f"Mode detection failed: {e}")
            return "unknown"