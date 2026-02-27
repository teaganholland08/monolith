$ADB = "C:\Users\Teagan Holland\Downloads\Monolith_Optimizer\platform-tools\adb.exe"
$SD = "5388-FC59"

Clear-Host
Write-Host "--- PROJECT MONOLITH: AUTO-DOCKING SEQUENCE ---" -ForegroundColor Cyan

# 1. PC PURGE
Write-Host "[!] Scrubbing PC Temp Files..." -ForegroundColor Yellow
Remove-Item -Path "$env:TEMP\*" -Recurse -Force -ErrorAction SilentlyContinue
Clear-RecycleBin -Confirm:$false -ErrorAction SilentlyContinue

# 2. PHONE SYNC
Write-Host "[!] Connecting to Galaxy A03s..." -ForegroundColor Yellow
&$ADB wait-for-device

# 3. STORAGE CLEANSE
Write-Host "[!] Clearing Play Services Clog..." -ForegroundColor Yellow
&$ADB shell "pm clear com.google.android.gms"

Write-Host "[!] Relocating Media to SD Card..." -ForegroundColor Yellow
&$ADB shell "mv /sdcard/DCIM/* /storage/$SD/DCIM/" 2>$null
&$ADB shell "mv /sdcard/Pictures/* /storage/$SD/Pictures/" 2>$null

# 4. FINAL HUD REPORT
Write-Host "`n--- AUTO-DOCK COMPLETE ---" -ForegroundColor Green
&$ADB shell df -h /data | Select-String "/data/user/0"
Write-Host "Monolith is Lean. CEO is Cleared for Operations." -ForegroundColor White