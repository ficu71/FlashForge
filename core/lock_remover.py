"""Screen lock removal logic via pushing a shell script and executing it."""

from utils.adb_fastboot import ADBFastboot
from utils.logger import Logger


class LockRemover:
    def __init__(self) -> None:
        self.logger = Logger("LockRemover")
        self.adb = ADBFastboot()

    def remove_lock(self, device: str) -> bool:
        """Execute a lock removal script on the device via ADB."""
        try:
            self.adb.push(device, "resources/exploits/lock_remover.sh", "/data/local/tmp/lock_remover.sh")  # type: ignore[attr-defined]
            self.adb.run_shell(device, "sh /data/local/tmp/lock_remover.sh")
            self.logger.info("Screen lock removal initiated")
            return True
        except Exception as e:
            self.logger.error(f"Lock removal failed: {e}")
            return False