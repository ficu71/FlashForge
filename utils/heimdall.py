"""Wrapper around the Heimdall flashing tool for Samsung devices."""

import subprocess
from utils.logger import Logger


class Heimdall:
    def __init__(self) -> None:
        self.logger = Logger("Heimdall")

    def flash_samsung(self, device: str, firmware: dict) -> bool:
        """Flash firmware partitions using heimdall. Firmware is a mapping of partition->image path."""
        try:
            for partition, img in firmware.items():
                subprocess.check_call(["heimdall", "flash", f"--{partition}", img])
            self.logger.info("Samsung firmware flashed via Heimdall")
            return True
        except Exception as e:
            self.logger.error(f"Heimdall flash failed: {e}")
            return False