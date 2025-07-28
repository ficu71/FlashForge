"""Simple wrapper around the adb and fastboot command line tools."""

import subprocess
from utils.logger import Logger


class ADBFastboot:
    def __init__(self) -> None:
        self.logger = Logger("ADBFastboot")

    def get_devices(self):
        """Return a list of connected ADB devices."""
        try:
            output = subprocess.check_output(["adb", "devices"]).decode()
            devices = [line.split("\t")[0] for line in output.splitlines() if "\tdevice" in line]
            return devices
        except Exception as e:
            self.logger.error(f"ADB device scan failed: {e}")
            return []

    def get_properties(self, device: str):
        """Return a dictionary of device properties via `adb shell getprop`."""
        try:
            output = subprocess.check_output(["adb", "-s", device, "shell", "getprop"]).decode()
            props = {}
            for line in output.splitlines():
                if "[" in line and "]" in line:
                    key = line.split("[")[1].split("]")[0]
                    value = line.split(": ")[1].strip("[]")
                    props[key] = value
            return props
        except Exception as e:
            self.logger.error(f"Get properties failed: {e}")
            return {}

    def flash(self, device: str, partition: str, image: str) -> bool:
        """Use fastboot to flash a partition."""
        try:
            subprocess.check_call(["fastboot", "-s", device, "flash", partition, image])
            self.logger.info(f"Flashed {partition} with {image}")
            return True
        except Exception as e:
            self.logger.error(f"Flash failed: {e}")
            return False

    def push(self, device: str, source: str, dest: str) -> bool:
        """Push a file to the device using ADB."""
        try:
            subprocess.check_call(["adb", "-s", device, "push", source, dest])
            self.logger.info(f"Pushed {source} to {dest}")
            return True
        except Exception as e:
            self.logger.error(f"Push failed: {e}")
            return False

    def pull(self, device: str, source: str, dest: str) -> bool:
        """Pull a file from the device using ADB."""
        try:
            subprocess.check_call(["adb", "-s", device, "pull", source, dest])
            self.logger.info(f"Pulled {source} to {dest}")
            return True
        except Exception as e:
            self.logger.error(f"Pull failed: {e}")
            return False

    def run_shell(self, device: str, command: str):
        """Run an arbitrary shell command on the device."""
        try:
            output = subprocess.check_output(["adb", "-s", device, "shell", command]).decode()
            self.logger.info(f"Shell command executed: {command}")
            return output
        except Exception as e:
            self.logger.error(f"Shell command failed: {e}")
            return None

    def check_oem_unlock(self, device: str) -> bool:
        """Check if OEM unlock is enabled via fastboot."""
        try:
            output = subprocess.check_output(["fastboot", "-s", device, "oem", "device-info"]).decode().lower()
            return "enabled" in output
        except Exception as e:
            self.logger.error(f"OEM unlock check failed: {e}")
            return False

    def oem_unlock(self, device: str) -> bool:
        """Issue fastboot OEM unlock command."""
        try:
            subprocess.check_call(["fastboot", "-s", device, "oem", "unlock"])
            self.logger.info("OEM unlock successful")
            return True
        except Exception as e:
            self.logger.error(f"OEM unlock failed: {e}")
            return False

    # Placeholder methods for unsupported operations; these will log errors if called.
    def flash_kirin(self, device: str, firmware) -> bool:
        self.logger.error("flash_kirin is not implemented")
        return False

    def flash_generic(self, device: str, firmware) -> bool:
        self.logger.error("flash_generic is not implemented")
        return False

    def install_apk(self, device: str, apk_name: str) -> bool:
        """Install an APK that has already been pushed to /data/local/tmp."""
        try:
            subprocess.check_call(["adb", "-s", device, "shell", "pm", "install", f"/data/local/tmp/{apk_name}"])
            self.logger.info(f"Installed {apk_name}")
            return True
        except Exception as e:
            self.logger.error(f"Install APK failed: {e}")
            return False

    def run_command(self, device: str, command: str) -> bool:
        """Wrapper to run a shell command and ignore the output."""
        return self.run_shell(device, command) is not None