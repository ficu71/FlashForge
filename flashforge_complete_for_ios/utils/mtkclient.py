"""Wrapper around MTKClient for MediaTek devices."""

import subprocess
from utils.logger import Logger


class MTKClient:
    def __init__(self) -> None:
        self.logger = Logger("MTKClient")

    def flash_brom(self, device: str, firmware: dict) -> bool:
        """Flash a scatter firmware using mtkclient."""
        try:
            subprocess.check_call(["mtkclient", "flash", "--scatter", firmware["path"]])
            self.logger.info("MediaTek firmware flashed via MTKClient")
            return True
        except Exception as e:
            self.logger.error(f"MTKClient flash failed: {e}")
            return False