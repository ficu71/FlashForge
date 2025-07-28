"""Firmware extraction and flashing helpers."""

import tarfile
import zipfile
from utils.logger import Logger
from utils.adb_fastboot import ADBFastboot
from utils.heimdall import Heimdall
from utils.mtkclient import MTKClient
from utils.qualcomm_tools import QualcommTools


class FirmwareHandler:
    def __init__(self) -> None:
        self.logger = Logger("FirmwareHandler")
        self.adb = ADBFastboot()
        self.heimdall = Heimdall()
        self.mtk = MTKClient()
        self.qcom = QualcommTools()

    def load_firmware(self, path: str):
        """Return a dictionary describing the firmware and extract it if necessary."""
        if path.endswith(".tar.md5"):
            return self.extract_tar_md5(path)
        if path.endswith(".zip"):
            return self.extract_zip(path)
        if path.endswith(".img"):
            return {"type": "image", "path": path}
        if path.endswith(".scatter"):
            return {"type": "scatter", "path": path}
        self.logger.error("Unsupported firmware format")
        return None

    def flash_firmware(self, device: str, firmware, chipset: str) -> None:
        """Dispatch flashing to the appropriate tool based on chipset."""
        try:
            if chipset == "Qualcomm":
                self.qcom.flash_edl(device, firmware)
            elif chipset == "MediaTek":
                self.mtk.flash_brom(device, firmware)
            elif chipset == "Exynos":
                self.heimdall.flash_samsung(device, firmware)
            elif chipset == "Kirin":
                self.adb.flash_kirin(device, firmware)  # type: ignore[attr-defined]
            else:
                self.adb.flash_generic(device, firmware)  # type: ignore[attr-defined]
        except Exception as e:
            self.logger.error(f"Flash failed: {e}")
            raise

    def extract_tar_md5(self, path: str):
        with tarfile.open(path, "r") as tar:
            tar.extractall("resources/firmwares")
        return {"type": "tar", "path": "resources/firmwares"}

    def extract_zip(self, path: str):
        with zipfile.ZipFile(path, "r") as zip_ref:
            zip_ref.extractall("resources/firmwares")
        return {"type": "zip", "path": "resources/firmwares"}