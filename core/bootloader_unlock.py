"""Bootloader unlocking logic leveraging OEM unlock or chipset exploits."""

from utils.adb_fastboot import ADBFastboot
from utils.logger import Logger
from core.exploit_engine import ExploitEngine


class BootloaderUnlock:
    def __init__(self) -> None:
        self.logger = Logger("BootloaderUnlock")
        self.adb = ADBFastboot()
        self.exploit_engine = ExploitEngine()

    def unlock(self, device: str, chipset: str) -> bool:
        """Unlock the bootloader using OEM commands or a chipset exploit."""
        try:
            if self.adb.check_oem_unlock(device):  # type: ignore[attr-defined]
                self.adb.oem_unlock(device)  # type: ignore[attr-defined]
                return True
            self.logger.info("OEM unlocking disabled, attempting exploit")
            return self.exploit_engine.run_exploit(chipset, device, "bootloader_unlock")
        except Exception as e:
            self.logger.error(f"Bootloader unlock failed: {e}")
            return False