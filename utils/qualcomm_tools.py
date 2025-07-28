"""Wrapper for flashing Qualcomm devices via EDL (qdl)."""

import subprocess
from utils.logger import Logger


class QualcommTools:
    def __init__(self) -> None:
        self.logger = Logger("QualcommTools")

    def flash_edl(self, device: str, firmware: dict) -> bool:
        """Flash firmware using Qualcomm's EDL mode via qdl."""
        try:
            subprocess.check_call(["qdl", "--device", device, "--firmware", firmware["path"]])
            self.logger.info("Qualcomm firmware flashed via EDL")
            return True
        except Exception as e:
            self.logger.error(f"EDL flash failed: {e}")
            return False