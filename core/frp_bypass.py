"""FRP bypass logic via pushing an APK and launching it via ADB."""

from utils.adb_fastboot import ADBFastboot
from utils.logger import Logger


class FRPBypass:
    def __init__(self) -> None:
        self.logger = Logger("FRPBypass")
        self.adb = ADBFastboot()

    def bypass_frp(self, device: str) -> bool:
        """Push and install a bypass APK then launch its main activity."""
        try:
            # Push exploit APK to device; path relative to project root
            self.adb.push(device, "resources/exploits/frp_bypass.apk", "/data/local/tmp/frp_bypass.apk")  # type: ignore[attr-defined]
            self.adb.install_apk(device, "frp_bypass.apk")  # type: ignore[attr-defined]
            self.adb.run_shell(device, "am start -n com.frp.bypass/.MainActivity")
            self.logger.info("FRP bypass initiated")
            return True
        except Exception as e:
            self.logger.error(f"FRP bypass failed: {e}")
            return False