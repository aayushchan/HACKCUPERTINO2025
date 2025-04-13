@echo off
echo Starting EcoLoop Application...

:: Set working directory to the script's location
cd /d "%~dp0"

:: Start the Python scraper in a new window
start cmd /k "python run_scraper.py"

:: Wait for scraper to initialize
timeout /t 5 >nul

:: Start the local web server in a new window
start cmd /k "python -m http.server 5000"

:: Open the browser to the app
start "" "http://localhost:5000/ecoloopapp.html"