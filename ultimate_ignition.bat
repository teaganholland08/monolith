@echo off
title SOVEREIGN APEX IGNITION - OMEGA LEVEL
color 0C

cd /d "%~dp0"

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

echo [1/2] Initiating Master Sovereign Protocol (Brain, CFO, Profit Engine)...
start "Sovereign Core" cmd /k "python master_launch_protocol.py"

timeout /t 3 /nobreak >nul

echo [2/2] Unleashing Omnibus Daemon (Mass Swarm Deployment)...
start "Omnibus Swarm" cmd /k "python monolith_daemon.py"

echo.
echo =====================================================================
echo SYSTEM ONLINE. ALL REVENUE AND EVOLUTION ENGINES ARE LIVE.
echo Do not close the spawned windows unless you intend to kill the Swarm.
echo =====================================================================
pause
