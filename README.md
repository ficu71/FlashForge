# FlashForge – Syndicate Flashing Tool

**FlashForge** to zaawansowane narzędzie desktopowe stworzone do serwisowania urządzeń z systemem Android: flashowania, odblokowywania bootloadera, bypassowania FRP, patchowania Magiska, usuwania blokad ekranu i obsługi exploitów. Projekt posiada pełne GUI w PyQt5 i jest gotowy do użycia offline przez techników serwisowych.

---

## 🔧 Funkcje
- Wykrywanie urządzeń (ADB / Fastboot / Download)
- Obsługa chipsetów: Qualcomm, MediaTek, Exynos, Kirin
- Flashowanie firmware (.zip, .tar.md5, .img, .scatter)
- Odblokowanie bootloadera (standardowe i exploity)
- FRP Bypass z wykorzystaniem APK i exploitów
- Patchowanie Magiska + Flash TWRP
- Pełne GUI (PyQt5) z Dark Theme
- Logi zapisywane do plików i podglądane w interfejsie
- Motyw dźwiękowy przy starcie + splashscreen

---

## 📦 Wymagania
- Python 3.8+
- Zainstalowane narzędzia CLI: `adb`, `fastboot`, `heimdall`, `qdl`, `mtkclient`
- System: Linux / Windows (kompatybilność CLI zależna od środowiska)

---

## 🚀 Instalacja

```bash
git clone https://github.com/twoj-login/FlashForge.git
cd FlashForge-GitRelease
pip install -r requirements.txt
mkdir logs
python main.py
```

---

## 🐳 Uruchomienie przez Docker

```bash
docker build -t flashforge .
docker run -it --rm --device=/dev/bus/usb:/dev/bus/usb flashforge
```

---

## 📂 Struktura projektu
```
FlashForge-GitRelease/
├── core/                  # Logika działania
├── gui/                   # GUI w PyQt5
├── utils/                 # Obsługa CLI tools, logger
├── exploits/              # Moduły exploitów dla chipsetów
├── resources/
│   ├── branding/          # Logo i splashscreen
│   └── audio/             # Motyw dźwiękowy
├── requirements.txt
├── Dockerfile
├── main.py
├── README.md
```

---

## ⚠️ Informacje prawne

Projekt FlashForge ma charakter **edukacyjny i serwisowy**. Nie wolno używać go do łamania zabezpieczeń cudzych urządzeń bez zgody właściciela. Autor nie ponosi odpowiedzialności za niewłaściwe użycie.

---

## 🧠 Licencja

MIT License © 2025 FlashForge Syndicate
