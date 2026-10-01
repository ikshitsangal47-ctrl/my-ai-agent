#!/bin/bash
echo "=========================================="
echo "Setting up Custom AI Desktop Agent for Linux"
echo "=========================================="

# 1. System packages installation (Added espeak & libespeak1)
echo "[1/5] Installing system dependencies..."
sudo apt-get update
sudo apt-get install -y python3-pip python3-venv python3-tk scrot x11-utils xvfb portaudio19-dev espeak espeak-ng libespeak1

# 2. Virtual environment setup
echo "[2/5] Setting up Python virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

source venv/bin/activate

# 3. Pip dependencies installation
echo "[3/5] Installing Python requirements..."
pip install --upgrade pip
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
elif [ -f "requirement.txt" ]; then
    mv requirement.txt requirements.txt
    pip install -r requirements.txt
else
    echo "Error: requirements.txt file not found!"
    exit 1
fi

# 4. Playwright browser setup
echo "[4/5] Installing Playwright Chromium browser..."
playwright install chromium

# 5. Fix Display / Xauthority & Auto-Run Agent
echo "[5/5] Launching AI Agent..."
touch ~/.Xauthority

if [ -z "$DISPLAY" ]; then
    export DISPLAY=:99
    xvfb-run -a python3 main.py
else
    python3 main.py
fi
