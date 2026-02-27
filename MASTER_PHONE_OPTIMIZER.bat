@echo off
set ADB="C:\Users\Teagan Holland\Downloads\Monolith_Optimizer\platform-tools\adb.exe"
color 0B
echo ===============================================================
echo   PROJECT MONOLITH: MASTER HUD OPTIMIZER (GALAXY A03s)
echo ===============================================================
%ADB% devices

echo [+] STEP 1: Deep Cleaning System Cache...
%ADB% shell pm trim-caches 128G
%ADB% shell pm clear --cache-only com.android.chrome
%ADB% shell pm clear --cache-only com.google.android.youtube

echo [+] STEP 2: Stripping Samsung Bloatware...
for %%a in (com.samsung.android.arzone com.samsung.android.foryou com.samsung.sree com.samsung.android.kidsinstaller com.sec.android.app.sbrowser) do (
    %ADB% shell pm uninstall -k --user 0 %%a 2>nul
)

echo [+] STEP 3: Moving Media to SD Card (Manual Path)...
:: Using the direct ID we found earlier for your card
set SD=5388-FC59
for %%f in (DCIM Download Movies Music Pictures Documents) do (
    echo Moving %%f...
    %ADB% shell "mkdir -p /storage/%SD%/%%f"
    %ADB% shell "mv /sdcard/%%f/* /storage/%SD%/%%f/ 2>nul"
)

echo [+] STEP 4: Wiping Log History...
%ADB% shell logcat -c

echo ===============================================================
echo   OPTIMIZATION COMPLETE
echo ===============================================================
%ADB% shell df -h /data
pause
