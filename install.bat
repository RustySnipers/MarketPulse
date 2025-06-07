@echo off
setlocal
set "URL=https://github.com/your-username/MarketPulse/releases/latest/download/MarketPulseSetup.exe"
set "installer=%TEMP%\MarketPulseSetup.exe"

where curl >nul 2>&1
if %ERRORLEVEL%==0 (
    echo Downloading installer with curl...
    curl -L "%URL%" -o "%installer%"
) else (
    echo Downloading installer with PowerShell...
    powershell -Command "Invoke-WebRequest -Uri '%URL%' -OutFile '%installer%'"
)

"%installer%" /SILENT
if %ERRORLEVEL% NEQ 0 exit /b %ERRORLEVEL%
choice /M "Launch app now?"
if %ERRORLEVEL%==1 (
    start "" "%ProgramFiles%\Market Pulse\MarketPulse.exe"
)
del "%installer%"
endlocal
