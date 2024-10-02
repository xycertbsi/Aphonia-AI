#!/bin/bash

# Kimenet elrejtése
set +x

echo "PIP Csomagok telepítése..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "A csomagok telepítése nem sikerült."
    exit 1
fi

echo "Program futtatása..."
python main.py

if [ $? -ne 0 ]; then
    echo "A program futtatása nem sikerült."
    exit 1
fi
