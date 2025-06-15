
FROM python:3.9-slim

# Zainstaluj zależności systemowe
RUN apt-get update && apt-get install -y \
    adb fastboot heimdall-flash \
    libgl1-mesa-glx libglib2.0-0 libsm6 libxrender1 libxext6 \
    xvfb x11-utils x11-xkb-utils pulseaudio qdl && \
    rm -rf /var/lib/apt/lists/*

# Ustaw katalog roboczy
WORKDIR /app

# Skopiuj pliki projektu
COPY . /app

# Instaluj zależności Pythona
RUN pip install -r requirements.txt

# Domyślne polecenie uruchomienia z symulowanym GUI
CMD ["xvfb-run", "-a", "python", "main.py"]
