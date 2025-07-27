"""USB scanner for enumerating connected devices by vendor/product ID."""

import usb.core  # type: ignore
from utils.logger import Logger


class USBScanner:
    VENDOR_WHITELIST = {0x05C6, 0x0BB4, 0x18D1, 0x2E05}  # Qualcomm, HTC, Google, Kirin

    def __init__(self) -> None:
        self.logger = Logger("USBScanner")

    def scan_devices(self):
        """Return a list of dictionaries for each matching USB device."""
        devices = []
        try:
            for dev in usb.core.find(find_all=True):
                if dev.idVendor in self.VENDOR_WHITELIST:
                    devices.append(
                        {
                            "vendor_id": hex(dev.idVendor),
                            "product_id": hex(dev.idProduct),
                            "serial": dev.serial_number or "unknown",
                        }
                    )
        except Exception as e:
            self.logger.error(f"USB scan failed: {e}")
        return devices