@echo off
title MONOLITH: Bounty Hunter (Zero Setup Required)
color 0A

echo ============================================
echo    BOUNTY ARBITRAGEUR - INSTANT REVENUE
echo ============================================
echo.
echo Starting bounty hunter agent...
echo This requires ZERO API keys or setup.
echo.

cd /d "%~dp0Monolith_v4.5_Immortal"
python System/Agents/bounty_arbitrageur.py

pause
