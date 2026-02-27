@echo off
title SOVEREIGN APEX IGNITION - OMEGA LEVEL
color 0C

:: Force the system into the exact Monolith folder regardless of where this script is run from
cd /d "C:\Users\Teagan Holland\Desktop\MONOLITH_COMMAND_CENTER"

echo =====================================================================
echo                ███╗   ███╗ ██████╗ ███╗   ██╗ ██████╗ 
echo                ████╗ ████║██╔═══██╗████╗  ██║██╔═══██╗
echo                ██╔████╔██║██║   ██║██╔██╗ ██║██║   ██║
echo                ██║╚██╔╝██║██║   ██║██║╚██╗██║██║   ██║
echo                ██║ ╚═╝ ██║╚██████╔╝██║ ╚████║╚██████╔╝
echo                ╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝ 
echo =====================================================================
echo.
echo WARNING: INITIATING OMEGA-LEVEL SWARM DEPLOYMENT
echo This will consume massive CPU/RAM and deploy 100+ concurrent agents.
echo.

echo [1/3] Initiating Master Sovereign Protocol (Brain, CFO, Profit Engine)...
start "Sovereign Core" cmd /c "cd /d "C:\Users\Teagan Holland\Desktop\MONOLITH_COMMAND_CENTER" & python master_launch_protocol.py & pause"

timeout /t 3 /nobreak >nul

echo [2/3] Unleashing Omnibus Daemon (Mass Swarm Deployment)...
start "Omnibus Swarm" cmd /c "cd /d "C:\Users\Teagan Holland\Desktop\MONOLITH_COMMAND_CENTER" & python monolith_daemon.py & pause"

timeout /t 3 /nobreak >nul

echo [3/3] Opening Sovereign Command Dashboard...
start "Sovereign Dashboard" cmd /c "cd /d "C:\Users\Teagan Holland\Desktop\MONOLITH_COMMAND_CENTER" & python master_dashboard.py & pause"

echo.
echo =====================================================================
echo SYSTEM ONLINE. ALL REVENUE AND EVOLUTION ENGINES ARE LIVE.
echo Do not close the spawned windows unless you intend to kill the Swarm.
echo =====================================================================
pause
