# FlashForge - Syndicate Flashing Tool

## Setup
1. Install dependencies:
```bash
pip install -r requirements.txt
```
2. Install platform tools:
    * **ADB/Fastboot**
    * **Heimdall** (for Samsung devices)
    * **MTKClient** (for MediaTek devices)
    * **QDL** (for Qualcomm EDL)
3. Place drivers in `resources/drivers/` and any custom firmwares in `resources/firmwares/`.

Run the GUI application with:
```bash
python main.py
```

### Structure

* `core/` – core logic for device detection, flashing and exploit handling.
* `gui/` – PyQt5‑based GUI components for the application.
* `utils/` – helper tools for interacting with ADB, Heimdall, MTKClient, etc.
* `exploits/` – chipset‑specific exploit modules.
* `resources/` – placeholder directories for drivers, firmware files and patches.

### Commands to Run

```bash
pip install -r requirements.txt
mkdir logs
python main.py
```