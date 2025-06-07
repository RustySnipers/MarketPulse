@echo off
set installer=MarketPulseSetup.exe
if not exist "%installer%" (
    echo Installer %installer% not found.
    pause
    exit /b 1
)
"%installer%"
if %ERRORLEVEL% NEQ 0 exit /b %ERRORLEVEL%
choice /M "Launch app now?"
if %ERRORLEVEL%==1 (
    start "" "%ProgramFiles%\Market Pulse\MarketPulse.exe"
)
del "%installer%"
