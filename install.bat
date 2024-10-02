@echo off

echo PIP csomagok telepitese...
if not exist requirements.txt (
    echo A requirements.txt fajl nem talalhato.
    timeout /t 5
    exit /b 1
)

py -m pip install -r requirements.txt
if errorlevel 1 (
    echo A csomagok telepitese nem sikerult.
    timeout /t 5
    exit /b 1
)

echo Program futtatas...
py main.py
if errorlevel 1 (
    echo A program futtatasa nem sikerult.
    timeout /t 5
    exit /b 1
)

echo Minden folyamat sikeresen befejezodott.
timeout /t 5
