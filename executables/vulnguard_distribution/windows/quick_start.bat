@echo off
echo.
echo ========================================
echo   VulnGuard Security Platform v2.0
echo ========================================
echo.
echo Choose an option:
echo 1. Install complete platform
echo 2. Run security agent scan
echo 3. Launch desktop application
echo 4. Show CLI help
echo 5. Exit
echo.
set /p choice="Enter choice (1-5): "

if "%choice%"=="1" (
    echo Starting platform installer...
    vulnguard-installer.exe
) else if "%choice%"=="2" (
    echo Starting security scan...
    vulnguard-agent.exe --no-upload --verbose
) else if "%choice%"=="3" (
    echo Launching desktop application...
    start vulnguard-desktop.exe
) else if "%choice%"=="4" (
    echo VulnGuard CLI Help:
    vulnguard-cli.exe --help
) else if "%choice%"=="5" (
    exit
) else (
    echo Invalid choice. Please try again.
    pause
    goto start
)

echo.
pause
