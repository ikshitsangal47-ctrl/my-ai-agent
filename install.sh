#!/bin/bash
echo "=================================================="
echo "   Setting up Custom AI Desktop Agent for Linux   "
echo "=================================================="

echo "[1/4] Installing Linux system dependencies..."
sudo apt-get update -y
sudo apt-get install -y python3-pip python3-tk python3-dev scrot python3-xlib portaudio19-dev libasound2-dev

echo "[2/4] Setting up Python Virtual Environment..."
python3 -m venv venv
source venv/bin/activate

echo "[3/4] Installing Python requirements & Playwright browsers..."
pip install --upgrade pip
pip install -r requirements.txt
playwright install-deps
playwright install chromium

echo "[4/4] Setup complete! Starting AI Agent..."
python3 main.py
