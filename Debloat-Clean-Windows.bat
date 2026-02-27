@echo off
title Windows 10/11 Debloat + Cleanup by ChatGPT
color 0A

echo ================================
echo  FULL WINDOWS DEBLOAT & CLEANUP
echo  ================================
echo.
echo Running as administrator...
echo.

:: Step 1: Clean Temp Folders
echo [*] Cleaning Temp folders...
del /s /q /f "%temp%\*"
del /s /q /f "C:\Windows\Temp\*"
ipconfig /flushdns

:: Step 2: Disable Telemetry Services
echo [*] Disabling telemetry services...
sc stop DiagTrack
sc delete DiagTrack
sc stop dmwappushservice
sc delete dmwappushservice
reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows\DataCollection" /v AllowTelemetry /t REG_DWORD /d 0 /f

:: Step 3: Disable Cortana
echo [*] Disabling Cortana...
reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows\Windows Search" /v AllowCortana /t REG_DWORD /d 0 /f

:: Step 4: Remove Xbox + Consumer Bloat Apps
echo [*] Removing Xbox and other bloatware...
powershell -Command "Get-AppxPackage *xbox* | Remove-AppxPackage"
powershell -Command "Get-AppxPackage *zune* | Remove-AppxPackage"
powershell -Command "Get-AppxPackage *bing* | Remove-AppxPackage"
powershell -Command "Get-AppxPackage *solitaire* | Remove-AppxPackage"
powershell -Command "Get-AppxPackage *getstarted* | Remove-AppxPackage"
powershell -Command "Get-AppxPackage *people* | Remove-AppxPackage"
powershell -Command "Get-AppxPackage *windowscommunicationsapps* | Remove-AppxPackage"
powershell -Command "Get-AppxPackage *skypeapp* | Remove-AppxPackage"

:: Step 5: Remove OneDrive
echo [*] Uninstalling OneDrive...
taskkill /f /im OneDrive.exe >nul 2>&1
%SystemRoot%\SysWOW64\OneDriveSetup.exe /uninstall
%SystemRoot%\System32\OneDriveSetup.exe /uninstall

:: Step 6: Disable Background Apps
echo [*] Disabling background apps...
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\BackgroundAccessApplications" /v GlobalUserDisabled /t REG_DWORD /d 1 /f

:: Step 7: Disable Action Center
echo [*] Disabling Action Center...
reg add "HKCU\Software\Policies\Microsoft\Windows\Explorer" /v DisableNotificationCenter /t REG_DWORD /d 1 /f

:: Step 8: Clean System Files
echo [*] Running Disk Cleanup silently...
cleanmgr /sagerun:1

:: Step 9: Disable Microsoft Feedback
echo [*] Disabling feedback prompts...
reg add "HKCU\Software\Microsoft\Siuf\Rules" /v NumberOfSIUFInPeriod /t REG_DWORD /d 0 /f
reg add "HKCU\Software\Microsoft\Siuf\Rules" /v PeriodInNanoSeconds /t REG_QWORD /d 0 /f

:: Done
echo.
echo ===============================
echo  DONE! System is now cleaned.
echo ===============================
pause
exit
