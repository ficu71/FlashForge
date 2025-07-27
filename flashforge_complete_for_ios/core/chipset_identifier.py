"""Detect chipset type for an Android device based on device properties."""

from utils.adb_fastboot import ADBFastboot
from utils.logger import Logger


class ChipsetIdentifier:
    def __init__(self) -> None:
        self.logger = Logger("ChipsetIdentifier")
        self.adb = ADBFastboot()

    def identify_chipset(self, device: str) -> str:
        """Return a human‑friendly chipset name based on system properties."""
        props = self.adb.get_properties(device)
        hardware = props.get("ro.hardware", "").lower()
        if "qualcomm" in hardware or "snapdragon" in hardware:
            return "Qualcomm"
        if "mediatek" in hardware or "mt" in hardware:
            return "MediaTek"
        if "exynos" in hardware:
            return "Exynos"
        if "kirin" in hardware:
            return "Kirin"
        self.logger.warning(f"Unknown chipset for device {device}")
        return "Unknown"