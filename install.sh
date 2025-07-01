#!/bin/bash

python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
sudo apt install python3-tk
python3 ./main.py

echo "Virtual environment created and dependencies installed."
