# =========================
# AI SAFE WINDOWS STRIP
# =========================

Write-Host "Stopping heavy services..."

$services = @(
"WSearch",
"SysMain",
"DiagTrack",
"dmwappushservice",
"MapsBroker",
"Fax",
"XblAuthManager",
"XblGameSave",
"XboxNetApiSvc",
"PrintSpooler"
)

foreach ($s in $services) {
  sc.exe stop $s | Out-Null
  sc.exe config $s start= disabled | Out-Null
}

Write-Host "Disabling background apps..."
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\BackgroundAccessApplications" /v GlobalUserDisabled /t REG_DWORD /d 1 /f

Write-Host "Disabling animations..."
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\VisualEffects" /v VisualFXSetting /t REG_DWORD /d 2 /f

Write-Host "Removing bloat apps..."
$apps = @(
"*Xbox*",
"*Cortana*",
"*ZuneMusic*",
"*ZuneVideo*",
"*People*",
"*YourPhone*",
"*Solitaire*",
"*Bing*",
"*News*",
"*Weather*"
)

foreach ($app in $apps) {
  Get-AppxPackage -AllUsers $app | Remove-AppxPackage -ErrorAction SilentlyContinue
}

Write-Host "Setting performance power plan..."
powercfg -setactive SCHEME_MIN

Write-Host "Fixing pagefile..."
wmic computersystem set AutomaticManagedPagefile=False | Out-Null
wmic pagefileset where name="C:\\pagefile.sys" set InitialSize=4096,MaximumSize=8192 | Out-Null

Write-Host "Disabling ads + telemetry UI..."
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\ContentDeliveryManager" /v SystemPaneSuggestionsEnabled /t REG_DWORD /d 0 /f
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Privacy" /v TailoredExperiencesWithDiagnosticDataEnabled /t REG_DWORD /d 0 /f

Write-Host "DONE. Reboot required."
