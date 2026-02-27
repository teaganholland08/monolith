@echo off
title Monolith Omnibus Ignition
color 0A

echo =======================================================
echo          PROJECT MONOLITH - TOTAL SYSTEMS IGNITION 
echo =======================================================
echo.
echo Checking virtual environment...

:: Optional: Insert commands to activate virtualenv here if you use one.
:: Example: call venv\Scripts\activate.bat

echo Initiating the Omnibus Daemon...
echo All services (Core, Shell, Scale, Monitor) will boot simultaneously.
echo DO NOT CLOSE THIS WINDOW.
echo.

python monolith_daemon.py

pause
