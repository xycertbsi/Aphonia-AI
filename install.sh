#!/bin/bash

echo "PIP csomagok telepitese..."

if [ ! -f requirements.txt ]; then
    echo "A requirements.txt fajl nem talalhato."
    sleep 5
    exit 1
fi

# Kimenet elrejtése a pip install és python futtatas során
pip install -r requirements.txt > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "A csomagok telepitese nem sikerult."
    sleep 5
    exit 1
fi

echo "Program futtatas..."
python main.py > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "A program futtatasa nem sikerult."
    sleep 5
    exit 1
fi

echo "Minden folyamat sikeresen befejezodott."
sleep 5
