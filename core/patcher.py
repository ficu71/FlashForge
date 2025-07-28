"""Magisk and TWRP patching helpers."""

from utils.adb_fastboot import ADBFastboot
from utils.logger import Logger


class Patcher:
    def __init__(self) -> None:
        self.logger = Logger("Patcher")
        self.adb = ADBFastboot()

    def patch_magisk(self, device: str, boot_img: str):
        """Patch a boot image with Magisk and return the path to the patched image."""
        try:
            # push boot image and Magisk ZIP to device
            self.adb.push(device, boot_img, "/data/local/tmp/boot.img")  # type: ignore[attr-defined]
            self.adb.push(device, "resources/patches/magisk.zip", "/data/local/tmp/magisk.zip")  # type: ignore[attr-defined]
            # run the Magisk patch command on device; requires magisk binary installed
            self.adb.run_shell(device, "magisk --install /data/local/tmp/magisk.zip /data/local/tmp/boot.img")
            # pull patched image back
            self.adb.pull(device, "/data/local/tmp/boot_patched.img", "resources/patches/boot_patched.img")  # type: ignore[attr-defined]
            self.logger.info("Magisk patch applied")
            return "resources/patches/boot_patched.img"
        except Exception as e:
            self.logger.error(f"Magisk patch failed: {e}")
            return None

    def flash_twrp(self, device: str, twrp_img: str) -> bool:
        """Flash a TWRP recovery image to the device."""
        try:
            self.adb.flash(device, "recovery", twrp_img)
            self.logger.info("TWRP flashed successfully")
            return True
        except Exception as e:
            self.logger.error(f"TWRP flash failed: {e}")
            return False